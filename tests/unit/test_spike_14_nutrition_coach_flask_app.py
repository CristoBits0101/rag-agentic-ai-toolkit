# --- DEPENDENCIAS ---
import io
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPIKE = ROOT / "spikes" / "14-basic_vision_multimodal_lab"

if str(SPIKE) not in sys.path:
    sys.path.insert(0, str(SPIKE))

from config.nutrition_coach_config import NUTRITION_COACH_SUPPORTED_MODELS
from models.nutrition_coach_image_processor import NutritionCoachImageProcessor
from models.nutrition_coach_llm_service import NutritionCoachVisionService
from orchestration.nutrition_coach_app_orchestration import create_nutrition_coach_app
from orchestration.nutrition_coach_asset_orchestration import ensure_nutrition_coach_example_assets
from orchestration.nutrition_coach_dataset_orchestration import build_nutrition_coach_dataset
from orchestration.nutrition_coach_helpers import build_nutrition_reference_text
from orchestration.nutrition_coach_helpers import format_response
from orchestration.nutrition_coach_helpers import get_all_items_for_image


class FakeNutritionCoachService:
    def __init__(self, model_name):
        self.model_name = model_name

    def generate_nutrition_response(
        self,
        user_image_base64,
        related_items,
        user_query,
    ):
        total_calories = int(related_items["Calories"].sum())
        return (
            "**Identification**\n"
            f"- {related_items.iloc[0]['Food Item']}\n\n"
            "**Portion Size & Calorie Estimation**\n"
            f"- {related_items.iloc[0]['Food Item']}: {related_items.iloc[0]['Portion Size']}, "
            f"{related_items.iloc[0]['Calories']} calories\n\n"
            "**Total Calories**\n"
            f"Total Calories: {total_calories}\n\n"
            "**Health Evaluation**\n"
            f"Query received: {user_query}\n\n"
            "**Disclaimer**\n"
            "Demo only."
        )


def test_nutrition_coach_example_assets_are_created():
    image_paths = ensure_nutrition_coach_example_assets()

    assert len(image_paths) == 3
    assert all(path.exists() for path in image_paths.values())


def test_nutrition_coach_dataset_contains_embeddings():
    image_processor = NutritionCoachImageProcessor()
    dataset = build_nutrition_coach_dataset(image_processor)

    assert len(dataset) == 8
    assert "Embedding" in dataset.columns
    assert dataset.iloc[0]["Embedding"].size > 0


def test_get_all_items_for_image_returns_meal_rows():
    image_processor = NutritionCoachImageProcessor()
    dataset = build_nutrition_coach_dataset(image_processor)
    image_key = dataset.iloc[0]["Image Key"]
    related_items = get_all_items_for_image(image_key, dataset)

    assert len(related_items) == 2
    assert all(related_items["Image Key"] == image_key)


def test_build_nutrition_reference_text_includes_total():
    image_processor = NutritionCoachImageProcessor()
    dataset = build_nutrition_coach_dataset(image_processor)
    related_items = get_all_items_for_image("salmon_plate", dataset)
    reference_text = build_nutrition_reference_text(related_items)

    assert "Grilled salmon" in reference_text
    assert "Total Calories: 638" in reference_text


def test_format_response_returns_html_markup():
    formatted = format_response(
        "**Identification**\n- Cheeseburger\n\n**Total Calories**\nTotal Calories: 905"
    )

    assert "<strong>Identification</strong>" in formatted
    assert "<li>Cheeseburger</li>" in formatted


def test_nutrition_service_returns_explicit_error_when_response_is_short():
    image_processor = NutritionCoachImageProcessor()
    dataset = build_nutrition_coach_dataset(image_processor)
    related_items = get_all_items_for_image("salad_bowl", dataset)
    service = NutritionCoachVisionService(
        NUTRITION_COACH_SUPPORTED_MODELS[0],
        response_generator=lambda model_name, prompt, encoded_image: "Short.",
    )

    response = service.generate_nutrition_response(
        user_image_base64="encoded-image",
        related_items=related_items,
        user_query="How many calories are in this food?",
    )

    assert "Error generating response" in response
    assert "**Reference Context**" in response
    assert "**Reference Nutrients**" in response
    assert "Total Calories: 367" in response


def test_nutrition_coach_app_renders_home_page():
    app = create_nutrition_coach_app(llm_service_factory=FakeNutritionCoachService)
    client = app.test_client()
    response = client.get("/")
    page = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "AI Nutrition Coach" in page
    assert "Active model" in page


def test_nutrition_coach_app_processes_uploaded_image():
    image_paths = ensure_nutrition_coach_example_assets()
    app = create_nutrition_coach_app(llm_service_factory=FakeNutritionCoachService)
    client = app.test_client()
    image_bytes = image_paths["burger_combo"].read_bytes()

    response = client.post(
        "/",
        data={
            "user_query": "How many calories are in this food?",
            "file": (io.BytesIO(image_bytes), "burger_combo.png"),
        },
        content_type="multipart/form-data",
    )
    page = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "Nutrition analysis" in page
    assert "Total Calories: 905" in page
    assert "Cheeseburger" in page


def test_nutrition_coach_variant_subfolders_exist():
    assert (SPIKE / "nutrition_coach_flask_app" / "app.py").exists()
    assert (SPIKE / "nutrition_coach_flask_app" / "main.py").exists()
    assert (SPIKE / "nutrition_coach_llama3_2_vision_app" / "main.py").exists()
    assert (SPIKE / "nutrition_coach_llava_app" / "main.py").exists()
    assert (SPIKE / "nutrition_coach_qwen2_5vl_app" / "main.py").exists()
