# --- DEPENDENCIAS ---
# 1. Sys: Para anadir la ruta del spike a los imports de prueba.
# 2. Path: Para resolver la ruta absoluta del spike.
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPIKE = ROOT / "spikes" / "10-advanced_retrievers_llamaindex_lab"

if str(SPIKE) not in sys.path:
    sys.path.insert(0, str(SPIKE))

from config.advanced_retrievers_config import ADVANCED_QUERY
from config.advanced_retrievers_config import APPLICATIONS_QUERY
from config.advanced_retrievers_config import COMPREHENSIVE_QUERY
from config.advanced_retrievers_config import LEARNING_TYPES_QUERY
from config.advanced_retrievers_config import SAMPLE_QUERY
from config.advanced_retrievers_config import TECHNICAL_QUERY
from models.advanced_retrievers_demo_llm import build_advanced_retrievers_demo_llm
from models.llamaindex_demo_embedding_gateway import (
    build_advanced_retrievers_demo_embedding,
)
from orchestration.advanced_retrievers_context_orchestration import (
    retrieve_auto_merging_comparison,
)
from orchestration.advanced_retrievers_context_orchestration import (
    retrieve_recursive_nodes,
)
from orchestration.advanced_retrievers_core_orchestration import (
    retrieve_bm25_nodes,
)
from orchestration.advanced_retrievers_core_orchestration import (
    retrieve_document_summary_embedding_nodes,
)
from orchestration.advanced_retrievers_core_orchestration import (
    retrieve_document_summary_llm_nodes,
)
from orchestration.advanced_retrievers_core_orchestration import (
    retrieve_vector_nodes,
)
from orchestration.advanced_retrievers_fusion_orchestration import (
    retrieve_hybrid_nodes,
)
from orchestration.advanced_retrievers_fusion_orchestration import (
    retrieve_query_fusion_nodes,
)
from orchestration.advanced_retrievers_fusion_orchestration import (
    run_production_rag_pipeline,
)


def patch_demo_models(monkeypatch) -> None:
    from orchestration import advanced_retrievers_fusion_orchestration as fusion_orchestration
    from orchestration import advanced_retrievers_index_orchestration as index_orchestration

    monkeypatch.setattr(
        index_orchestration,
        "build_advanced_retrievers_llm",
        build_advanced_retrievers_demo_llm,
    )
    monkeypatch.setattr(
        index_orchestration,
        "build_advanced_retrievers_embedding",
        build_advanced_retrievers_demo_embedding,
    )
    monkeypatch.setattr(
        fusion_orchestration,
        "build_advanced_retrievers_llm",
        build_advanced_retrievers_demo_llm,
    )
    index_orchestration.build_advanced_retrievers_lab_context.cache_clear()
    index_orchestration.build_auto_merging_bundle.cache_clear()
    index_orchestration.build_recursive_bundle.cache_clear()


def test_vector_retriever_prioritizes_machine_learning_foundation():
    nodes = retrieve_vector_nodes(SAMPLE_QUERY)

    assert nodes
    assert "Machine learning is a branch of artificial intelligence" in nodes[0].text


def test_bm25_retriever_prioritizes_neural_networks_document():
    nodes = retrieve_bm25_nodes(TECHNICAL_QUERY)

    assert nodes
    assert "neural networks" in nodes[0].text.lower()
    assert "deep learning" in nodes[0].text.lower()


def test_document_summary_retrievers_return_learning_type_documents(monkeypatch):
    patch_demo_models(monkeypatch)
    llm_nodes = retrieve_document_summary_llm_nodes(LEARNING_TYPES_QUERY)
    embedding_nodes = retrieve_document_summary_embedding_nodes(LEARNING_TYPES_QUERY)

    assert llm_nodes
    assert embedding_nodes
    assert any("supervised learning" in node.text.lower() for node in llm_nodes)
    assert any(
        keyword in " ".join(node.text.lower() for node in embedding_nodes)
        for keyword in [
            "supervised learning",
            "unsupervised learning",
            "reinforcement learning",
        ]
    )


def test_auto_merging_returns_broader_parent_context(monkeypatch):
    patch_demo_models(monkeypatch)
    leaf_nodes, merged_nodes = retrieve_auto_merging_comparison(ADVANCED_QUERY)

    assert leaf_nodes
    assert merged_nodes
    assert "neural networks" in leaf_nodes[0].text.lower()
    assert len(merged_nodes[0].text) > len(leaf_nodes[0].text)
    assert "backpropagation" in merged_nodes[0].text.lower()


def test_recursive_retriever_follows_application_references(monkeypatch):
    patch_demo_models(monkeypatch)
    nodes = retrieve_recursive_nodes(APPLICATIONS_QUERY)

    assert nodes
    combined_text = " ".join(node.text.lower() for node in nodes)
    assert "applications" in combined_text
    assert "assistants" in combined_text or "computer vision" in combined_text


def test_query_fusion_and_hybrid_retrieval_cover_learning_paradigms(monkeypatch):
    patch_demo_models(monkeypatch)
    fusion_nodes = retrieve_query_fusion_nodes(COMPREHENSIVE_QUERY, "reciprocal_rerank")
    hybrid_nodes = retrieve_hybrid_nodes(COMPREHENSIVE_QUERY)

    assert fusion_nodes
    assert hybrid_nodes
    fusion_text = " ".join(node.text.lower() for node in fusion_nodes)
    hybrid_text = " ".join(node.text.lower() for node in hybrid_nodes)
    assert "supervised learning" in fusion_text or "reinforcement learning" in fusion_text
    assert "hybrid retrieval" in hybrid_text or "supervised learning" in hybrid_text


def test_production_rag_pipeline_returns_grounded_answer(monkeypatch):
    patch_demo_models(monkeypatch)
    answer = run_production_rag_pipeline(COMPREHENSIVE_QUERY)

    assert answer
    assert "learning" in answer.lower()
    assert any(
        keyword in answer.lower()
        for keyword in ["supervised", "unsupervised", "reinforcement", "transfer"]
    )
