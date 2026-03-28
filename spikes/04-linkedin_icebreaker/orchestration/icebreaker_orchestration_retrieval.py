# --- DEPENDENCIAS ---
# 1. Chroma: Para almacenar embeddings en memoria.
# 2. Configuracion: Para leer nombre de coleccion y tamano de retrieval.
# 3. Modelos: Para obtener el modelo de embeddings.
# 4. Pipeline: Para preparar los trozos del perfil.
# 5. Estado: Para reutilizar la indexacion activa.
from langchain_community.vectorstores import Chroma

from config.icebreaker_config import COLLECTION_PREFIX
from config.icebreaker_config import TOP_K
from models.icebreaker_models import get_embedding_model
from pipeline.icebreaker_profile_pipeline import prepare_profile_chunks
from state.icebreaker_state import runtime_state

# --- RETRIEVAL ---
# 1.1. Funcion para crear una base vectorial a partir del perfil mock.
def build_vector_store(profile_key: str):
    # Obtiene el modelo local que genera embeddings.
    embedding_model = get_embedding_model()
    # Prepara los trozos del perfil ya normalizados.
    chunks = prepare_profile_chunks(profile_key)

    # Construye la base vectorial para este perfil.
    return Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        collection_name=f"{COLLECTION_PREFIX}_{profile_key}",
    )


# 1.2. Funcion para construir el retriever desde la base vectorial.
def build_retriever(vector_store):
    # Devuelve un retriever de similitud con el top k configurado.
    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": TOP_K},
    )


# 1.3. Funcion para reutilizar el retriever del perfil activo.
def get_profile_retriever(profile_key: str):
    # Reindexa solo si cambia el perfil o si aun no existe un retriever.
    if runtime_state.active_profile_key != profile_key or runtime_state.retriever is None:
        runtime_state.vector_store = build_vector_store(profile_key)
        runtime_state.retriever = build_retriever(runtime_state.vector_store)
        runtime_state.active_profile_key = profile_key

    # Devuelve el retriever listo para consultas.
    return runtime_state.retriever
