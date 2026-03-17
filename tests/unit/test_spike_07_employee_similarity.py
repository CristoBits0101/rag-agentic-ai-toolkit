# --- DEPENDENCIAS ---
# 1. Sys: Para anadir la ruta del spike a los imports de prueba.
# 2. Path: Para resolver la ruta absoluta del spike.
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPIKE = ROOT / "spikes" / "07-employee_similarity_search_chromadb_lab"

if str(SPIKE) not in sys.path:
    sys.path.insert(0, str(SPIKE))

from orchestration.book_collection_orchestration import bootstrap_book_collection
from orchestration.book_search_orchestration import get_fantasy_and_science_fiction_books
from orchestration.book_search_orchestration import search_highly_rated_dystopian_books
from orchestration.book_search_orchestration import search_magical_fantasy_adventures
from orchestration.employee_collection_orchestration import bootstrap_employee_collection
from orchestration.employee_search_orchestration import get_california_employees
from orchestration.employee_search_orchestration import get_engineering_employees
from orchestration.employee_search_orchestration import get_senior_employees
from orchestration.employee_search_orchestration import search_empty_employee_case
from orchestration.employee_search_orchestration import search_python_developers


def test_employee_collection_contains_fifteen_documents():
    collection = bootstrap_employee_collection()
    items = collection.get()

    assert len(items["documents"]) == 15


def test_python_developer_query_returns_john_doe_first():
    collection = bootstrap_employee_collection()
    results = search_python_developers(collection)

    assert "employee_1" in results["ids"][0][:3]


def test_employee_filters_match_expected_counts():
    collection = bootstrap_employee_collection()

    assert len(get_engineering_employees(collection)["ids"]) == 8
    assert len(get_senior_employees(collection)["ids"]) == 6
    assert len(get_california_employees(collection)["ids"]) == 3


def test_empty_employee_case_returns_no_results():
    collection = bootstrap_employee_collection()
    results = search_empty_employee_case(collection)

    assert results["ids"] == [[]]


def test_book_fantasy_query_returns_harry_potter_first():
    collection = bootstrap_book_collection()
    results = search_magical_fantasy_adventures(collection)

    assert results["ids"][0][0] == "book_4"


def test_book_filters_and_dystopian_search_match_expected_results():
    collection = bootstrap_book_collection()
    genre_results = get_fantasy_and_science_fiction_books(collection)
    dystopian_results = search_highly_rated_dystopian_books(collection)

    assert len(genre_results["ids"]) == 4
    assert dystopian_results["ids"][0][0] == "book_3"
