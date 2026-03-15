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


# 1.2. Funcion para crear una respuesta de respaldo sin LLM.
def generate_fallback_response(query: str, search_results: list[dict]) -> str:
    # Devuelve un mensaje claro cuando no hubo recuperacion.
    if not search_results:
        return (
            "I could not find matching food items for your request. "
            "Try using ingredients cuisine types or meal moments."
        )

    top_result = search_results[0]
    response_parts = [
        f"For '{query}' I recommend {top_result['food_name']}.",
        f"It is a {top_result['cuisine_type']} {top_result['meal_type'].lower()} option",
        f"with {top_result['food_calories_per_serving']} calories.",
    ]

    if top_result["food_health_benefits"]:
        response_parts.append(top_result["food_health_benefits"])

    if len(search_results) > 1:
        response_parts.append(
            f"Another strong option is {search_results[1]['food_name']}."
        )

    # Devuelve la recomendacion final unida en una sola respuesta.
    return " ".join(response_parts)


# 1.3. Funcion para generar la respuesta RAG principal.
def generate_food_rag_response(query: str, search_results: list[dict]) -> str:
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

    # Usa fallback cuando Ollama no esta disponible o devuelve poco texto.
    if llm_response is None or len(llm_response) < 40:
        return generate_fallback_response(query, search_results)

    # Devuelve la salida del modelo cuando existe una respuesta util.
    return llm_response


# 1.4. Funcion para comparar dos preferencias de comida.
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

    # Usa una comparacion simple cuando no hay LLM disponible.
    if llm_response is None or len(llm_response) < 40:
        left_name = results_left[0]["food_name"] if results_left else "no result"
        right_name = results_right[0]["food_name"] if results_right else "no result"
        return (
            f"The first query points to {left_name} as a richer indulgent option while "
            f"the second query points to {right_name} as a lighter healthier choice."
        )

    # Devuelve el analisis del modelo cuando esta disponible.
    return llm_response
