# --- DEPENDENCIAS ---
# 1. Sys: Para anadir la ruta del spike a los imports de prueba.
# 2. Path: Para resolver la ruta absoluta del spike.
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPIKE = ROOT / "spikes" / "08-food_recommendation_rag"

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


def test_rag_response_uses_real_llm_output_when_gateway_is_stubbed(monkeypatch):
    collection, _food_items = bootstrap_food_collection()
    results = perform_similarity_search(
        collection,
        "I want something spicy and healthy for dinner.",
        3,
    )
    monkeypatch.setattr(
        "orchestration.food_rag_orchestration.invoke_llm",
        lambda prompt: "Try Spicy Tofu Stir Fry first and keep Greek Salad as a lighter second option.",
    )

    response = generate_food_rag_response(
        "I want something spicy and healthy for dinner.",
        results,
    )

    assert "Spicy Tofu Stir Fry" in response
    assert "Greek Salad" in response


def test_query_comparison_uses_real_llm_output_when_gateway_is_stubbed(monkeypatch):
    collection, _food_items = bootstrap_food_collection()
    left_results = perform_similarity_search(collection, "chocolate dessert", 3)
    right_results = perform_similarity_search(collection, "healthy breakfast", 3)
    monkeypatch.setattr(
        "orchestration.food_rag_orchestration.invoke_llm",
        lambda prompt: "Chocolate Lava Cake is richer while Greek Yogurt Parfait is the lighter breakfast choice.",
    )

    response = compare_food_queries(
        "chocolate dessert",
        left_results,
        "healthy breakfast",
        right_results,
    )

    assert "Chocolate Lava Cake" in response
    assert "Greek Yogurt Parfait" in response
