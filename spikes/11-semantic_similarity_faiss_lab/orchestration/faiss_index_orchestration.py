# --- DEPENDENCIAS ---
# 1. Dataclass: Para transportar el estado del laboratorio.
# 2. Functools: Para cachear la construccion del indice.
from dataclasses import dataclass
from functools import lru_cache

import faiss
import numpy as np

from data.faiss_forum_posts import FORUM_POSTS
from models.faiss_semantic_embedding_gateway import embed_texts
from orchestration.faiss_preprocessing_orchestration import preprocess_text

# --- INDICE ---
@dataclass(frozen=True)
class SemanticFaissLabContext:
    raw_posts: list[dict[str, str]]
    processed_documents: list[str]
    embeddings: np.ndarray
    index: faiss.IndexFlatL2


@lru_cache(maxsize=1)
def build_semantic_faiss_lab_context() -> SemanticFaissLabContext:
    # Preprocesa el corpus genera embeddings y construye el indice FAISS.
    raw_posts = list(FORUM_POSTS)
    processed_documents = [preprocess_text(post["text"]) for post in raw_posts]
    embeddings = embed_texts(processed_documents)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return SemanticFaissLabContext(
        raw_posts=raw_posts,
        processed_documents=processed_documents,
        embeddings=embeddings,
        index=index,
    )
