# --- DEPENDENCIAS ---
# 1. Configuracion: Para leer el numero de resultados por defecto.
# 2. Embeddings: Para convertir consultas en vectores.
from config.food_recommendation_config import DEFAULT_N_RESULTS
from models.food_embedding_gateway import build_food_embedding

# --- BUSQUEDA ---
# 1.1. Funcion para construir filtros de metadatos.
def build_where_clause(
    cuisine_filter: str | None = None,
    max_calories: int | None = None,
):
    # Acumula filtros individuales solo cuando se solicitan.
    filters: list[dict] = []

    if cuisine_filter:
        filters.append({"cuisine_type": cuisine_filter})

    if max_calories is not None:
        filters.append({"calories": {"$lte": max_calories}})

    # Devuelve None si no se aplican restricciones.
    if not filters:
        return None

    # Devuelve filtro simple cuando solo existe una restriccion.
    if len(filters) == 1:
        return filters[0]

    # Devuelve un and explicito para varias restricciones.
    return {"$and": filters}


# 1.2. Funcion para normalizar un resultado de ChromaDB.
def normalize_query_results(query_result: dict) -> list[dict]:
    # Sale temprano si la consulta no trae vecinos.
    if not query_result or not query_result.get("ids") or not query_result["ids"][0]:
        return []

    ids = query_result["ids"][0]
    metadatas = query_result["metadatas"][0]
    distances = query_result["distances"][0]
    documents = query_result["documents"][0]
    normalized: list[dict] = []

    # Recorre cada vecino y construye un resultado uniforme.
    for index, item_id in enumerate(ids):
        metadata = metadatas[index]
        ingredients_text = metadata.get("ingredients", "")
        tags_text = metadata.get("dietary_tags", "")
        normalized.append(
            {
                "food_id": item_id,
                "food_name": metadata.get("name", ""),
                "food_description": metadata.get("description", ""),
                "cuisine_type": metadata.get("cuisine_type", ""),
                "meal_type": metadata.get("meal_type", ""),
                "food_calories_per_serving": metadata.get("calories", 0),
                "cooking_method": metadata.get("cooking_method", ""),
                "food_health_benefits": metadata.get("health_benefits", ""),
                "taste_profile": metadata.get("taste_profile", ""),
                "food_ingredients": [
                    item.strip()
                    for item in ingredients_text.split(",")
                    if item.strip()
                ],
                "dietary_tags": [
                    item.strip()
                    for item in tags_text.split(",")
                    if item.strip()
                ],
                "similarity_score": 1 - distances[index],
                "distance": distances[index],
                "document": documents[index],
            }
        )

    # Devuelve la lista de resultados formateada.
    return normalized


# 1.3. Funcion para realizar similarity search sin filtros.
def perform_similarity_search(
    collection,
    query: str,
    n_results: int = DEFAULT_N_RESULTS,
) -> list[dict]:
    # Genera el embedding determinista de la consulta.
    query_embedding = build_food_embedding(query).tolist()
    query_result = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
    )

    # Devuelve la lista de resultados normalizada.
    return normalize_query_results(query_result)


# 1.4. Funcion para realizar similarity search con filtros.
def perform_filtered_similarity_search(
    collection,
    query: str,
    cuisine_filter: str | None = None,
    max_calories: int | None = None,
    n_results: int = DEFAULT_N_RESULTS,
) -> list[dict]:
    # Genera el embedding y aplica filtros de metadatos.
    query_embedding = build_food_embedding(query).tolist()
    query_result = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        where=build_where_clause(cuisine_filter, max_calories),
    )

    # Devuelve la lista de resultados normalizada.
    return normalize_query_results(query_result)


# 1.5. Funcion para resumir resultados de forma legible.
def format_food_results(results: list[dict], detailed: bool = True) -> str:
    # Sale temprano cuando no existen resultados.
    if not results:
        return "No matching foods found."

    lines: list[str] = []

    # Recorre cada recomendacion y genera una linea de salida.
    for index, result in enumerate(results, 1):
        if detailed:
            lines.append(
                f"{index}. {result['food_name']} | {result['cuisine_type']} | "
                f"{result['food_calories_per_serving']} cal | "
                f"{result['similarity_score'] * 100:.1f}% match | "
                f"{result['food_description']}"
            )
        else:
            lines.append(
                f"{index}. {result['food_name']} "
                f"({result['similarity_score'] * 100:.1f}% match)"
            )

    # Devuelve el bloque compacto de texto.
    return "\n".join(lines)
