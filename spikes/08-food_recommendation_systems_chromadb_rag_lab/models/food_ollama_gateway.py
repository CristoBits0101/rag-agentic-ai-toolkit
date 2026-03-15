# --- DEPENDENCIAS ---
# 1. Configuracion: Para leer el nombre del modelo local.
# 2. Estado: Para reutilizar una unica instancia del LLM.
from config.food_recommendation_config import OLLAMA_MODEL_NAME
from state.food_recommendation_state import runtime_state

# --- MODELOS ---
# 1.1. Funcion para cargar el modelo local de Ollama.
def get_llm():
    # Sale temprano si ya se verifico la disponibilidad del LLM.
    if runtime_state.llm_checked:
        return runtime_state.llm_model

    # Marca la verificacion para no repetir importaciones costosas.
    runtime_state.llm_checked = True

    try:
        # Importa Ollama de forma perezosa para permitir fallback limpio.
        from langchain_ollama import OllamaLLM

        runtime_state.llm_model = OllamaLLM(
            model=OLLAMA_MODEL_NAME,
            temperature=0.3,
            num_predict=256,
        )
    except Exception:
        runtime_state.llm_model = None

    # Devuelve el LLM o None si no esta disponible.
    return runtime_state.llm_model


# 1.2. Funcion para ejecutar una llamada segura al LLM.
def invoke_llm(prompt: str):
    # Obtiene el modelo si existe en el entorno local.
    llm = get_llm()

    # Sale con None cuando no hay soporte local de Ollama.
    if llm is None:
        return None

    try:
        # Ejecuta la generacion y limpia espacios sobrantes.
        response = llm.invoke(prompt)
    except Exception:
        return None

    # Devuelve la respuesta como texto simple.
    return str(response).strip()
