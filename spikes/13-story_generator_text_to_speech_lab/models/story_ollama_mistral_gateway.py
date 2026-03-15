# --- DEPENDENCIAS ---
from config.story_real_provider_config import OLLAMA_STORY_MODEL_NAME

try:
    from langchain_ollama import OllamaLLM
except ImportError:
    OllamaLLM = None

# --- MODEL ---
def generate_story_with_ollama_mistral(
    prompt: str,
    model_name: str = OLLAMA_STORY_MODEL_NAME,
) -> str:
    if OllamaLLM is None:
        raise RuntimeError(
            "LangChain Ollama is not available. Install langchain-ollama and ensure Ollama is running."
        )

    try:
        llm = OllamaLLM(
            model=model_name,
            temperature=0.4,
            top_p=0.9,
            top_k=40,
            num_predict=768,
        )
        return str(llm.invoke(prompt)).strip()
    except Exception as exc:
        raise RuntimeError(
            f"Ollama could not generate the story with model {model_name}. Verify ollama serve and ollama pull {model_name}."
        ) from exc
