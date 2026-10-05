import os
from typing import List, Any, Optional
from google import genai
from dotenv import load_dotenv

load_dotenv()

DEFAULT_EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "gemini-embedding-001")


class GoogleAIEmbedder:
    """
    Cliente de embeddings de Google AI con descubrimiento dinámico de modelos
    y extracción robusta de vectores empleando el SDK google-genai.
    """

    def __init__(self, model_name: Optional[str] = None, api_key: Optional[str] = None):
        self.requested_model_name = model_name or DEFAULT_EMBEDDING_MODEL
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("No se encontro una clave de API valida. Configure GOOGLE_API_KEY o GEMINI_API_KEY en su archivo .env.")
        self.client = genai.Client(api_key=self.api_key)
        self.active_model_name = self._resolve_embedding_model(self.requested_model_name)

    def _clean_model_name(self, name: str) -> str:
        """
        Remueve el prefijo 'models/' si está presente para estandarizar la llamada a la API.
        """
        if name and name.startswith("models/"):
            return name[len("models/"):]
        return name

    def _discover_available_embedding_models(self) -> List[str]:
        """
        Consulta dinámicamente client.models.list() para identificar los modelos
        que soportan generación de embeddings (embedContent).
        """
        discovered = []
        try:
            for m in self.client.models.list():
                raw_name = getattr(m, "name", "")
                clean_name = self._clean_model_name(raw_name)
                
                supported_actions = getattr(m, "supported_actions", []) or getattr(m, "supported_generation_methods", [])
                supported_str = " ".join([str(sa).lower() for sa in supported_actions])
                
                if "embed" in clean_name.lower() or "embed" in supported_str or "embedcontent" in supported_str:
                    discovered.append(clean_name)
        except Exception:
            pass

        return discovered

    def _resolve_embedding_model(self, preferred_name: str) -> str:
        """
        Resuelve el modelo de embedding a utilizar priorizando el modelo solicitado,
        o seleccionando dinámicamente el primer modelo disponible que contenga 'embedding'.
        """
        clean_preferred = self._clean_model_name(preferred_name)
        available_models = self._discover_available_embedding_models()

        if available_models:
            if clean_preferred in available_models:
                return clean_preferred
            
            for model in available_models:
                if "gemini-embedding" in model.lower():
                    return model
            
            for model in available_models:
                if "embedding" in model.lower():
                    return model
            
            return available_models[0]

        fallback_candidates = [
            clean_preferred,
            "gemini-embedding-001",
            "gemini-embedding-2",
            "text-embedding-004",
            "embedding-001"
        ]
        return fallback_candidates[0]

    def _extract_vector_values(self, response: Any) -> List[List[float]]:
        """
        Extrae de forma robusta la lista de listas de números flotantes del objeto de respuesta.
        Soporta respuestas batch (embeddings) y respuesta única (embedding).
        """
        if hasattr(response, "embeddings") and response.embeddings:
            extracted = []
            for emb in response.embeddings:
                if hasattr(emb, "values") and emb.values:
                    extracted.append(list(emb.values))
            return extracted

        if hasattr(response, "embedding") and response.embedding:
            emb = response.embedding
            if hasattr(emb, "values") and emb.values:
                return [list(emb.values)]

        raise ValueError("No se pudieron extraer valores de vector de la respuesta de embeddings.")

    def _embed_with_fallback(self, contents: Any) -> List[List[float]]:
        """
        Ejecuta la llamada a embed_content intentando con el modelo activo.
        Si ocurre un error 404 NOT_FOUND, realiza una redescubrimiento dinámico de modelos.
        """
        try:
            res = self.client.models.embed_content(
                model=self.active_model_name,
                contents=contents
            )
            return self._extract_vector_values(res)
        except Exception as e:
            err_msg = str(e).lower()
            if "404" in err_msg or "not_found" in err_msg or "not found" in err_msg:
                available_models = self._discover_available_embedding_models()
                for alt_model in available_models:
                    if alt_model == self.active_model_name:
                        continue
                    try:
                        res = self.client.models.embed_content(
                            model=alt_model,
                            contents=contents
                        )
                        self.active_model_name = alt_model
                        return self._extract_vector_values(res)
                    except Exception:
                        continue
            raise e

    def embed_texts(self, texts: List[str], batch_size: int = 100) -> List[List[float]]:
        """
        Vectoriza una lista de cadenas de texto en lotes.
        """
        if not texts:
            return []

        all_embeddings = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            batch_vectors = self._embed_with_fallback(contents=batch)
            all_embeddings.extend(batch_vectors)

        return all_embeddings

    def embed_query(self, query: str) -> List[float]:
        """
        Vectoriza una única cadena de texto de consulta.
        """
        vectors = self._embed_with_fallback(contents=query)
        if not vectors:
            raise ValueError("No se pudo obtener el vector de la consulta.")
        return vectors[0]
