# --- DEPENDENCIAS ---
# 1. Sys: Para anadir la ruta del spike a los imports de prueba.
# 2. Path: Para resolver la ruta absoluta del spike.
# 3. Numpy: Para validar embeddings deterministas del laboratorio.
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SPIKE = ROOT / "spikes" / "06-chromadb_cheat_sheet"

if str(SPIKE) not in sys.path:
    sys.path.insert(0, str(SPIKE))

from data.chromadb_demo_dataset import COMPLEX_METADATA_FILTER
from data.chromadb_demo_dataset import CRUD_DEMO_ITEM
from data.chromadb_demo_dataset import DOCUMENT_FILTER
from data.chromadb_demo_dataset import METADATA_FILTER
from models.chromadb_keyword_embedding_gateway import build_keyword_embedding
from orchestration.chromadb_collection_orchestration import add_crud_demo_item
from orchestration.chromadb_collection_orchestration import bootstrap_demo_collection
from orchestration.chromadb_collection_orchestration import delete_crud_demo_item
from orchestration.chromadb_collection_orchestration import modify_collection_metadata
from orchestration.chromadb_collection_orchestration import update_crud_demo_item
from orchestration.chromadb_query_orchestration import get_documents_by_id
from orchestration.chromadb_query_orchestration import get_documents_with_document_filter
from orchestration.chromadb_query_orchestration import (
    get_documents_with_metadata_filter,
)
from orchestration.chromadb_query_orchestration import query_by_text


def test_build_keyword_embedding_detects_animal_signal():
    animal_embedding = build_keyword_embedding("polar bears and pandas in the arctic")
    animal_reference = build_keyword_embedding("arctic wildlife and polar bear habitat")
    tech_reference = build_keyword_embedding("python programming dataframes and backend services")

    assert isinstance(animal_embedding, np.ndarray)
    assert animal_embedding.ndim == 1
    assert animal_embedding.size > 0
    assert np.isfinite(animal_embedding).all()
    assert float(np.dot(animal_embedding, animal_reference)) > float(
        np.dot(animal_embedding, tech_reference)
    )


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


def test_collection_crud_flow_supports_add_update_and_delete():
    collection = bootstrap_demo_collection()

    modify_collection_metadata(
        collection,
        {"topic": "query testing", "mode": "cheat sheet", "domain": "rag"},
    )
    add_crud_demo_item(collection)
    created = get_documents_by_id(collection, [CRUD_DEMO_ITEM["id"]])

    assert created["ids"] == [CRUD_DEMO_ITEM["id"]]
    assert created["documents"] == [CRUD_DEMO_ITEM["document"]]
    assert collection.metadata["domain"] == "rag"

    updated_document, updated_metadata = update_crud_demo_item(collection)
    updated = get_documents_by_id(collection, [CRUD_DEMO_ITEM["id"]])

    assert updated["documents"] == [updated_document]
    assert updated["metadatas"] == [updated_metadata]

    delete_crud_demo_item(collection)
    deleted = get_documents_by_id(collection, [CRUD_DEMO_ITEM["id"]])

    assert deleted["ids"] == []
