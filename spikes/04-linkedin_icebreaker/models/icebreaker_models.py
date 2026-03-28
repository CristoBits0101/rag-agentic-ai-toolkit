# --- DEPENDENCIAS ---
# 1. OllamaEmbeddings: Para generar embeddings desde Ollama.
# 2. OllamaLLM: Para responder con un modelo local de Ollama.
# 3. Configuracion: Para leer nombres de modelos.
# 4. Estado: Para reutilizar el modelo de embeddings.
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import OllamaLLM

from config.icebreaker_config import DEFAULT_LLM_MODEL
from config.icebreaker_config import EMBED_MODEL_NAME
from state.icebreaker_state import runtime_state

# --- MODELOS ---
# 1.1. Funcion para crear el LLM de Ollama con parametros por llamada.
def build_llm(
    model_name: str = DEFAULT_LLM_MODEL,
    temperature: float = 0.0,
    num_predict: int = 256,
):
    # Devuelve una instancia lista para usar en la cadena de prompts.
    return OllamaLLM(
        model=model_name,
        temperature=temperature,
        num_predict=num_predict,
    )


# 1.2. Funcion para cargar y reutilizar el modelo de embeddings.
def get_embedding_model(model_name: str = EMBED_MODEL_NAME):
    # Reutiliza el modelo si ya fue cargado con el mismo nombre.
    if (
        runtime_state.embedding_model is None
        or runtime_state.embedding_model_name != model_name
    ):
        runtime_state.embedding_model = OllamaEmbeddings(model=model_name)
        runtime_state.embedding_model_name = model_name

    # Devuelve el modelo de embeddings listo para vectorizar texto.
    return runtime_state.embedding_model
