# --- DEPENDENCIAS ---
# 1. Sys: Para anadir la ruta del spike a los imports de prueba.
# 2. Path: Para resolver la ruta absoluta del spike.
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SPIKE = ROOT / "spikes" / "11-semantic_similarity"

if str(SPIKE) not in sys.path:
    sys.path.insert(0, str(SPIKE))

from config.faiss_similarity_config import GRAPHICS_QUERY
from config.faiss_similarity_config import MEDICAL_QUERY
from config.faiss_similarity_config import PRIMARY_QUERY
from config.faiss_similarity_config import SEMANTIC_QUERY
from config.faiss_similarity_config import SPACE_QUERY
from data.faiss_forum_posts import FORUM_POSTS
from models.faiss_semantic_embedding_gateway import build_semantic_vector
from orchestration.faiss_index_orchestration import build_semantic_faiss_lab_context
from orchestration.faiss_preprocessing_orchestration import preprocess_text
from orchestration.faiss_search_orchestration import search_semantic_posts


def test_preprocess_removes_headers_emails_and_punctuation():
    processed = preprocess_text(FORUM_POSTS[0]["text"])

    assert "from" not in processed
    assert "@" not in processed
    assert ":" not in processed
    assert "mph" in processed


def test_semantic_vector_brings_bike_query_closer_to_motorcycle_post():
    bike_query = build_semantic_vector(preprocess_text(SEMANTIC_QUERY))
    motorcycle_post = build_semantic_vector(preprocess_text(FORUM_POSTS[2]["text"]))
    space_post = build_semantic_vector(preprocess_text(FORUM_POSTS[3]["text"]))

    motorcycle_distance = np.linalg.norm(bike_query - motorcycle_post)
    space_distance = np.linalg.norm(bike_query - space_post)

    assert motorcycle_distance < space_distance


def test_faiss_index_contains_all_posts():
    context = build_semantic_faiss_lab_context()

    assert context.index.ntotal == len(FORUM_POSTS)
    assert context.embeddings.shape[0] == len(FORUM_POSTS)


def test_primary_query_returns_motorcycle_category_first():
    results = search_semantic_posts(PRIMARY_QUERY)

    assert results
    assert results[0]["category"] == "motorcycles"


def test_space_query_returns_space_category_first():
    results = search_semantic_posts(SPACE_QUERY)

    assert results
    assert results[0]["category"] == "space"


def test_graphics_and_medical_queries_return_expected_categories():
    graphics_results = search_semantic_posts(GRAPHICS_QUERY)
    medical_results = search_semantic_posts(MEDICAL_QUERY)

    assert graphics_results[0]["category"] == "graphics"
    assert medical_results[0]["category"] == "medicine"
