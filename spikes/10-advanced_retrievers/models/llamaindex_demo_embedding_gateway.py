# --- DEPENDENCIAS ---
# 1. Regex: Para tokenizar texto de forma simple.
import re

from llama_index.core.base.embeddings.base import BaseEmbedding

# --- EMBEDDINGS ---
KEYWORD_GROUPS = {
    "ml_basics": {
        "artificial",
        "classification",
        "data",
        "forecasting",
        "intelligence",
        "learning",
        "machine",
        "patterns",
        "recommendation",
        "regression",
    },
    "deep_learning": {
        "backpropagation",
        "deep",
        "gradient",
        "hidden",
        "layered",
        "layers",
        "neural",
        "network",
        "networks",
        "weights",
    },
    "nlp": {
        "assistants",
        "chatbots",
        "document",
        "language",
        "nlp",
        "search",
        "summarize",
        "text",
        "translate",
    },
    "computer_vision": {
        "classification",
        "detection",
        "frames",
        "image",
        "imaging",
        "inspection",
        "pixels",
        "scenes",
        "video",
        "vision",
    },
    "reinforcement_learning": {
        "agents",
        "control",
        "decisions",
        "penalties",
        "policies",
        "reinforcement",
        "rewards",
        "robotics",
        "sequential",
    },
    "supervised_learning": {
        "classification",
        "examples",
        "labeled",
        "outputs",
        "prediction",
        "regression",
        "spam",
        "supervised",
    },
    "unsupervised_learning": {
        "anomaly",
        "clustering",
        "dimensionality",
        "discovery",
        "reduction",
        "segmentation",
        "structure",
        "topic",
        "unlabeled",
        "unsupervised",
    },
    "transfer_learning": {
        "adaptation",
        "pretrained",
        "reuse",
        "speech",
        "tasks",
        "transfer",
        "vision",
    },
    "generative_ai": {
        "code",
        "content",
        "creates",
        "generation",
        "generative",
        "images",
        "media",
        "synthetic",
    },
    "llm": {
        "answering",
        "corpora",
        "language",
        "large",
        "llm",
        "massive",
        "models",
        "question",
        "reasoning",
        "summarization",
    },
    "retrieval": {
        "bm25",
        "fusion",
        "hybrid",
        "keyword",
        "query",
        "ranking",
        "retrieval",
        "semantic",
        "summary",
        "vector",
    },
    "applications": {
        "analytics",
        "applications",
        "automation",
        "business",
        "customers",
        "enterprise",
        "support",
        "systems",
        "translation",
        "workflows",
    },
}


def tokenize_text(text: str) -> list[str]:
    # Convierte a minusculas y extrae palabras alfanumericas.
    return re.findall(r"[a-z0-9]+", text.lower())


def build_demo_vector(text: str) -> list[float]:
    # Cuenta senales del dominio y anade un sesgo estable.
    tokens = tokenize_text(text)
    vector = [
        float(sum(token in keywords for token in tokens))
        for keywords in KEYWORD_GROUPS.values()
    ]
    vector.append(1.0)
    return vector


class AdvancedRetrieversDemoEmbedding(BaseEmbedding):
    # Implementa embeddings deterministas compatibles con LlamaIndex.
    model_name: str = "advanced_retrievers_demo_embedding"

    def _get_query_embedding(self, query: str) -> list[float]:
        # Genera el embedding de una consulta.
        return build_demo_vector(query)

    async def _aget_query_embedding(self, query: str) -> list[float]:
        # Reutiliza la misma logica para el flujo asincrono.
        return self._get_query_embedding(query)

    def _get_text_embedding(self, text: str) -> list[float]:
        # Genera el embedding de un texto.
        return build_demo_vector(text)

    def _get_text_embeddings(self, texts: list[str]) -> list[list[float]]:
        # Procesa varios textos en lote.
        return [build_demo_vector(text) for text in texts]


def build_advanced_retrievers_demo_embedding() -> AdvancedRetrieversDemoEmbedding:
    # Devuelve una instancia lista para indexacion y retrieval.
    return AdvancedRetrieversDemoEmbedding()
