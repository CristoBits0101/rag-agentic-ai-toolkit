# --- DEPENDENCIAS ---
from config.meeting_assistant_config import OLLAMA_MODEL_NAME
from config.meeting_assistant_config import USE_OLLAMA_BY_DEFAULT
from models.meeting_assistant_demo_llm import build_meeting_assistant_demo_llm

try:
    from langchain_ollama import OllamaLLM
except ImportError:
    OllamaLLM = None


def build_meeting_assistant_llm(use_ollama: bool = USE_OLLAMA_BY_DEFAULT):
    if use_ollama and OllamaLLM is not None:
        try:
            return OllamaLLM(
                model=OLLAMA_MODEL_NAME,
                temperature=0.2,
                top_p=0.9,
                top_k=40,
                num_predict=512,
            )
        except Exception:
            pass

    return build_meeting_assistant_demo_llm()
