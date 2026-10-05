import os
from typing import List, Dict, Any
from pypdf import PdfReader


def read_file_content(file_path: str) -> str:
    """
    Reads text content from .txt, .md, or .pdf files.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()

    if ext in [".txt", ".md"]:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except UnicodeDecodeError:
            with open(file_path, "r", encoding="latin-1") as f:
                return f.read()

    elif ext == ".pdf":
        reader = PdfReader(file_path)
        text_content = []
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text_content.append(extracted)
        return "\n".join(text_content)

    else:
        raise ValueError(f"Unsupported file extension: {ext}")


def chunk_text(
    text: str,
    source: str,
    chunk_size_words: int = 300,
    overlap_words: int = 50
) -> List[Dict[str, Any]]:
    """
    Splits text into chunks of specified word length with overlap.
    Returns a list of dictionaries containing text, chunk index, and source metadata.
    """
    words = text.split()
    if not words:
        return []

    chunks = []
    step = chunk_size_words - overlap_words
    if step <= 0:
        step = max(1, chunk_size_words // 2)

    chunk_index = 0
    for i in range(0, len(words), step):
        chunk_words = words[i:i + chunk_size_words]
        chunk_str = " ".join(chunk_words)
        
        chunks.append({
            "text": chunk_str,
            "chunk_index": chunk_index,
            "source": source
        })
        chunk_index += 1
        
        if i + chunk_size_words >= len(words):
            break

    return chunks
