import os
import shutil
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from app.chunk import read_file_content, chunk_text
from app.embed import GoogleAIEmbedder
from app.store import ChromaVectorStore
from app.generate import GeminiGenerator

load_dotenv()

app = FastAPI(
    title="Sistema RAG API",
    description="API para ingestión documental, almacenamiento vectorial y consultas RAG ancladas.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

embedder: Optional[GoogleAIEmbedder] = None
vector_store: Optional[ChromaVectorStore] = None
generator: Optional[GeminiGenerator] = None


@app.on_event("startup")
def startup_event():
    global embedder, vector_store, generator
    try:
        embedder = GoogleAIEmbedder()
        vector_store = ChromaVectorStore()
        generator = GeminiGenerator()
    except Exception as e:
        print(f"Error durante la inicialización de servicios RAG: {str(e)}")


class QueryRequest(BaseModel):
    question: str = Field(..., description="Pregunta enviada por el usuario.")
    top_k: int = Field(default=3, ge=1, le=10, description="Número de chunks a recuperar.")


class ChunkDetail(BaseModel):
    id: str
    text: str
    source: str
    chunk_index: int
    distance: float


class CitationDetail(BaseModel):
    citation_id: str
    source: str
    chunk_index: int
    distance: float


class QueryResponse(BaseModel):
    question: str
    answer: str
    answered: bool
    reason: str
    citations: List[CitationDetail]
    retrieved_chunks: List[ChunkDetail]


class IngestResponse(BaseModel):
    source: str
    total_chunks: int
    inserted_count: int
    message: str


class HealthResponse(BaseModel):
    status: str
    chroma_status: str
    total_documents: int
    persist_directory: str


@app.get("/health", response_model=HealthResponse)
def health_check():
    """
    Verifica el estado de salud de la API y la conectividad con ChromaDB.
    """
    if vector_store is None:
        return HealthResponse(
            status="error",
            chroma_status="No inicializado",
            total_documents=0,
            persist_directory=""
        )

    try:
        stats = vector_store.get_stats()
        return HealthResponse(
            status="ok",
            chroma_status="conectado",
            total_documents=stats["total_documents"],
            persist_directory=stats["persist_directory"]
        )
    except Exception as e:
        return HealthResponse(
            status="error",
            chroma_status=f"error: {str(e)}",
            total_documents=0,
            persist_directory=""
        )


@app.post("/ingest", response_model=IngestResponse)
async def ingest_document(
    file: Optional[UploadFile] = File(None),
    file_path: Optional[str] = Form(None)
):
    """
    Recibe un archivo o ruta de archivo, realiza chunking, calcula embeddings con Google AI
    y persiste chunks y metadatos en ChromaDB.
    """
    if vector_store is None or embedder is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Servicios RAG no inicializados correctamente. Verifique la API Key de Google AI."
        )

    temp_path = None
    try:
        if file is not None:
            source_name = file.filename
            temp_dir = os.path.join(os.getcwd(), "temp_uploads")
            os.makedirs(temp_dir, exist_ok=True)
            temp_path = os.path.join(temp_dir, source_name)
            
            with open(temp_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            target_file = temp_path
        elif file_path is not None and file_path.strip():
            target_file = file_path.strip()
            source_name = os.path.basename(target_file)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Debe proporcionar un archivo (file) o una ruta de archivo (file_path)."
            )

        content = read_file_content(target_file)
        if not content.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El archivo '{source_name}' está vacío o no contiene texto legible."
            )

        chunks = chunk_text(content, source=source_name, chunk_size_words=300, overlap_words=50)
        if not chunks:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se pudieron generar chunks del archivo provisto."
            )

        chunk_texts = [c["text"] for c in chunks]
        embeddings = embedder.embed_texts(chunk_texts)

        inserted_count = vector_store.add_chunks(chunks, embeddings)

        return IngestResponse(
            source=source_name,
            total_chunks=len(chunks),
            inserted_count=inserted_count,
            message=f"Documento '{source_name}' procesado e ingestado exitosamente."
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error durante el proceso de ingesta: {str(e)}"
        )
    finally:
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass


@app.post("/query", response_model=QueryResponse)
def query_rag(request: QueryRequest):
    """
    Procesa consultas del usuario: vectoriza la pregunta, busca chunks similares en ChromaDB,
    evalúa criterios de abstención y genera respuestas ancladas con citas usando Gemini.
    """
    if vector_store is None or embedder is None or generator is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Servicios RAG no inicializados. Verifique la configuración de entorno y la API Key."
        )

    if not request.question.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La pregunta no puede estar vacía."
        )

    try:
        query_embedding = embedder.embed_query(request.question)
        retrieved = vector_store.search_similar(query_embedding, top_k=request.top_k)

        generation_result = generator.generate_response(request.question, retrieved)

        retrieved_chunk_details = [
            ChunkDetail(
                id=c["id"],
                text=c["text"],
                source=c["source"],
                chunk_index=c["chunk_index"],
                distance=c["distance"]
            )
            for c in retrieved
        ]

        citation_details = [
            CitationDetail(
                citation_id=c["citation_id"],
                source=c["source"],
                chunk_index=c["chunk_index"],
                distance=c["distance"]
            )
            for c in generation_result.get("citations", [])
        ]

        return QueryResponse(
            question=request.question,
            answer=generation_result["answer"],
            answered=generation_result["answered"],
            reason=generation_result["reason"],
            citations=citation_details,
            retrieved_chunks=retrieved_chunk_details
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar la consulta RAG: {str(e)}"
        )
