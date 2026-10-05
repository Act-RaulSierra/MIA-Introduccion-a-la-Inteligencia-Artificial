import os
from typing import List, Dict, Any
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

DEFAULT_DISTANCE_THRESHOLD = float(os.getenv("ABSTENTION_DISTANCE_THRESHOLD", "0.65"))
DEFAULT_GENERATION_MODEL = os.getenv("GENERATION_MODEL", "gemini-3.8-flash")
FALLBACK_GENERATION_MODELS = [
    DEFAULT_GENERATION_MODEL,
    "gemini-3.8-flash",
    "gemini-2.0-flash",
    "gemini-1.5-flash"
]


class GeminiGenerator:
    """
    Orquesta la generación de respuestas ancladas con Gemini, lista priorizada de candidatos
    y aplicación estricta de citas y abstención.
    """

    def __init__(
        self,
        model_name: str = None,
        api_key: str = None,
        distance_threshold: float = DEFAULT_DISTANCE_THRESHOLD
    ):
        self.primary_model_name = model_name or DEFAULT_GENERATION_MODEL
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("No se encontro una clave de API valida. Configure GOOGLE_API_KEY o GEMINI_API_KEY en su archivo .env.")
        self.client = genai.Client(api_key=self.api_key)
        self.distance_threshold = distance_threshold
        self.active_model_name = self.primary_model_name

    def _generate_with_fallback(self, user_prompt: str, system_instruction: str) -> Any:
        """
        Ejecuta la generación intentando primero con el modelo configurado/activo,
        recorriendo la lista de candidatos (gemini-3.8-flash, gemini-2.0-flash, gemini-1.5-flash)
        ante errores 404 o NOT_FOUND.
        """
        candidate_models = [self.active_model_name]
        for m in FALLBACK_GENERATION_MODELS:
            if m not in candidate_models:
                candidate_models.append(m)

        last_exception = None
        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.1,
            top_p=0.9
        )

        for model in candidate_models:
            try:
                response = self.client.models.generate_content(
                    model=model,
                    contents=user_prompt,
                    config=config
                )
                self.active_model_name = model
                return response
            except Exception as e:
                last_exception = e
                err_msg = str(e).lower()
                if "404" in err_msg or "not_found" in err_msg or "not found" in err_msg:
                    continue
                else:
                    raise e

        if last_exception:
            raise last_exception
        raise RuntimeError("No se pudo generar respuesta con ninguno de los modelos intentados.")

    def generate_response(
        self,
        question: str,
        retrieved_chunks: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Genera una respuesta anclada exclusivamente en los chunks recuperados.
        Evalúa el umbral matemático de distancia y los criterios de abstención.
        """
        if not retrieved_chunks:
            return {
                "answer": "No se encontraron documentos relevantes en la base de conocimientos para responder a su consulta.",
                "answered": False,
                "reason": "Sin chunks recuperados.",
                "citations": []
            }

        best_distance = min(chunk.get("distance", 1.0) for chunk in retrieved_chunks)
        if best_distance > self.distance_threshold:
            return {
                "answer": "No dispongo de suficiente información en la base de datos documental para responder a esta pregunta con certeza.",
                "answered": False,
                "reason": f"Distancia del chunk más cercano ({best_distance:.4f}) supera el umbral de abstención ({self.distance_threshold:.4f}).",
                "citations": []
            }

        context_parts = []
        citations_metadata = []
        
        for idx, chunk in enumerate(retrieved_chunks, start=1):
            source_file = chunk.get("source", "desconocido")
            chunk_idx = chunk.get("chunk_index", 0)
            text = chunk.get("text", "")
            
            context_parts.append(f"[{idx}] (Fuente: {source_file}, Chunk: {chunk_idx})\n{text}")
            citations_metadata.append({
                "citation_id": f"[{idx}]",
                "source": source_file,
                "chunk_index": chunk_idx,
                "distance": chunk.get("distance", 0.0)
            })

        formatted_context = "\n\n".join(context_parts)

        system_instruction = (
            "Eres un asistente de inteligencia artificial especializado y riguroso. "
            "Tu tarea es responder a la pregunta del usuario basándote EXCLUSIVAMENTE en el contexto proporcionado. "
            "Reglas strictly de respuesta:\n"
            "1. Responde siempre en idioma español.\n"
            "2. Toda afirmación o dato en tu respuesta debe estar explícitamente respaldado por el contexto y debe incluir su cita en formato [1], [2], etc.\n"
            "3. Si el contexto no contiene información suficiente para responder a la pregunta, debes abstenerte de inventar o usar conocimientos previos y responder exactamente: 'No dispongo de suficiente información en el contexto provisto para responder a esta pregunta.'\n"
            "4. No utilices emoticones, emojis ni caracteres gráficos bajo ninguna circunstancia. Tu formato debe ser texto estricto y profesional."
        )

        user_prompt = (
            f"CONTEXTO RECUPERADO:\n{formatted_context}\n\n"
            f"PREGUNTA DEL USUARIO:\n{question}\n\n"
            f"RESPUESTA ANCLADA Y CITADA:"
        )

        try:
            response = self._generate_with_fallback(user_prompt, system_instruction)
            response_text = response.text.strip() if response.text else ""

            abstention_phrases = [
                "no dispongo de suficiente información",
                "no se encuentra información",
                "no hay suficiente información",
                "no contiene información"
            ]

            is_abstained = any(phrase in response_text.lower() for phrase in abstention_phrases)

            return {
                "answer": response_text,
                "answered": not is_abstained,
                "reason": "Evaluación exitosa de contexto." if not is_abstained else "Modelo determinó falta de evidencia en contexto.",
                "citations": citations_metadata if not is_abstained else []
            }

        except Exception as e:
            return {
                "answer": f"Error al generar respuesta con el modelo de lenguaje: {str(e)}",
                "answered": False,
                "reason": f"Excepción en API de generación: {str(e)}",
                "citations": []
            }
