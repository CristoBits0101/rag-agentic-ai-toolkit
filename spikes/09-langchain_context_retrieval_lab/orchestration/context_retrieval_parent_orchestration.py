# --- DEPENDENCIAS ---
# 1. Configuracion: Para leer la consulta y chunk sizes del ejemplo.
# 2. Colecciones: Para cargar el documento base y nombres de coleccion.
# 3. Embeddings: Para construir la coleccion de child chunks.
from config.context_retrieval_config import CHILD_CHUNK_OVERLAP
from config.context_retrieval_config import CHILD_CHUNK_SIZE
from config.context_retrieval_config import COMPANY_POLICIES_FILE
from config.context_retrieval_config import PARENT_CHUNK_OVERLAP
from config.context_retrieval_config import PARENT_CHUNK_SIZE
from config.context_retrieval_config import PARENT_COLLECTION_PREFIX
from config.context_retrieval_config import PARENT_QUERY
from langchain.retrievers import ParentDocumentRetriever
from langchain.storage import InMemoryStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from models.context_retrieval_embedding_gateway import (
    build_context_retrieval_embeddings,
)
from orchestration.context_retrieval_collection_orchestration import (
    build_collection_name,
)
from orchestration.context_retrieval_collection_orchestration import (
    build_persist_directory,
)
from orchestration.context_retrieval_collection_orchestration import (
    load_text_documents,
)

# --- PARENT RETRIEVAL ---
def build_parent_document_retriever() -> tuple[
    ParentDocumentRetriever,
    Chroma,
    InMemoryStore,
]:
    # Prepara splitters pequenos y grandes para recuperar mejor contexto.
    parent_splitter = RecursiveCharacterTextSplitter(
        chunk_size=PARENT_CHUNK_SIZE,
        chunk_overlap=PARENT_CHUNK_OVERLAP,
        length_function=len,
    )
    child_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHILD_CHUNK_SIZE,
        chunk_overlap=CHILD_CHUNK_OVERLAP,
        length_function=len,
    )
    vectorstore = Chroma(
        collection_name=build_collection_name(PARENT_COLLECTION_PREFIX),
        embedding_function=build_context_retrieval_embeddings(),
        collection_metadata={"hnsw:space": "cosine"},
        persist_directory=build_persist_directory(PARENT_COLLECTION_PREFIX),
    )
    store = InMemoryStore()
    retriever = ParentDocumentRetriever(
        vectorstore=vectorstore,
        docstore=store,
        child_splitter=child_splitter,
        parent_splitter=parent_splitter,
    )
    return retriever, vectorstore, store


def retrieve_parent_documents(
    query: str = PARENT_QUERY,
) -> tuple[list[Document], list[Document], int]:
    # Indexa el manual de politicas y compara child y parent retrieval.
    retriever, vectorstore, store = build_parent_document_retriever()
    policy_documents = load_text_documents(COMPANY_POLICIES_FILE)
    retriever.add_documents(policy_documents)
    child_documents = vectorstore.similarity_search(query, k=2)
    parent_documents = retriever.invoke(query)
    parent_key_count = len(list(store.yield_keys()))
    return child_documents, parent_documents, parent_key_count
