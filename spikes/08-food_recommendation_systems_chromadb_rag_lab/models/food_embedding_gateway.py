# --- DEPENDENCIAS ---
# 1. Regex: Para tokenizar texto de forma simple.
# 2. Numpy: Para devolver embeddings listos para ChromaDB.
import re

import numpy as np

# --- EMBEDDINGS ---
# 1.1. Diccionario de palabras clave por dominio culinario.
KEYWORD_GROUPS = {
    "dessert_sweet": {
        "baked",
        "cake",
        "chocolate",
        "cocoa",
        "dessert",
        "honey",
        "lava",
        "pie",
        "sweet",
        "treat",
    },
    "italian_comfort": {
        "basil",
        "creamy",
        "italian",
        "mozzarella",
        "parmesan",
        "pasta",
        "pizza",
        "primavera",
        "risotto",
        "tomato",
    },
    "spicy_dinner": {
        "basil",
        "chili",
        "comfort",
        "dinner",
        "hearty",
        "pepper",
        "savory",
        "spiced",
        "spicy",
        "tikka",
        "warm",
    },
    "healthy_light": {
        "avocado",
        "fresh",
        "grilled",
        "healthy",
        "light",
        "low",
        "salad",
        "vegetable",
        "vegetables",
        "wrap",
    },
    "breakfast_protein": {
        "breakfast",
        "egg",
        "eggs",
        "morning",
        "omelette",
        "parfait",
        "protein",
        "toast",
        "yogurt",
    },
    "asian_umami": {
        "asian",
        "ginger",
        "japanese",
        "miso",
        "sesame",
        "soba",
        "soy",
        "thai",
        "tofu",
        "umami",
    },
    "mediterranean_fresh": {
        "cucumber",
        "feta",
        "greek",
        "herbs",
        "lemon",
        "lentil",
        "mediterranean",
        "olive",
        "parsley",
    },
    "comfort_hearty": {
        "chili",
        "comfort",
        "cozy",
        "creamy",
        "hearty",
        "risotto",
        "soup",
        "warm",
    },
    "vegetarian_plant": {
        "avocado",
        "berries",
        "lentil",
        "mushroom",
        "spinach",
        "tofu",
        "veggie",
        "vegetarian",
    },
    "protein_rich": {
        "beef",
        "chicken",
        "egg",
        "eggs",
        "greek",
        "lentil",
        "protein",
        "salmon",
        "tofu",
        "yogurt",
    },
}


# 1.2. Funcion para tokenizar un texto de entrada.
def tokenize_text(text: str) -> list[str]:
    # Convierte a minusculas y extrae solo palabras simples.
    return re.findall(r"[a-z0-9]+", text.lower())


# 1.3. Funcion para crear un embedding determinista.
def build_food_embedding(text: str) -> np.ndarray:
    # Tokeniza el texto antes de contar senales semanticas.
    tokens = tokenize_text(text)
    vector = np.array(
        [
            float(sum(token in KEYWORD_GROUPS["dessert_sweet"] for token in tokens)),
            float(sum(token in KEYWORD_GROUPS["italian_comfort"] for token in tokens)),
            float(sum(token in KEYWORD_GROUPS["spicy_dinner"] for token in tokens)),
            float(sum(token in KEYWORD_GROUPS["healthy_light"] for token in tokens)),
            float(sum(token in KEYWORD_GROUPS["breakfast_protein"] for token in tokens)),
            float(sum(token in KEYWORD_GROUPS["asian_umami"] for token in tokens)),
            float(
                sum(token in KEYWORD_GROUPS["mediterranean_fresh"] for token in tokens)
            ),
            float(sum(token in KEYWORD_GROUPS["comfort_hearty"] for token in tokens)),
            float(sum(token in KEYWORD_GROUPS["vegetarian_plant"] for token in tokens)),
            float(sum(token in KEYWORD_GROUPS["protein_rich"] for token in tokens)),
        ],
        dtype=np.float32,
    )

    # Evita vectores nulos para no degradar la similitud coseno.
    if not vector.any():
        return np.ones(10, dtype=np.float32)

    # Devuelve el embedding como vector Numpy.
    return vector


# 1.4. Funcion para crear embeddings de una lista de textos.
def build_food_embeddings(texts: list[str]) -> list[list[float]]:
    # Devuelve embeddings serializables para ChromaDB.
    return [build_food_embedding(text).tolist() for text in texts]
