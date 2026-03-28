# --- DEPENDENCIAS ---
import pandas as pd

from data.nourishbot_dataset import DIETARY_RULES
from data.nourishbot_dataset import NOURISHBOT_MEALS
from models.nourishbot_entities import DetectedMeal
from models.nourishbot_entities import DietaryAdvice
from models.nourishbot_entities import NutritionSnapshot
from models.nourishbot_entities import RecipeSuggestion
from models.nourishbot_llm_gateway import generate_vision_notes


class VisionMealDetectionTool:
    name = "vision_meal_detection_tool"

    def __init__(self, image_processor, dataset: pd.DataFrame, vision_note_generator=generate_vision_notes):
        self.image_processor = image_processor
        self.dataset = dataset
        self.vision_note_generator = vision_note_generator

    def run(self, image_path: str) -> DetectedMeal:
        encoded = self.image_processor.encode_image(image_path)
        closest_row, score = self.image_processor.find_closest_match(encoded["vector"], self.dataset)
        if closest_row is None:
            raise RuntimeError("No meal match found for the uploaded image.")
        fallback_note = (
            f"The image most closely matches {closest_row['title']} with ingredients like "
            f"{', '.join(closest_row['identified_items'])}."
        )
        try:
            vision_notes = self.vision_note_generator(
                encoded_image=encoded["base64"],
                prompt=(
                    "Describe the visible food items in one short paragraph and note the main ingredients."
                ),
            )
        except Exception:
            vision_notes = fallback_note

        return DetectedMeal(
            image_key=closest_row["image_key"],
            title=closest_row["title"],
            similarity_score=round(float(score), 4),
            identified_items=list(closest_row["identified_items"]),
            vision_notes=vision_notes,
        )


class NutritionLookupTool:
    name = "nutrition_lookup_tool"

    def __init__(self, dataset: pd.DataFrame):
        self.dataset = dataset

    def run(self, meal_key: str, summary: str = "") -> NutritionSnapshot:
        row = self.dataset[self.dataset["image_key"] == meal_key].iloc[0]
        nutrients = row["nutrients"]
        nutrition_summary = summary or (
            f"{row['title']} delivers {row['estimated_calories']} calories with {nutrients['protein']} of protein and {nutrients['fiber']} of fiber."
        )
        return NutritionSnapshot(
            dish=row["title"],
            estimated_calories=int(row["estimated_calories"]),
            protein=nutrients["protein"],
            carbohydrates=nutrients["carbohydrates"],
            fats=nutrients["fats"],
            fiber=nutrients["fiber"],
            vitamins=list(nutrients["vitamins"]),
            minerals=list(nutrients["minerals"]),
            health_evaluation=row["health_evaluation"],
            nutrition_summary=nutrition_summary,
        )


class DietaryPreferenceTool:
    name = "dietary_preference_tool"

    def run(self, ingredients: list[str], dietary_preference: str) -> DietaryAdvice:
        rules = DIETARY_RULES.get(dietary_preference, [])
        blocked = []
        allowed = []
        for ingredient in ingredients:
            if any(rule in ingredient.lower() for rule in rules):
                blocked.append(ingredient)
            else:
                allowed.append(ingredient)
        compatible = len(blocked) == 0
        if compatible:
            note = f"The detected meal already fits the {dietary_preference} preference."
        elif allowed:
            note = f"To fit {dietary_preference} keep {', '.join(allowed)} and replace {', '.join(blocked)}."
        else:
            note = f"Most ingredients conflict with {dietary_preference} so a new recipe direction is recommended."
        return DietaryAdvice(
            dietary_preference=dietary_preference,
            compatible=compatible,
            allowed_ingredients=allowed,
            blocked_ingredients=blocked,
            coaching_note=note,
        )


class RecipePlanningTool:
    name = "recipe_planning_tool"

    def run(self, meal_key: str, dietary_preference: str, allowed_ingredients: list[str]) -> RecipeSuggestion:
        meal = next(item for item in NOURISHBOT_MEALS if item["image_key"] == meal_key)
        recipe_text = meal["recipe_ideas"].get(dietary_preference) or meal["recipe_ideas"].get("balanced")
        final_ingredients = allowed_ingredients or [item for item in meal["identified_items"] if item not in DIETARY_RULES.get(dietary_preference, [])]
        title = f"{dietary_preference.title()} {meal['title']} Remix"
        instructions = (
            f"Prep {', '.join(final_ingredients[:3])}. Cook or warm the base meal components and finish with a bright sauce. {recipe_text}"
        )
        rationale = f"This recipe keeps the meal aligned with the {dietary_preference} preference while preserving the core flavor profile."
        return RecipeSuggestion(
            title=title,
            ingredients=final_ingredients,
            instructions=instructions,
            calorie_target=int(meal["estimated_calories"]),
            rationale=rationale,
        )