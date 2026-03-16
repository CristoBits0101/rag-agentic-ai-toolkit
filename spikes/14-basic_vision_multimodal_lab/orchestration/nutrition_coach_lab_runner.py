# --- DEPENDENCIAS ---
from config.nutrition_coach_config import NUTRITION_COACH_DEFAULT_MODEL
from models.nutrition_coach_image_processor import NutritionCoachImageProcessor
from models.nutrition_coach_llm_service import NutritionCoachVisionService
from orchestration.nutrition_coach_asset_orchestration import ensure_nutrition_coach_example_assets
from orchestration.nutrition_coach_dataset_orchestration import build_nutrition_coach_dataset
from orchestration.nutrition_coach_helpers import get_all_items_for_image


def print_separator(title: str) -> None:
    print("=" * 60)
    print(title)
    print("=" * 60)


def run_nutrition_coach_lab(model_name: str = NUTRITION_COACH_DEFAULT_MODEL) -> None:
    print_separator("14. NUTRITION COACH FLASK APP")
    example_paths = ensure_nutrition_coach_example_assets()
    image_processor = NutritionCoachImageProcessor()
    dataset = build_nutrition_coach_dataset(image_processor)
    first_example_path = next(iter(example_paths.values()))
    user_encoding = image_processor.encode_image(first_example_path, is_url=False)
    closest_row, _ = image_processor.find_closest_match(user_encoding["vector"], dataset)
    related_items = get_all_items_for_image(closest_row["Image Key"], dataset)
    response = NutritionCoachVisionService(model_name).generate_nutrition_response(
        user_image_base64=user_encoding["base64"],
        related_items=related_items,
        user_query="How many calories are in this food?",
    )
    print(f"Model: {model_name}")
    print(f"Example: {first_example_path}")
    print()
    print(response)
