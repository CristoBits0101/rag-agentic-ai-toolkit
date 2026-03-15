# --- DEPENDENCIAS ---
# 1. Sys: Para anadir la ruta del spike a los imports de prueba.
# 2. Path: Para resolver la ruta absoluta del spike.
# 3. Numpy: Para validar embeddings deterministas del laboratorio.
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SPIKE = ROOT / "spikes" / "06-vector_databases_chromadb_cheat_sheet_lab"

if str(SPIKE) not in sys.path:
    sys.path.insert(0, str(SPIKE))

from data.chromadb_demo_dataset import COMPLEX_METADATA_FILTER
from data.chromadb_demo_dataset import DOCUMENT_FILTER
from data.chromadb_demo_dataset import METADATA_FILTER
from models.chromadb_keyword_embedding_gateway import build_keyword_embedding
from orchestration.chromadb_collection_orchestration import bootstrap_demo_collection
from orchestration.chromadb_query_orchestration import get_documents_with_document_filter
from orchestration.chromadb_query_orchestration import (
    get_documents_with_metadata_filter,
)
from orchestration.chromadb_query_orchestration import query_by_text


def test_build_keyword_embedding_detects_animal_signal():
    embedding = build_keyword_embedding("polar bears and pandas in the arctic")

    assert isinstance(embedding, np.ndarray)
    assert embedding[0] > embedding[1]
    assert embedding[0] > embedding[2]


def test_metadata_filter_returns_only_animal_documents():
    collection = bootstrap_demo_collection()

    result = get_documents_with_metadata_filter(collection, METADATA_FILTER)

    assert result["ids"] == ["doc_1", "doc_2"]


def test_complex_metadata_filter_returns_langchain_and_llamaindex_docs():
    collection = bootstrap_demo_collection()

    result = get_documents_with_metadata_filter(collection, COMPLEX_METADATA_FILTER)

    assert result["ids"] == ["doc_3", "doc_4"]


def test_document_filter_is_case_sensitive_for_pandas():
    collection = bootstrap_demo_collection()

    result = get_documents_with_document_filter(collection, DOCUMENT_FILTER)

    assert result["ids"] == ["doc_2"]


def test_similarity_query_returns_polar_bear_document_first():
    collection = bootstrap_demo_collection()

    result = query_by_text(
        collection,
        "Which document talks about polar bears and Arctic wildlife?",
        n_results=1,
    )

    assert result["ids"][0][0] == "doc_1"
