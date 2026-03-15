# --- DEPENDENCIAS ---
# 1. Sys: Para anadir la ruta del spike a los imports de prueba.
# 2. Path: Para resolver la ruta absoluta del spike.
import sys
from pathlib import Path

from langchain_core.documents import Document

ROOT = Path(__file__).resolve().parents[2]
SPIKE = ROOT / "spikes" / "03-rag_pdf_qa_bot_lab"

if str(SPIKE) not in sys.path:
    sys.path.insert(0, str(SPIKE))

from bootstrap.rag_bootstrap import configure_warnings
from bootstrap.rag_bootstrap import warn
from orchestration.rag_orchestration_qa import rag_qa
from orchestration.rag_orchestration_retrieval import get_rag_retriever
from pipeline.rag_document_pipeline import split_loaded_documents
from state.rag_state import runtime_state
from ui.rag_ui import build_interface


def test_configure_warnings_replaces_warn_function():
    import warnings

    original_warn = warnings.warn

    try:
        configure_warnings()
        assert warnings.warn is warn
    finally:
        warnings.warn = original_warn


def test_split_loaded_documents_creates_multiple_chunks():
    loaded_documents = [
        Document(page_content=("texto " * 400).strip(), metadata={"source": "sample.pdf"})
    ]

    chunks = split_loaded_documents(loaded_documents)

    assert len(chunks) >= 2
    assert all(chunk.page_content for chunk in chunks)


def test_get_rag_retriever_reuses_cached_retriever(monkeypatch):
    runtime_state.indexed_pdf_path = None
    runtime_state.vector_store = None
    runtime_state.rag_retriever = None

    counters = {"prepare": 0, "vector_store": 0, "retriever": 0}

    def fake_prepare_pdf_chunks(file_path):
        counters["prepare"] += 1
        return [Document(page_content=f"contenido de {file_path}")]

    def fake_build_vector_store(chunks):
        counters["vector_store"] += 1
        return {"chunks": chunks}

    def fake_build_retriever(vector_store):
        counters["retriever"] += 1
        return {"retriever": vector_store}

    monkeypatch.setattr(
        "orchestration.rag_orchestration_retrieval.prepare_pdf_chunks",
        fake_prepare_pdf_chunks,
    )
    monkeypatch.setattr(
        "orchestration.rag_orchestration_retrieval.build_vector_store",
        fake_build_vector_store,
    )
    monkeypatch.setattr(
        "orchestration.rag_orchestration_retrieval.build_retriever",
        fake_build_retriever,
    )

    first_retriever = get_rag_retriever("sample.pdf")
    second_retriever = get_rag_retriever("sample.pdf")

    assert first_retriever == second_retriever
    assert counters == {"prepare": 1, "vector_store": 1, "retriever": 1}


def test_rag_qa_validates_inputs_and_returns_chain_result(monkeypatch):
    assert rag_qa("", "pregunta") == "Carga un archivo PDF."
    assert rag_qa("sample.pdf", "   ") == "Escribe una pregunta."

    class FakeQaChain:
        def invoke(self, payload):
            assert payload == {"query": "Que dice el documento?"}
            return {"result": "respuesta grounded"}

    class FakeRetrievalQa:
        @staticmethod
        def from_chain_type(llm, chain_type, retriever, return_source_documents):
            assert llm == "fake_llm"
            assert chain_type == "stuff"
            assert retriever == "fake_retriever"
            assert return_source_documents is False
            return FakeQaChain()

    monkeypatch.setattr("orchestration.rag_orchestration_qa.get_llm", lambda: "fake_llm")
    monkeypatch.setattr(
        "orchestration.rag_orchestration_qa.get_rag_retriever",
        lambda file_path: "fake_retriever",
    )
    monkeypatch.setattr("orchestration.rag_orchestration_qa.RetrievalQA", FakeRetrievalQa)

    response = rag_qa("sample.pdf", "Que dice el documento?")

    assert response == "respuesta grounded"


def test_build_interface_returns_gradio_interface():
    rag_application = build_interface()

    assert hasattr(rag_application, "launch")
    assert rag_application.title == "RAG Chatbot"
