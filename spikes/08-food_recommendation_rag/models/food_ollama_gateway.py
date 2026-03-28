# --- DEPENDENCIAS ---
# 1. Configuracion: Para leer el nombre del modelo local.
# 2. Estado: Para reutilizar una unica instancia del LLM.
from config.food_recommendation_config import OLLAMA_MODEL_NAME
from state.food_recommendation_state import runtime_state

# --- MODELOS ---
# 1.1. Funcion para cargar el modelo local de Ollama.
def get_llm():
    # Reutiliza el modelo ya inicializado.
    if runtime_state.llm_model is not None:
        return runtime_state.llm_model

    try:
        # Importa Ollama de forma perezosa para no cargar la dependencia antes de tiempo.
        from langchain_ollama import OllamaLLM
    except Exception as exc:
        raise RuntimeError(
            "LangChain Ollama is not available. Install langchain-ollama before running practica 08."
        ) from exc

    try:
        runtime_state.llm_model = OllamaLLM(
            model=OLLAMA_MODEL_NAME,
            temperature=0.3,
            num_predict=256,
        )
        return runtime_state.llm_model
    except Exception as exc:
        raise RuntimeError(
            f"Ollama could not load model {OLLAMA_MODEL_NAME}. Verify ollama serve and ollama pull {OLLAMA_MODEL_NAME}."
        ) from exc


# 1.2. Funcion para ejecutar una llamada segura al LLM.
def invoke_llm(prompt: str):
    # Obtiene el modelo real del spike.
    llm = get_llm()

    try:
        # Ejecuta la generacion y limpia espacios sobrantes.
        response = llm.invoke(prompt)
    except Exception as exc:
        raise RuntimeError("Ollama could not complete the food recommendation prompt.") from exc

    # Devuelve la respuesta como texto simple.
    return str(response).strip()
