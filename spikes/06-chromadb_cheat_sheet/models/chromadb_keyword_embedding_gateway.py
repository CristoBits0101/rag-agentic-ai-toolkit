# --- DEPENDENCIAS ---
from functools import lru_cache

import numpy as np

try:
    from langchain_ollama import OllamaEmbeddings
except Exception:
    OllamaEmbeddings = None

OLLAMA_EMBEDDING_MODEL_NAME = "nomic-embed-text"


@lru_cache(maxsize=1)
def get_embedding_model():
    if OllamaEmbeddings is None:
        raise RuntimeError(
            "LangChain Ollama is not available. Install langchain-ollama before running practica 06."
        )

    return OllamaEmbeddings(model=OLLAMA_EMBEDDING_MODEL_NAME)


def build_keyword_embedding(text: str) -> np.ndarray:
    vector = get_embedding_model().embed_query(text)
    return np.array(vector, dtype=np.float32)


def build_keyword_embeddings(texts: list[str]) -> list[list[float]]:
    return get_embedding_model().embed_documents(texts)
