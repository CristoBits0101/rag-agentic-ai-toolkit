# --- DEPENDENCIAS ---
# 1. Regex: Para tokenizar texto de forma simple.
# 2. Embeddings: Para cumplir la interfaz que LangChain espera.
import re

from langchain_core.embeddings import Embeddings

# --- EMBEDDINGS ---
KEYWORD_GROUPS = {
    "policy_email": {
        "attachment",
        "attachments",
        "business",
        "email",
        "mail",
        "message",
        "sending",
    },
    "policy_smoking": {
        "area",
        "breaks",
        "designated",
        "entrances",
        "smoking",
        "vaping",
    },
    "policy_remote": {
        "approval",
        "chat",
        "core",
        "home",
        "hybrid",
        "remote",
    },
    "policy_security": {
        "authentication",
        "confidential",
        "encrypted",
        "encryption",
        "laptops",
        "security",
    },
    "retrieval_langchain": {
        "chains",
        "langchain",
        "models",
        "prompts",
        "retrieval",
        "retrievers",
        "vector",
    },
    "retrieval_multi_query": {
        "alternatives",
        "different",
        "multiqueryretriever",
        "perspectives",
        "phrasings",
        "reformulation",
    },
    "retrieval_self_query": {
        "constraints",
        "directed",
        "filters",
        "metadata",
        "rating",
        "selfqueryretriever",
    },
    "retrieval_parent": {
        "child",
        "context",
        "larger",
        "parent",
        "parentdocumentretriever",
        "surrounding",
    },
    "movie_science_fiction": {
        "dinosaurs",
        "earth",
        "explorers",
        "humanity",
        "science",
        "wormhole",
    },
    "movie_dreams": {
        "dream",
        "dreams",
        "inception",
        "psychologist",
        "series",
    },
    "movie_women": {
        "affection",
        "family",
        "greta",
        "women",
        "warm",
    },
    "movie_animation": {
        "animated",
        "blast",
        "toys",
    },
    "movie_thriller": {
        "desire",
        "room",
        "thriller",
        "zone",
    },
}


def tokenize_text(text: str) -> list[str]:
    # Convierte a minusculas y extrae palabras simples.
    return re.findall(r"[a-z0-9]+", text.lower())


def build_context_retrieval_vector(text: str) -> list[float]:
    # Cuenta senales semanticas del dominio en un vector determinista.
    tokens = tokenize_text(text)
    vector = [
        float(sum(token in keywords for token in tokens))
        for keywords in KEYWORD_GROUPS.values()
    ]

    # Evita un vector nulo para no degradar la similitud.
    if not any(vector):
        return [1.0] * len(KEYWORD_GROUPS)

    return vector


class ContextRetrievalKeywordEmbeddings(Embeddings):
    # Implementa embeddings compatibles con LangChain y Chroma.
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        # Genera un vector por cada documento.
        return [build_context_retrieval_vector(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        # Reutiliza la misma logica para la consulta.
        return build_context_retrieval_vector(text)


def build_context_retrieval_embeddings() -> ContextRetrievalKeywordEmbeddings:
    # Devuelve una instancia lista para usarse en cada vector store.
    return ContextRetrievalKeywordEmbeddings()
