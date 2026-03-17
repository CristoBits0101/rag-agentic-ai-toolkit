# --- DEPENDENCIAS ---
from functools import lru_cache

try:
    from langchain_ollama import OllamaEmbeddings
except Exception:
    OllamaEmbeddings = None

OLLAMA_EMBEDDING_MODEL_NAME = "nomic-embed-text"


@lru_cache(maxsize=1)
def build_context_retrieval_embeddings():
    if OllamaEmbeddings is None:
        raise RuntimeError(
            "LangChain Ollama is not available. Install langchain-ollama before running practica 09."
        )

    return OllamaEmbeddings(model=OLLAMA_EMBEDDING_MODEL_NAME)
