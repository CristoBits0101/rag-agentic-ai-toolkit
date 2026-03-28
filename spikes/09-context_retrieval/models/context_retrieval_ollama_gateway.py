# --- DEPENDENCIAS ---
from functools import lru_cache

try:
    from langchain_ollama import OllamaLLM
except Exception:
    OllamaLLM = None

OLLAMA_RETRIEVAL_MODEL_NAME = "qwen2.5:7b"


@lru_cache(maxsize=1)
def build_context_retrieval_llm():
    if OllamaLLM is None:
        raise RuntimeError(
            "LangChain Ollama is not available. Install langchain-ollama before running practica 09."
        )

    return OllamaLLM(
        model=OLLAMA_RETRIEVAL_MODEL_NAME,
        temperature=0,
        num_predict=256,
    )
