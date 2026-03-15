# --- DEPENDENCIAS ---
# 1. Sys: Para anadir la ruta del spike a los imports de prueba.
# 2. Path: Para resolver la ruta absoluta del spike.
# 3. Numpy: Para validar calculos matriciales del laboratorio.
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SPIKE = ROOT / "spikes" / "05-similarity_search_by_hand_lab"

if str(SPIKE) not in sys.path:
    sys.path.insert(0, str(SPIKE))

from orchestration.similarity_metrics_orchestration import build_cosine_similarity_matrix
from orchestration.similarity_metrics_orchestration import (
    build_cosine_similarity_matrix_operator,
)
from orchestration.similarity_metrics_orchestration import build_dot_product_matrix
from orchestration.similarity_metrics_orchestration import (
    build_dot_product_matrix_operator,
)
from orchestration.similarity_metrics_orchestration import build_l2_distance_matrix
from orchestration.similarity_metrics_orchestration import (
    build_l2_distance_matrix_improved,
)
from orchestration.similarity_metrics_orchestration import euclidean_distance_fn
from orchestration.similarity_metrics_orchestration import normalize_embeddings_manual
from orchestration.similarity_metrics_orchestration import verify_normalized_embeddings
from orchestration.similarity_search_orchestration import search_with_query_embedding


def test_euclidean_distance_fn_matches_expected_value():
    distance = euclidean_distance_fn(np.array([0.0, 0.0]), np.array([3.0, 4.0]))

    assert distance == 5.0


def test_improved_l2_matrix_matches_full_matrix():
    embeddings = np.array(
        [
            [1.0, 0.0],
            [0.0, 1.0],
            [1.0, 1.0],
        ]
    )

    assert np.allclose(
        build_l2_distance_matrix(embeddings),
        build_l2_distance_matrix_improved(embeddings),
    )


def test_dot_product_operator_matches_manual_matrix():
    embeddings = np.array(
        [
            [1.0, 2.0],
            [3.0, 4.0],
        ]
    )

    assert np.allclose(
        build_dot_product_matrix(embeddings),
        build_dot_product_matrix_operator(embeddings),
    )


def test_normalize_embeddings_manual_returns_unit_vectors():
    embeddings = np.array(
        [
            [3.0, 4.0],
            [5.0, 12.0],
        ]
    )
    normalized_embeddings = normalize_embeddings_manual(embeddings)

    assert np.allclose(
        verify_normalized_embeddings(normalized_embeddings),
        np.array([1.0, 1.0]),
    )


def test_cosine_similarity_operator_matches_manual_matrix():
    embeddings = np.array(
        [
            [1.0, 0.0],
            [0.0, 1.0],
            [1.0, 1.0],
        ]
    )
    normalized_embeddings = normalize_embeddings_manual(embeddings)

    assert np.allclose(
        build_cosine_similarity_matrix(normalized_embeddings),
        build_cosine_similarity_matrix_operator(normalized_embeddings),
    )


def test_search_with_query_embedding_returns_best_matching_document():
    documents = ["developer bug fixing", "insect study", "database migration"]
    normalized_document_embeddings = np.array(
        [
            [1.0, 0.0],
            [0.0, 1.0],
            [0.6, 0.4],
        ]
    )
    normalized_query_embedding = np.array([[1.0, 0.0]])

    result = search_with_query_embedding(
        documents,
        normalized_document_embeddings,
        normalized_query_embedding,
    )

    assert result["best_match_index"] == 0
    assert result["best_match_document"] == "developer bug fixing"
