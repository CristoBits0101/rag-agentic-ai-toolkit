# --- DEPENDENCIAS ---
# 1. Regex: Para tokenizar texto de forma simple.
# 2. Numpy: Para devolver embeddings listos para ChromaDB.
import re

import numpy as np

# --- EMBEDDINGS ---
# 1.1. Diccionario de palabras clave por dominio semantico.
KEYWORD_GROUPS = {
    "animals_general": {
        "animal",
        "animals",
        "arctic",
        "bear",
        "bears",
        "habitat",
        "hunt",
        "live",
        "panda",
        "pandas",
        "polar",
        "seal",
        "seals",
        "wildlife",
        "zoo",
    },
    "tech": {
        "agent",
        "agents",
        "chromadb",
        "document",
        "documents",
        "framework",
        "langchain",
        "llamaindex",
        "metadata",
        "python",
        "query",
        "rag",
        "recommend",
        "recommendation",
        "recommendations",
        "retrieve",
        "retrieval",
        "search",
        "similar",
        "suggest",
        "products",
        "content",
        "vector",
        "workflows",
    },
    "geo": {
        "fleet",
        "geo",
        "geospatial",
        "gps",
        "live",
        "maps",
        "route",
        "routing",
        "traffic",
        "updates",
    },
    "polar_animals": {
        "arctic",
        "bear",
        "bears",
        "ice",
        "polar",
        "seal",
        "seals",
    },
    "panda_animals": {
        "bamboo",
        "foraging",
        "panda",
        "pandas",
    },
}


# 1.2. Funcion para tokenizar un texto de entrada.
def tokenize_text(text: str) -> list[str]:
    # Convierte a minusculas y extrae solo palabras simples.
    return re.findall(r"[a-z0-9]+", text.lower())


# 1.3. Funcion para crear un embedding determinista desde palabras clave.
def build_keyword_embedding(text: str) -> np.ndarray:
    # Tokeniza el texto antes de contar dominios semanticos.
    tokens = tokenize_text(text)
    vector = np.array(
        [
            float(sum(token in KEYWORD_GROUPS["animals_general"] for token in tokens)),
            float(sum(token in KEYWORD_GROUPS["tech"] for token in tokens)),
            float(sum(token in KEYWORD_GROUPS["geo"] for token in tokens)),
            float(sum(token in KEYWORD_GROUPS["polar_animals"] for token in tokens)),
            float(sum(token in KEYWORD_GROUPS["panda_animals"] for token in tokens)),
        ],
        dtype=np.float32,
    )

    # Evita vectores nulos para no degradar la similitud coseno.
    if not vector.any():
        return np.ones(5, dtype=np.float32)

    # Devuelve el embedding como vector Numpy.
    return vector


# 1.4. Funcion para crear embeddings para una lista de textos.
def build_keyword_embeddings(texts: list[str]) -> list[list[float]]:
    # Devuelve cada embedding en formato serializable para ChromaDB.
    return [build_keyword_embedding(text).tolist() for text in texts]
