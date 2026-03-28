# --- DEPENDENCIAS ---
import Stemmer

from llama_index.core.indices.document_summary import (
    DocumentSummaryIndexEmbeddingRetriever,
)
from llama_index.core.indices.document_summary import DocumentSummaryIndexLLMRetriever
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.retrievers.bm25 import BM25Retriever

from orchestration.advanced_retrievers_index_orchestration import (
    build_advanced_retrievers_lab_context,
)

# --- RETRIEVAL ---
def retrieve_vector_nodes(query: str, similarity_top_k: int = 3):
    # Recupera nodos por similitud semantica.
    lab = build_advanced_retrievers_lab_context()
    retriever = VectorIndexRetriever(
        index=lab.vector_index,
        similarity_top_k=similarity_top_k,
    )
    return retriever.retrieve(query)


def retrieve_bm25_nodes(query: str, similarity_top_k: int = 3):
    # Recupera nodos por ranking BM25.
    lab = build_advanced_retrievers_lab_context()
    retriever = BM25Retriever.from_defaults(
        nodes=lab.nodes,
        similarity_top_k=similarity_top_k,
        stemmer=Stemmer.Stemmer("english"),
        language="english",
    )
    return retriever.retrieve(query)


def retrieve_document_summary_llm_nodes(query: str, choice_top_k: int = 3):
    # Recupera documentos usando seleccion de resumenes con LLM.
    lab = build_advanced_retrievers_lab_context()
    retriever = DocumentSummaryIndexLLMRetriever(
        lab.document_summary_index,
        choice_top_k=choice_top_k,
    )
    return retriever.retrieve(query)


def retrieve_document_summary_embedding_nodes(
    query: str,
    similarity_top_k: int = 3,
):
    # Recupera documentos usando similitud sobre resumenes.
    lab = build_advanced_retrievers_lab_context()
    retriever = DocumentSummaryIndexEmbeddingRetriever(
        lab.document_summary_index,
        similarity_top_k=similarity_top_k,
    )
    return retriever.retrieve(query)
