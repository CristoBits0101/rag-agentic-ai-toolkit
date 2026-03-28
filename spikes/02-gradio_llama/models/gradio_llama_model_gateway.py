# --- DEPENDENCIAS ---
# 1.    OllamaLLM: Para responder preguntas con un modelo local.
# 2. Configuracion: Para leer el nombre del modelo.
# 3.        Estado: Para reutilizar la instancia cargada.
from langchain_ollama import OllamaLLM

from config.gradio_llama_runtime_config import MODEL_NAME
from state.gradio_llama_runtime_state import runtime_state


# Carga el modelo solo una vez.
def get_llama_model():
    # Crea la instancia solo en la primera llamada.
    if runtime_state.llama_model is None:
        runtime_state.llama_model = OllamaLLM(
            model=MODEL_NAME,
            temperature=0.3,
            top_p=0.9,
            top_k=40,
            num_predict=256,
        )

    # Devuelve la instancia lista para reutilizar.
    return runtime_state.llama_model
