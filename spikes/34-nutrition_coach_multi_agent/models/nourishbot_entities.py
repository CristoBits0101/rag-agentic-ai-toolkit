# --- DEPENDENCIAS ---
from pydantic import BaseModel
from pydantic import Field


class DetectedMeal(BaseModel):
    image_key: str = Field(..., description="Matched dataset image key.")
    title: str = Field(..., description="Detected meal title.")
    similarity_score: float = Field(..., description="Similarity score against the local image dataset.")
    identified_items: list[str] = Field(default_factory=list, description="Food items associated with the detected meal.")
    vision_notes: str = Field(..., description="Visual notes or multimodal fallback description.")


class NutritionSnapshot(BaseModel):
    dish: str = Field(..., description="Detected dish title.")
    estimated_calories: int = Field(..., description="Estimated calories for the meal.")
    protein: str = Field(..., description="Protein estimate.")
    carbohydrates: str = Field(..., description="Carbohydrate estimate.")
    fats: str = Field(..., description="Fat estimate.")
    fiber: str = Field(..., description="Fiber estimate.")
    vitamins: list[str] = Field(default_factory=list, description="Key vitamins.")
    minerals: list[str] = Field(default_factory=list, description="Key minerals.")
    health_evaluation: str = Field(..., description="Health framing of the meal.")
    nutrition_summary: str = Field(..., description="One paragraph summary.")


class DietaryAdvice(BaseModel):
    dietary_preference: str = Field(..., description="User selected dietary preference.")
    compatible: bool = Field(..., description="Whether the detected meal is compatible with the preference.")
    allowed_ingredients: list[str] = Field(default_factory=list, description="Ingredients that remain compatible.")
    blocked_ingredients: list[str] = Field(default_factory=list, description="Ingredients blocked by the diet.")
    coaching_note: str = Field(..., description="Suggested adjustment for the meal.")


class RecipeSuggestion(BaseModel):
    title: str = Field(..., description="Recipe title.")
    ingredients: list[str] = Field(default_factory=list, description="Recommended ingredient list.")
    instructions: str = Field(..., description="Condensed preparation guidance.")
    calorie_target: int = Field(..., description="Approximate calorie target.")
    rationale: str = Field(..., description="Why the recipe suits the selected dietary preference.")