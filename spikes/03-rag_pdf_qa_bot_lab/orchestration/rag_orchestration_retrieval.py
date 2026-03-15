# --- DEPENDENCIAS ---
# 1.        Chroma: Para almacenar embeddings en una base vectorial.
# 2.  Configuracion: Para leer el numero de resultados y el nombre de la coleccion.
# 3. Documentos RAG: Para preparar trozos del PDF.
# 4.       Modelos: Para obtener el modelo de embeddings.
# 5.        Estado: Para reutilizar la indexacion en memoria.
from langchain_community.vectorstores import Chroma

from config.rag_config import COLLECTION_NAME
from config.rag_config import TOP_K
from models.rag_models import get_embedding_model
from pipeline.rag_document_pipeline import prepare_pdf_chunks
from state.rag_state import runtime_state

# --- RETRIEVAL ---
# 1.1. Funcion para crear la base vectorial desde los fragmentos.
def build_vector_store(chunks):
    # Obtiene el modelo que convierte texto en vectores.
    embedding_model = get_embedding_model()
    # Crea la base vectorial con los trozos del documento.
    vector_store = Chroma.from_documents(
        # Guarda los trozos ya preparados.
        documents=chunks,
        # Usa el modelo que genera vectores.
        embedding=embedding_model,
        # Asigna un nombre interno a la coleccion.
        collection_name=COLLECTION_NAME,
    )

    # Devuelve la base vectorial lista para retrieval.
    return vector_store


# 1.2. Funcion para crear el retriever desde la base vectorial.
def build_retriever(vector_store):
    # Crea el buscador a partir de la base vectorial.
    retriever_obj = vector_store.as_retriever(
        # Busca por similitud de significado.
        search_type="similarity",
        # Limita la cantidad de resultados recuperados.
        search_kwargs={"k": TOP_K},
    )

    # Devuelve el retriever ya preparado.
    return retriever_obj


# 1.3. Funcion para indexar un PDF y reutilizar su retriever.
def get_rag_retriever(file_path: str):
    # Reindexa solo si cambia el archivo o si no existe el retriever.
    if runtime_state.indexed_pdf_path != file_path or runtime_state.rag_retriever is None:
        # Prepara los trozos del PDF.
        chunks = prepare_pdf_chunks(file_path)
        # Crea la base vectorial con esos trozos.
        runtime_state.vector_store = build_vector_store(chunks)
        # Crea el retriever usando la base vectorial.
        runtime_state.rag_retriever = build_retriever(runtime_state.vector_store)
        # Guarda la ruta del PDF ya indexado.
        runtime_state.indexed_pdf_path = file_path

    # Devuelve el retriever listo para responder.
    return runtime_state.rag_retriever
