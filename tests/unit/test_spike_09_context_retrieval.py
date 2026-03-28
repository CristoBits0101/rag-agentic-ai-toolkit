# --- DEPENDENCIAS ---
# 1. Sys: Para anadir la ruta del spike a los imports de prueba.
# 2. Path: Para resolver la ruta absoluta del spike.
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPIKE = ROOT / "spikes" / "09-context_retrieval"

if str(SPIKE) not in sys.path:
    sys.path.insert(0, str(SPIKE))

from config.context_retrieval_config import MULTI_QUERY_QUESTION
from models.context_retrieval_demo_llm import build_context_retrieval_demo_llm
from orchestration.context_retrieval_parent_orchestration import (
    retrieve_parent_documents,
)
from orchestration.context_retrieval_search_orchestration import (
    retrieve_multi_query_documents,
)
from orchestration.context_retrieval_search_orchestration import (
    retrieve_policy_documents,
)
from orchestration.context_retrieval_self_query_orchestration import (
    retrieve_self_query_documents,
)


def patch_demo_llm(monkeypatch) -> None:
    from orchestration import context_retrieval_search_orchestration as search_orchestration
    from orchestration import context_retrieval_self_query_orchestration as self_query_orchestration

    monkeypatch.setattr(
        search_orchestration,
        "build_context_retrieval_llm",
        build_context_retrieval_demo_llm,
    )
    monkeypatch.setattr(
        self_query_orchestration,
        "build_context_retrieval_llm",
        build_context_retrieval_demo_llm,
    )


def test_similarity_retrieval_prioritizes_email_policy_chunk():
    documents = retrieve_policy_documents("email policy", search_kwargs={"k": 2})

    assert documents
    assert any("email" in document.page_content.lower() for document in documents)
    assert any("sensitive attachments" in document.page_content.lower() for document in documents)


def test_top_k_retrieval_returns_single_document():
    documents = retrieve_policy_documents("email policy", search_kwargs={"k": 1})

    assert len(documents) == 1


def test_multi_query_retrieval_returns_langchain_context(monkeypatch):
    patch_demo_llm(monkeypatch)
    documents = retrieve_multi_query_documents(MULTI_QUERY_QUESTION)

    assert documents
    assert any("LangChain" in document.page_content for document in documents)
    assert any("MultiQueryRetriever" in document.page_content for document in documents)


def test_self_query_retrieval_filters_by_director_and_topic(monkeypatch):
    patch_demo_llm(monkeypatch)
    documents = retrieve_self_query_documents(
        "Has Greta Gerwig directed any movies about women"
    )

    assert len(documents) == 1
    assert documents[0].metadata["director"] == "Greta Gerwig"
    assert "women" in documents[0].page_content.lower()


def test_self_query_retrieval_combines_rating_and_genre(monkeypatch):
    patch_demo_llm(monkeypatch)
    documents = retrieve_self_query_documents(
        "What's a highly rated science fiction film?"
    )

    assert documents
    assert all(document.metadata["rating"] > 8.5 for document in documents)
    assert documents[0].metadata["genre"] == "science fiction"


def test_parent_document_retrieval_returns_broader_context_than_child_chunk():
    child_documents, parent_documents, parent_key_count = retrieve_parent_documents()

    assert parent_key_count >= 1
    assert child_documents
    assert parent_documents
    assert "smoking" in child_documents[0].page_content.lower()
    assert len(parent_documents[0].page_content) > len(child_documents[0].page_content)
    assert "Email Policy" in parent_documents[0].page_content
