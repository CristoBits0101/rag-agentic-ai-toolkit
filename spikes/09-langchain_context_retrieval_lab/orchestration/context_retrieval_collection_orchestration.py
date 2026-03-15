# --- DEPENDENCIAS ---
# 1. Tempfile: Para aislar cada vector store en un directorio temporal.
# 1. Uuid: Para generar nombres de coleccion aislados por ejecucion.
# 2. Configuracion: Para leer rutas y chunk sizes del laboratorio.
# 3. Dataset: Para cargar el conjunto local de peliculas.
# 4. Embeddings: Para crear el embedding determinista del vector store.
from tempfile import mkdtemp
from uuid import uuid4

from config.context_retrieval_config import COMPANY_POLICIES_FILE
from config.context_retrieval_config import MOVIE_COLLECTION_PREFIX
from config.context_retrieval_config import NOTES_CHUNK_OVERLAP
from config.context_retrieval_config import NOTES_CHUNK_SIZE
from config.context_retrieval_config import NOTES_COLLECTION_PREFIX
from config.context_retrieval_config import POLICY_CHUNK_OVERLAP
from config.context_retrieval_config import POLICY_CHUNK_SIZE
from config.context_retrieval_config import POLICY_COLLECTION_PREFIX
from config.context_retrieval_config import RETRIEVAL_NOTES_FILE
from data.context_retrieval_movie_dataset import MOVIE_RECORDS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from models.context_retrieval_embedding_gateway import (
    build_context_retrieval_embeddings,
)

# --- CARGA ---
def build_collection_name(prefix: str) -> str:
    # Crea un nombre unico para evitar colisiones entre tests.
    return f"{prefix}_{uuid4().hex[:8]}"


def build_persist_directory(prefix: str) -> str:
    # Aisla cada vector store para evitar estado compartido entre suites.
    return mkdtemp(prefix=f"{prefix}_")


def load_text_documents(file_path) -> list[Document]:
    # Carga un archivo local como una lista de documentos de LangChain.
    loader = TextLoader(str(file_path), encoding="utf-8")
    return loader.load()


def split_documents(
    documents: list[Document],
    chunk_size: int,
    chunk_overlap: int,
) -> list[Document]:
    # Divide documentos largos en chunks consistentes para retrieval.
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )
    return splitter.split_documents(documents)


def build_policy_vectorstore() -> tuple[Chroma, list[Document]]:
    # Carga y divide el manual de politicas de empresa.
    policy_documents = load_text_documents(COMPANY_POLICIES_FILE)
    policy_chunks = split_documents(
        policy_documents,
        POLICY_CHUNK_SIZE,
        POLICY_CHUNK_OVERLAP,
    )
    vectorstore = Chroma.from_documents(
        documents=policy_chunks,
        embedding=build_context_retrieval_embeddings(),
        collection_name=build_collection_name(POLICY_COLLECTION_PREFIX),
        collection_metadata={"hnsw:space": "cosine"},
        persist_directory=build_persist_directory(POLICY_COLLECTION_PREFIX),
    )
    return vectorstore, policy_chunks


def build_retrieval_notes_vectorstore() -> tuple[Chroma, list[Document]]:
    # Carga y divide las notas locales de context retrieval.
    notes_documents = load_text_documents(RETRIEVAL_NOTES_FILE)
    notes_chunks = split_documents(
        notes_documents,
        NOTES_CHUNK_SIZE,
        NOTES_CHUNK_OVERLAP,
    )
    vectorstore = Chroma.from_documents(
        documents=notes_chunks,
        embedding=build_context_retrieval_embeddings(),
        collection_name=build_collection_name(NOTES_COLLECTION_PREFIX),
        collection_metadata={"hnsw:space": "cosine"},
        persist_directory=build_persist_directory(NOTES_COLLECTION_PREFIX),
    )
    return vectorstore, notes_chunks


def build_movie_documents() -> list[Document]:
    # Convierte el dataset local de peliculas a documentos de LangChain.
    return [
        Document(
            page_content=record["page_content"],
            metadata=record["metadata"],
        )
        for record in MOVIE_RECORDS
    ]


def build_movie_vectorstore() -> tuple[Chroma, list[Document]]:
    # Construye el vector store de peliculas para filtros por metadatos.
    movie_documents = build_movie_documents()
    vectorstore = Chroma.from_documents(
        documents=movie_documents,
        embedding=build_context_retrieval_embeddings(),
        collection_name=build_collection_name(MOVIE_COLLECTION_PREFIX),
        collection_metadata={"hnsw:space": "cosine"},
        persist_directory=build_persist_directory(MOVIE_COLLECTION_PREFIX),
    )
    return vectorstore, movie_documents
