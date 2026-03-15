# --- DEPENDENCIAS ---
# 1. Sys: Para anadir la ruta del spike a los imports de prueba.
# 2. Path: Para resolver la ruta absoluta del spike.
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPIKE = ROOT / "spikes" / "08-food_recommendation_systems_chromadb_rag_lab"

if str(SPIKE) not in sys.path:
    sys.path.insert(0, str(SPIKE))

from orchestration.food_collection_orchestration import bootstrap_food_collection
from orchestration.food_rag_orchestration import compare_food_queries
from orchestration.food_rag_orchestration import generate_food_rag_response
from orchestration.food_search_orchestration import perform_filtered_similarity_search
from orchestration.food_search_orchestration import perform_similarity_search
from pipeline.food_data_pipeline import load_food_data


def test_load_food_data_normalizes_ids_and_taste_profile():
    food_items = load_food_data()

    assert len(food_items) >= 16
    assert all(isinstance(item["food_id"], str) for item in food_items)
    assert all("taste_profile" in item for item in food_items)


def test_similarity_search_returns_chocolate_lava_cake_first():
    collection, _food_items = bootstrap_food_collection()

    results = perform_similarity_search(collection, "chocolate dessert", 3)

    assert results[0]["food_name"] == "Chocolate Lava Cake"


def test_filtered_search_respects_cuisine_filter():
    collection, _food_items = bootstrap_food_collection()

    results = perform_filtered_similarity_search(
        collection,
        "creamy pasta",
        cuisine_filter="Italian",
        n_results=3,
    )

    assert results[0]["food_name"] == "Creamy Pasta Primavera"
    assert all(result["cuisine_type"] == "Italian" for result in results)


def test_filtered_search_respects_calorie_limit():
    collection, _food_items = bootstrap_food_collection()

    results = perform_filtered_similarity_search(
        collection,
        "healthy meal",
        max_calories=300,
        n_results=5,
    )

    assert results
    assert all(result["food_calories_per_serving"] <= 300 for result in results)


def test_rag_response_uses_fallback_when_llm_is_unavailable(monkeypatch):
    collection, _food_items = bootstrap_food_collection()
    results = perform_similarity_search(
        collection,
        "I want something spicy and healthy for dinner.",
        3,
    )
    monkeypatch.setattr(
        "orchestration.food_rag_orchestration.invoke_llm",
        lambda prompt: None,
    )

    response = generate_food_rag_response(
        "I want something spicy and healthy for dinner.",
        results,
    )

    assert "For 'I want something spicy and healthy for dinner.'" in response
    assert results[0]["food_name"] in response


def test_query_comparison_fallback_mentions_both_top_results(monkeypatch):
    collection, _food_items = bootstrap_food_collection()
    left_results = perform_similarity_search(collection, "chocolate dessert", 3)
    right_results = perform_similarity_search(collection, "healthy breakfast", 3)
    monkeypatch.setattr(
        "orchestration.food_rag_orchestration.invoke_llm",
        lambda prompt: None,
    )

    response = compare_food_queries(
        "chocolate dessert",
        left_results,
        "healthy breakfast",
        right_results,
    )

    assert left_results[0]["food_name"] in response
    assert right_results[0]["food_name"] in response
