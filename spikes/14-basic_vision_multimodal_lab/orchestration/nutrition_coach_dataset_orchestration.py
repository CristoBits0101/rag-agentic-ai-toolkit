# --- DEPENDENCIAS ---
import pandas as pd

from data.nutrition_coach_dataset import NUTRITION_COACH_MEALS
from orchestration.nutrition_coach_asset_orchestration import ensure_nutrition_coach_example_assets


def build_nutrition_coach_dataset(image_processor) -> pd.DataFrame:
    image_paths = ensure_nutrition_coach_example_assets()
    rows = []

    for meal in NUTRITION_COACH_MEALS:
        image_path = image_paths[meal["image_key"]]
        embedding = image_processor.build_embedding_for_path(image_path)

        for item in meal["items"]:
            rows.append(
                {
                    "Image Key": meal["image_key"],
                    "Image Path": str(image_path),
                    "Image URL": f"file://{image_path.as_posix()}",
                    "Meal Title": meal["title"],
                    "Food Item": item["Food Item"],
                    "Portion Size": item["Portion Size"],
                    "Calories": item["Calories"],
                    "Protein": item["Protein"],
                    "Carbohydrates": item["Carbohydrates"],
                    "Fats": item["Fats"],
                    "Vitamins": item["Vitamins"],
                    "Minerals": item["Minerals"],
                    "Health Note": item["Health Note"],
                    "Embedding": embedding,
                }
            )

    return pd.DataFrame(rows)
