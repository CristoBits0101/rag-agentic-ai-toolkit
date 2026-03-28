# --- DEPENDENCIAS ---
# 1. Configuracion: Para leer el nombre del modelo por defecto.
# 2. Estado: Para reutilizar el modelo de embeddings ya cargado.
from config.similarity_runtime_config import MODEL_NAME
from state.similarity_runtime_state import runtime_state

# --- MODELOS ---
# 1.1. Funcion para cargar el modelo de embeddings bajo demanda.
def get_embedding_model(model_name: str = MODEL_NAME):
    # Carga la libreria solo cuando la practica realmente lo necesita.
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError as exc:
        raise ImportError(
            "Falta sentence-transformers. Instala con pip install -U sentence-transformers==4.1.0."
        ) from exc

    # Reutiliza el modelo si ya fue cargado con el mismo nombre.
    if runtime_state.embedding_model is None or runtime_state.model_name != model_name:
        runtime_state.embedding_model = SentenceTransformer(model_name)
        runtime_state.model_name = model_name

    # Devuelve el modelo listo para generar embeddings.
    return runtime_state.embedding_model


# 1.2. Funcion para convertir una lista de textos en embeddings.
def encode_texts(texts: list[str], model_name: str = MODEL_NAME):
    # Usa el modelo ya cargado o lo inicializa si hace falta.
    embedding_model = get_embedding_model(model_name)

    # Devuelve embeddings en formato Numpy para operaciones matriciales.
    return embedding_model.encode(texts)
