# --- DEPENDENCIAS ---
# 1. OllamaEmbeddings: Para generar embeddings desde Ollama.
# 2.        OllamaLLM: Para responder preguntas con un modelo local de Ollama.
# 3.     Configuracion: Para leer nombres de modelos.
# 4.            Estado: Para reutilizar instancias cargadas.
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import OllamaLLM

from rag_config import EMBED_MODEL_NAME
from rag_config import MODEL_NAME
from rag_state import runtime_state

# --- MODELOS ---
# 1.1. Funcion para cargar el modelo LLM de Ollama.
def get_llm():
    # Carga el modelo solo la primera vez.
    if runtime_state.llm_model is None:
        # Crea el modelo de Ollama para responder preguntas.
        runtime_state.llm_model = OllamaLLM(
            # Usa el nombre del modelo configurado.
            model=MODEL_NAME,
            # Ajusta la variacion de la respuesta.
            temperature=0.5,
            # Limita la longitud maxima de la salida.
            num_predict=256,
        )

    # Devuelve el LLM listo para la cadena QA.
    return runtime_state.llm_model


# 1.2. Funcion para cargar el modelo de embeddings de Ollama.
def get_embedding_model():
    # Carga el modelo solo la primera vez.
    if runtime_state.embedding_model is None:
        # Crea el modelo que convierte texto en vectores.
        runtime_state.embedding_model = OllamaEmbeddings(
            # Usa el nombre del modelo de embeddings configurado.
            model=EMBED_MODEL_NAME,
        )

    # Devuelve el modelo listo para vectorizar fragmentos.
    return runtime_state.embedding_model
