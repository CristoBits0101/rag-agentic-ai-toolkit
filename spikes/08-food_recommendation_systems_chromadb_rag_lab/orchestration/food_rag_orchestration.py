# --- DEPENDENCIAS ---
# 1. Configuracion: Para limitar el contexto enviado al modelo.
# 2. LLM: Para invocar Ollama cuando este disponible.
from config.food_recommendation_config import MAX_CONTEXT_ITEMS
from models.food_ollama_gateway import invoke_llm

# --- RAG ---
# 1.1. Funcion para preparar contexto estructurado para el LLM.
def prepare_context_for_llm(query: str, search_results: list[dict]) -> str:
    # Devuelve un contexto simple cuando no hay resultados.
    if not search_results:
        return "No relevant food items were retrieved for the request."

    context_parts = [
        f"User query: {query}",
        "Retrieved food options:",
    ]

    # Recorre solo los mejores elementos para controlar el tamano.
    for index, result in enumerate(search_results[:MAX_CONTEXT_ITEMS], 1):
        ingredients = ", ".join(result["food_ingredients"][:5])
        context_parts.append(
            f"Option {index}: {result['food_name']} | "
            f"Cuisine: {result['cuisine_type']} | "
            f"Meal type: {result['meal_type']} | "
            f"Calories: {result['food_calories_per_serving']} | "
            f"Description: {result['food_description']} | "
            f"Ingredients: {ingredients} | "
            f"Health benefits: {result['food_health_benefits']} | "
            f"Taste profile: {result['taste_profile']} | "
            f"Similarity: {result['similarity_score'] * 100:.1f}%."
        )

    # Devuelve el contexto unido para el prompt.
    return "\n".join(context_parts)


# 1.2. Funcion para generar la respuesta RAG principal.
def generate_food_rag_response(query: str, search_results: list[dict]) -> str:
    # Sale temprano cuando no hubo recuperacion.
    if not search_results:
        return (
            "I could not find matching food items for your request. "
            "Try using ingredients cuisine types or meal moments."
        )

    # Prepara el contexto recuperado antes de construir el prompt.
    context = prepare_context_for_llm(query, search_results)
    prompt = (
        "You are a food recommendation assistant.\n"
        "Use only the retrieved food options.\n"
        "Recommend two or three foods that match the request.\n"
        "Explain the match using cuisine calories taste and health benefits.\n"
        "Keep the answer concise and conversational.\n\n"
        f"{context}\n\n"
        "Answer:"
    )
    llm_response = invoke_llm(prompt)

    # Devuelve la salida del modelo cuando existe una respuesta util.
    return llm_response or "The food recommendation model returned an empty response."


# 1.3. Funcion para comparar dos preferencias de comida.
def compare_food_queries(
    query_left: str,
    results_left: list[dict],
    query_right: str,
    results_right: list[dict],
) -> str:
    # Construye el prompt de comparacion entre preferencias.
    prompt = (
        "You compare two food recommendation requests.\n"
        "Summarize the key difference between them.\n"
        "Mention the best option from each side.\n"
        "Keep the answer short.\n\n"
        f"Left side:\n{prepare_context_for_llm(query_left, results_left)}\n\n"
        f"Right side:\n{prepare_context_for_llm(query_right, results_right)}\n\n"
        "Comparison:"
    )
    llm_response = invoke_llm(prompt)

    # Devuelve el analisis del modelo cuando esta disponible.
    return llm_response or "The food comparison model returned an empty response."
