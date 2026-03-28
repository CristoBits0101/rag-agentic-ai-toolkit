# --- DEPENDENCIAS ---
from llama_index.core.retrievers import AutoMergingRetriever

from orchestration.advanced_retrievers_index_orchestration import (
    build_auto_merging_bundle,
)
from orchestration.advanced_retrievers_index_orchestration import (
    build_recursive_bundle,
)

# --- CONTEXTO ---
def retrieve_auto_merging_comparison(query: str):
    # Devuelve leaf chunks y nodos fusionados para comparar contexto.
    bundle = build_auto_merging_bundle()
    auto_merging_retriever = AutoMergingRetriever(
        bundle.leaf_retriever,
        bundle.storage_context,
        verbose=False,
    )
    leaf_nodes = bundle.leaf_retriever.retrieve(query)
    merged_nodes = auto_merging_retriever.retrieve(query)
    return leaf_nodes, merged_nodes


def retrieve_recursive_nodes(query: str):
    # Sigue referencias entre recuperadores enlazados.
    bundle = build_recursive_bundle()
    return bundle.recursive_retriever.retrieve(query)
