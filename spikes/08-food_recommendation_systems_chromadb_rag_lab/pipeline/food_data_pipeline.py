# --- DEPENDENCIAS ---
# 1. Json: Para cargar el dataset local de comida.
# 2. Path: Para resolver la ruta del archivo de datos.
# 3. Any: Para tipar estructuras flexibles del dataset.
# 4. Dict: Para tipar cada item normalizado.
# 5. List: Para tipar colecciones de comida.
import json
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List

from config.food_recommendation_config import DATA_FILE_NAME

# --- PIPELINE ---
# 1.1. Funcion para resolver la ruta local del dataset.
def get_food_data_path() -> Path:
    # Devuelve la ruta absoluta del archivo JSON del spike.
    return Path(__file__).resolve().parents[1] / "data" / DATA_FILE_NAME


# 1.2. Funcion para normalizar un item de comida.
def normalize_food_item(item: Dict[str, Any], index: int) -> Dict[str, Any]:
    # Copia el item para no mutar la estructura original.
    normalized = dict(item)
    normalized["food_id"] = str(normalized.get("food_id", index + 1))
    normalized["food_name"] = str(normalized.get("food_name", f"Food {index + 1}"))
    normalized["food_description"] = str(normalized.get("food_description", ""))
    normalized["cuisine_type"] = str(normalized.get("cuisine_type", "Unknown"))
    normalized["cooking_method"] = str(normalized.get("cooking_method", ""))
    normalized["food_health_benefits"] = str(
        normalized.get("food_health_benefits", "")
    )
    normalized["meal_type"] = str(normalized.get("meal_type", "Any"))
    normalized["food_calories_per_serving"] = int(
        normalized.get("food_calories_per_serving", 0)
    )
    normalized["food_ingredients"] = list(normalized.get("food_ingredients", []))
    normalized["dietary_tags"] = list(normalized.get("dietary_tags", []))
    normalized["food_nutritional_factors"] = dict(
        normalized.get("food_nutritional_factors", {})
    )
    feature_values = normalized.get("food_features", {})
    taste_parts: list[str] = []

    # Recorre las caracteristicas y compone un perfil simple de sabor.
    if isinstance(feature_values, dict):
        for value in feature_values.values():
            if value:
                taste_parts.append(str(value))

    # Guarda un perfil sintetico para documentos y metadatos.
    normalized["taste_profile"] = ", ".join(taste_parts)
    return normalized


# 1.3. Funcion para cargar y normalizar el dataset local.
def load_food_data() -> List[Dict[str, Any]]:
    # Abre el archivo JSON del spike.
    with get_food_data_path().open("r", encoding="utf-8") as file:
        raw_items = json.load(file)

    # Devuelve todos los items ya normalizados.
    return [normalize_food_item(item, index) for index, item in enumerate(raw_items)]


# 1.4. Funcion para construir el documento enriquecido de un alimento.
def build_food_document(food_item: Dict[str, Any]) -> str:
    # Compone un texto rico para el embedding semantico.
    nutrition = ", ".join(
        f"{key}: {value}"
        for key, value in food_item["food_nutritional_factors"].items()
    )
    ingredients = ", ".join(food_item["food_ingredients"])
    dietary_tags = ", ".join(food_item["dietary_tags"])
    return (
        f"Name: {food_item['food_name']}. "
        f"Description: {food_item['food_description']}. "
        f"Cuisine: {food_item['cuisine_type']}. "
        f"Meal type: {food_item['meal_type']}. "
        f"Cooking method: {food_item['cooking_method']}. "
        f"Ingredients: {ingredients}. "
        f"Taste profile: {food_item['taste_profile']}. "
        f"Health benefits: {food_item['food_health_benefits']}. "
        f"Dietary tags: {dietary_tags}. "
        f"Calories: {food_item['food_calories_per_serving']}. "
        f"Nutrition: {nutrition}."
    )


# 1.5. Funcion para construir metadatos compatibles con ChromaDB.
def build_food_metadata(food_item: Dict[str, Any]) -> Dict[str, Any]:
    # Convierte listas en texto para evitar metadatos no escalares.
    return {
        "name": food_item["food_name"],
        "cuisine_type": food_item["cuisine_type"],
        "meal_type": food_item["meal_type"],
        "ingredients": ", ".join(food_item["food_ingredients"]),
        "calories": food_item["food_calories_per_serving"],
        "description": food_item["food_description"],
        "cooking_method": food_item["cooking_method"],
        "health_benefits": food_item["food_health_benefits"],
        "taste_profile": food_item["taste_profile"],
        "dietary_tags": ", ".join(food_item["dietary_tags"]),
    }
