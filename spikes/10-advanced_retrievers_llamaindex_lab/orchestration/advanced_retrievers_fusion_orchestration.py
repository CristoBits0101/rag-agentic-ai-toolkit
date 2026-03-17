# --- DEPENDENCIAS ---
import Stemmer

from llama_index.core.base.base_retriever import BaseRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.retrievers import QueryFusionRetriever
from llama_index.core.retrievers.fusion_retriever import FUSION_MODES
from llama_index.core.schema import NodeWithScore
from llama_index.retrievers.bm25 import BM25Retriever

from config.advanced_retrievers_config import HYBRID_TOP_K
from config.advanced_retrievers_config import QUERY_FUSION_NUM_QUERIES
from config.advanced_retrievers_config import QUERY_FUSION_TOP_K
from models.advanced_retrievers_ollama_gateway import build_advanced_retrievers_llm
from orchestration.advanced_retrievers_index_orchestration import (
    build_advanced_retrievers_lab_context,
)

# --- FUSION ---
def normalize_node_scores(nodes: list[NodeWithScore]) -> dict[str, float]:
    # Normaliza scores en el rango cero a uno.
    if not nodes:
        return {}

    scores = [node.score or 0.0 for node in nodes]
    min_score = min(scores)
    max_score = max(scores)

    if max_score == min_score:
        return {node.node.node_id: 1.0 for node in nodes}

    return {
        node.node.node_id: ((node.score or 0.0) - min_score) / (max_score - min_score)
        for node in nodes
    }


class WeightedHybridRetriever(BaseRetriever):
    # Combina retrieval vectorial y BM25 con pesos simples.
    def __init__(
        self,
        vector_retriever,
        bm25_retriever,
        vector_weight: float = 0.6,
        keyword_weight: float = 0.4,
        similarity_top_k: int = HYBRID_TOP_K,
    ) -> None:
        self._vector_retriever = vector_retriever
        self._bm25_retriever = bm25_retriever
        self._vector_weight = vector_weight
        self._keyword_weight = keyword_weight
        self._similarity_top_k = similarity_top_k
        super().__init__()

    def _retrieve(self, query_bundle):
        # Fusiona resultados normalizados de ambos recuperadores.
        vector_nodes = self._vector_retriever.retrieve(query_bundle)
        bm25_nodes = self._bm25_retriever.retrieve(query_bundle)
        vector_scores = normalize_node_scores(vector_nodes)
        bm25_scores = normalize_node_scores(bm25_nodes)
        merged = {}

        for node in vector_nodes:
            merged[node.node.node_id] = NodeWithScore(
                node=node.node,
                score=(vector_scores.get(node.node.node_id, 0.0) * self._vector_weight),
            )

        for node in bm25_nodes:
            node_id = node.node.node_id
            weighted_score = bm25_scores.get(node_id, 0.0) * self._keyword_weight
            if node_id in merged:
                merged[node_id].score = (merged[node_id].score or 0.0) + weighted_score
            else:
                merged[node_id] = NodeWithScore(node=node.node, score=weighted_score)

        ranked_nodes = sorted(
            merged.values(),
            key=lambda item: item.score or 0.0,
            reverse=True,
        )
        return ranked_nodes[: self._similarity_top_k]


def build_hybrid_retriever() -> WeightedHybridRetriever:
    # Construye el recuperador hibrido del ejercicio.
    lab = build_advanced_retrievers_lab_context()
    vector_retriever = lab.vector_index.as_retriever(similarity_top_k=HYBRID_TOP_K)
    bm25_retriever = BM25Retriever.from_defaults(
        nodes=lab.nodes,
        similarity_top_k=HYBRID_TOP_K,
        stemmer=Stemmer.Stemmer("english"),
        language="english",
    )
    return WeightedHybridRetriever(vector_retriever, bm25_retriever)


def resolve_fusion_mode(mode_name: str):
    # Traduce nombres del laboratorio a enums reales.
    mode_map = {
        "reciprocal_rerank": FUSION_MODES.RECIPROCAL_RANK,
        "relative_score": FUSION_MODES.RELATIVE_SCORE,
        "dist_based_score": FUSION_MODES.DIST_BASED_SCORE,
    }
    return mode_map[mode_name]


def retrieve_query_fusion_nodes(query: str, mode_name: str):
    # Ejecuta QueryFusionRetriever con el modo indicado.
    lab = build_advanced_retrievers_lab_context()
    retriever = QueryFusionRetriever(
        [lab.vector_index.as_retriever(similarity_top_k=QUERY_FUSION_TOP_K + 2)],
        llm=build_advanced_retrievers_llm(),
        similarity_top_k=QUERY_FUSION_TOP_K,
        num_queries=QUERY_FUSION_NUM_QUERIES,
        mode=resolve_fusion_mode(mode_name),
        use_async=False,
        verbose=False,
    )
    return retriever.retrieve(query)


def retrieve_hybrid_nodes(query: str):
    # Devuelve resultados del recuperador hibrido del ejercicio.
    return build_hybrid_retriever().retrieve(query)


def run_production_rag_pipeline(query: str) -> str:
    # Ejecuta un query engine sencillo sobre el recuperador hibrido.
    query_engine = RetrieverQueryEngine.from_args(
        retriever=build_hybrid_retriever(),
        llm=build_advanced_retrievers_llm(),
        use_async=False,
    )
    response = query_engine.query(query)
    return str(response)
