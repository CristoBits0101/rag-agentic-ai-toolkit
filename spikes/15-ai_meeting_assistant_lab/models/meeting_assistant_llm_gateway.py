# --- DEPENDENCIAS ---
from config.meeting_assistant_config import OLLAMA_MODEL_NAME
from config.meeting_assistant_config import USE_OLLAMA_BY_DEFAULT

try:
    from langchain_ollama import OllamaLLM
except ImportError:
    OllamaLLM = None


def build_meeting_assistant_llm(use_ollama: bool = USE_OLLAMA_BY_DEFAULT):
    if not use_ollama:
        raise RuntimeError("Practica 15 requiere un modelo real de Ollama para generar actas.")

    if OllamaLLM is None:
        raise RuntimeError(
            "LangChain Ollama is not available. Install langchain-ollama before running practica 15."
        )

    try:
        return OllamaLLM(
            model=OLLAMA_MODEL_NAME,
            temperature=0.2,
            top_p=0.9,
            top_k=40,
            num_predict=512,
        )
    except Exception as exc:
        raise RuntimeError(
            f"Ollama could not load model {OLLAMA_MODEL_NAME}. Verify ollama serve and ollama pull {OLLAMA_MODEL_NAME}."
        ) from exc
