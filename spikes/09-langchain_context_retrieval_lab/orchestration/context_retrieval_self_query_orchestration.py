# --- DEPENDENCIAS ---
# 1. Configuracion: Para reutilizar las consultas del laboratorio.
# 2. LLM Demo: Para traducir lenguaje natural a filtros.
# 3. Peliculas: Para crear el vector store con metadatos.
from config.context_retrieval_config import SELF_QUERY_PROMPTS
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain_core.documents import Document
from models.context_retrieval_demo_llm import build_context_retrieval_demo_llm
from orchestration.context_retrieval_collection_orchestration import (
    build_movie_vectorstore,
)

# --- SELF QUERY ---
def build_metadata_field_info() -> list[AttributeInfo]:
    # Define los metadatos que el retriever puede filtrar.
    return [
        AttributeInfo(
            name="genre",
            description="The genre of the movie.",
            type="string",
        ),
        AttributeInfo(
            name="year",
            description="The year the movie was released.",
            type="integer",
        ),
        AttributeInfo(
            name="director",
            description="The name of the movie director.",
            type="string",
        ),
        AttributeInfo(
            name="rating",
            description="A 1 to 10 rating for the movie.",
            type="float",
        ),
    ]


def retrieve_self_query_documents(query: str) -> list[Document]:
    # Ejecuta el SelfQueryRetriever sobre el dataset de peliculas.
    vectorstore, _movie_documents = build_movie_vectorstore()
    retriever = SelfQueryRetriever.from_llm(
        build_context_retrieval_demo_llm(),
        vectorstore,
        "Brief summary of a movie.",
        build_metadata_field_info(),
    )
    return retriever.invoke(query)


def run_self_query_examples() -> dict[str, list[Document]]:
    # Recorre las consultas ejemplo del notebook adaptado.
    return {
        prompt: retrieve_self_query_documents(prompt)
        for prompt in SELF_QUERY_PROMPTS
    }
