# --- DEPENDENCIAS ---
# 1. Configuracion: Para reutilizar la consulta de demostracion.
# 2. Colecciones: Para crear vector stores del laboratorio.
# 3. LLM Demo: Para expandir consultas en MultiQueryRetriever.
from config.context_retrieval_config import MULTI_QUERY_QUESTION
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_core.documents import Document
from models.context_retrieval_demo_llm import build_context_retrieval_demo_llm
from orchestration.context_retrieval_collection_orchestration import (
    build_policy_vectorstore,
)
from orchestration.context_retrieval_collection_orchestration import (
    build_retrieval_notes_vectorstore,
)

# --- RETRIEVAL ---
def retrieve_policy_documents(
    query: str,
    search_type: str = "similarity",
    search_kwargs: dict | None = None,
) -> list[Document]:
    # Ejecuta retrieval clasico sobre politicas de empresa.
    vectorstore, _policy_chunks = build_policy_vectorstore()
    retriever = vectorstore.as_retriever(
        search_type=search_type,
        search_kwargs=search_kwargs or {"k": 4},
    )
    return retriever.invoke(query)


def run_policy_retrieval_examples() -> dict[str, list[Document]]:
    # Ejecuta las cuatro variantes principales del notebook adaptado.
    return {
        "similarity": retrieve_policy_documents("email policy", search_kwargs={"k": 4}),
        "top_k_1": retrieve_policy_documents("email policy", search_kwargs={"k": 1}),
        "mmr": retrieve_policy_documents(
            "email policy",
            search_type="mmr",
            search_kwargs={"k": 2, "fetch_k": 4},
        ),
        "threshold": retrieve_policy_documents(
            "email policy",
            search_type="similarity_score_threshold",
            search_kwargs={"k": 3, "score_threshold": 0.15},
        ),
    }


def retrieve_multi_query_documents(
    query: str = MULTI_QUERY_QUESTION,
) -> list[Document]:
    # Expande la pregunta en varias consultas para mejorar recall.
    vectorstore, _notes_chunks = build_retrieval_notes_vectorstore()
    multi_query_retriever = MultiQueryRetriever.from_llm(
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
        llm=build_context_retrieval_demo_llm(),
    )
    return multi_query_retriever.invoke(query)
