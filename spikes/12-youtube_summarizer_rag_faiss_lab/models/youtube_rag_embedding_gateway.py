# --- DEPENDENCIAS ---
# 1. Regex: Para tokenizar texto de forma simple.
import re

from langchain_core.embeddings import Embeddings

# --- EMBEDDINGS ---
KEYWORD_GROUPS = {
    "rag_overview": {
        "answer",
        "evidence",
        "generation",
        "ground",
        "rag",
        "retrieval",
    },
    "hallucinations": {
        "facts",
        "grounded",
        "hallucinate",
        "hallucinations",
        "precise",
        "traceable",
    },
    "knowledge_cutoff": {
        "company",
        "cutoff",
        "domain",
        "private",
        "proprietary",
        "stale",
        "training",
    },
    "chunking_embeddings": {
        "chunk",
        "chunking",
        "chunks",
        "embedding",
        "embeddings",
        "semantic",
        "vector",
    },
    "faiss_search": {
        "dense",
        "faiss",
        "index",
        "nearest",
        "search",
        "similarity",
        "vectors",
    },
    "prompt_answering": {
        "context",
        "generator",
        "material",
        "prompt",
        "question",
        "retriever",
        "response",
        "source",
    },
}


def tokenize_text(text: str) -> list[str]:
    # Convierte a minusculas y extrae tokens alfanumericos simples.
    return re.findall(r"[a-z0-9]+", text.lower())


def expand_query_tokens(tokens: list[str]) -> list[str]:
    # Amplia consultas cortas con sinonimos del dominio.
    expanded_tokens = list(tokens)

    expansion_map = {
        "faiss": ["similarity", "search", "vectors", "index"],
        "hallucinations": ["ground", "grounded", "context", "retrieve"],
        "hallucination": ["ground", "grounded", "context", "retrieve"],
        "rag": ["retrieval", "generation", "private", "cutoff"],
        "workflow": ["chunking", "embeddings", "retrieval", "index"],
        "problems": ["cutoff", "stale", "private", "proprietary"],
    }

    for token in tokens:
        expanded_tokens.extend(expansion_map.get(token, []))

    return expanded_tokens


def build_youtube_rag_vector(text: str, expand_query: bool = False) -> list[float]:
    # Cuenta señales del dominio en un vector determinista.
    tokens = tokenize_text(text)
    if expand_query:
        tokens = expand_query_tokens(tokens)

    vector = [
        float(sum(token in keywords for token in tokens))
        for keywords in KEYWORD_GROUPS.values()
    ]
    vector.append(1.0)
    return vector


class YouTubeRagKeywordEmbeddings(Embeddings):
    # Implementa embeddings compatibles con LangChain y FAISS.
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        # Genera un vector por cada chunk del transcript.
        return [build_youtube_rag_vector(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        # Reutiliza la misma logica para la consulta.
        return build_youtube_rag_vector(text, expand_query=True)


def build_youtube_rag_embeddings() -> YouTubeRagKeywordEmbeddings:
    # Devuelve una instancia lista para el vector store FAISS.
    return YouTubeRagKeywordEmbeddings()
