import os
import uuid
from typing import List, Dict, Any
import chromadb
from chromadb.config import Settings
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DEFAULT_CHROMA_PATH = os.getenv("CHROMA_PATH", os.path.join(BASE_DIR, "chroma"))


class ChromaVectorStore:
    """
    Manages persistent ChromaDB vector storage and query retrieval.
    Precomputed embeddings from Google AI are explicitly passed to Chroma.
    """

    def __init__(self, persist_directory: str = DEFAULT_CHROMA_PATH, collection_name: str = "rag_documents"):
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        
        os.makedirs(self.persist_directory, exist_ok=True)
        
        self.client = chromadb.PersistentClient(path=self.persist_directory)
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def add_chunks(
        self,
        chunks: List[Dict[str, Any]],
        embeddings: List[List[float]]
    ) -> int:
        """
        Inserts document chunks along with their precomputed embeddings and metadata.
        """
        if not chunks or not embeddings or len(chunks) != len(embeddings):
            raise ValueError("Chunks and embeddings must be non-empty and equal in length.")

        ids = []
        documents = []
        metadatas = []

        for chunk in chunks:
            chunk_id = str(uuid.uuid4())
            ids.append(chunk_id)
            documents.append(chunk["text"])
            metadatas.append({
                "source": str(chunk.get("source", "unknown")),
                "chunk_index": int(chunk.get("chunk_index", 0))
            })

        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas
        )

        return len(ids)

    def search_similar(
        self,
        query_embedding: List[float],
        top_k: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Executes k-NN similarity search against stored embeddings.
        Returns matching document chunks, metadata, and distance metrics.
        """
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )

        retrieved = []
        if not results or not results["documents"] or not results["documents"][0]:
            return retrieved

        docs = results["documents"][0]
        metas = results["metadatas"][0]
        dists = results["distances"][0]
        ids = results["ids"][0]

        for i in range(len(docs)):
            retrieved.append({
                "id": ids[i],
                "text": docs[i],
                "source": metas[i].get("source", "unknown"),
                "chunk_index": metas[i].get("chunk_index", 0),
                "distance": float(dists[i])
            })

        return retrieved

    def get_stats(self) -> Dict[str, Any]:
        """
        Returns stats about stored collections and total items.
        """
        return {
            "collection_name": self.collection_name,
            "total_documents": self.collection.count(),
            "persist_directory": self.persist_directory
        }
