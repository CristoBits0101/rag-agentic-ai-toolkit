# --- DEPENDENCIAS ---
from config.advanced_retrievers_config import ADVANCED_QUERY
from config.advanced_retrievers_config import APPLICATIONS_QUERY
from config.advanced_retrievers_config import COMPREHENSIVE_QUERY
from config.advanced_retrievers_config import LEARNING_TYPES_QUERY
from config.advanced_retrievers_config import SAMPLE_QUERY
from config.advanced_retrievers_config import TECHNICAL_QUERY
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
from orchestration.advanced_retrievers_index_orchestration import (
    build_advanced_retrievers_lab_context,
)

# --- RUNNER ---
def print_section(title: str):
    # Separa visualmente cada seccion del laboratorio.
    print(f"\n=== {title} ===")


def format_node(node_with_score) -> str:
    # Compacta score metadatos y contenido en una sola linea.
    text = " ".join(node_with_score.node.get_content().split())[:150]
    metadata = node_with_score.node.metadata
    metadata_text = " | ".join(f"{key}: {value}" for key, value in metadata.items())
    score = node_with_score.score
    if score is None:
        return f"{metadata_text} | {text}"
    return f"score: {score:.4f} | {metadata_text} | {text}"


def print_nodes(nodes):
    # Imprime la lista de resultados recuperados.
    if not nodes:
        print("No nodes found.")
        return

    for index, node in enumerate(nodes, start=1):
        print(f"{index}. {format_node(node)}")


def run_advanced_retrievers_llamaindex_lab():
    # Ejecuta las demostraciones principales del laboratorio.
    lab = build_advanced_retrievers_lab_context()
    print("Practica 10 Explore Advanced Retrievers In LlamaIndex")

    print_section("Background")
    print(f"Documentos cargados: {len(lab.documents)}")
    print(f"Nodos creados: {len(lab.nodes)}")
    print("Indices disponibles: VectorStoreIndex DocumentSummaryIndex KeywordTableIndex")

    print_section("Vector Index Retriever")
    print(f"Query: {SAMPLE_QUERY}")
    print_nodes(retrieve_vector_nodes(SAMPLE_QUERY))

    print_section("BM25 Retriever")
    print(f"Query: {TECHNICAL_QUERY}")
    print_nodes(retrieve_bm25_nodes(TECHNICAL_QUERY))

    print_section("Document Summary Index Retrievers")
    print(f"Query: {LEARNING_TYPES_QUERY}")
    print("\nLLM Retriever.")
    print_nodes(retrieve_document_summary_llm_nodes(LEARNING_TYPES_QUERY))
    print("\nEmbedding Retriever.")
    print_nodes(retrieve_document_summary_embedding_nodes(LEARNING_TYPES_QUERY))

    print_section("Auto Merging Retriever")
    print(f"Query: {ADVANCED_QUERY}")
    leaf_nodes, merged_nodes = retrieve_auto_merging_comparison(ADVANCED_QUERY)
    print("\nLeaf chunks.")
    print_nodes(leaf_nodes[:3])
    print("\nMerged parents.")
    print_nodes(merged_nodes[:3])

    print_section("Recursive Retriever")
    print(f"Query: {APPLICATIONS_QUERY}")
    print_nodes(retrieve_recursive_nodes(APPLICATIONS_QUERY))

    print_section("Query Fusion Retriever")
    print(f"Query: {COMPREHENSIVE_QUERY}")
    for mode_name in [
        "reciprocal_rerank",
        "relative_score",
        "dist_based_score",
    ]:
        print(f"\nMode: {mode_name}")
        print_nodes(retrieve_query_fusion_nodes(COMPREHENSIVE_QUERY, mode_name))

    print_section("Exercise 1 Hybrid Retriever")
    print(f"Query: {COMPREHENSIVE_QUERY}")
    print_nodes(retrieve_hybrid_nodes(COMPREHENSIVE_QUERY))

    print_section("Exercise 2 Production RAG Pipeline")
    print(f"Query: {COMPREHENSIVE_QUERY}")
    print(run_production_rag_pipeline(COMPREHENSIVE_QUERY))
