# --- DEPENDENCIAS ---
# 1. Configuracion: Para leer consultas y filtros de demostracion.
# 2. Coleccion: Para crear y poblar la base vectorial del spike.
# 3. RAG: Para generar recomendaciones y comparaciones explicadas.
# 4. Busqueda: Para ejecutar consultas basicas y filtradas.
from config.food_recommendation_config import BASIC_QUERY_TEXT
from config.food_recommendation_config import CALORIE_FILTER_QUERY_TEXT
from config.food_recommendation_config import CALORIE_FILTER_VALUE
from config.food_recommendation_config import COMBINED_FILTER_CUISINE
from config.food_recommendation_config import COMBINED_FILTER_MAX_CALORIES
from config.food_recommendation_config import COMBINED_FILTER_QUERY_TEXT
from config.food_recommendation_config import COMPARE_QUERY_LEFT
from config.food_recommendation_config import COMPARE_QUERY_RIGHT
from config.food_recommendation_config import CUISINE_FILTER_QUERY_TEXT
from config.food_recommendation_config import CUISINE_FILTER_VALUE
from config.food_recommendation_config import RAG_QUERY_TEXT
from orchestration.food_collection_orchestration import bootstrap_food_collection
from orchestration.food_rag_orchestration import compare_food_queries
from orchestration.food_rag_orchestration import generate_food_rag_response
from orchestration.food_search_orchestration import format_food_results
from orchestration.food_search_orchestration import perform_filtered_similarity_search
from orchestration.food_search_orchestration import perform_similarity_search

# --- RUNNER ---
# 1.1. Funcion para imprimir titulos de seccion.
def print_section(title: str):
    # Separa visualmente cada bloque de resultados.
    print(f"\n=== {title} ===")


# 1.2. Funcion para ejecutar el laboratorio adaptado.
def run_food_recommendation_lab():
    # Crea la coleccion y carga el dataset local.
    collection, food_items = bootstrap_food_collection()
    print("Practice 08 Food Recommendation Systems With ChromaDB And RAG.")
    print(f"Dataset loaded: {len(food_items)} food items.")
    print("RAG generation uses Ollama when available and falls back otherwise.")

    print_section("Interactive Search Style")
    print(f"Query: {BASIC_QUERY_TEXT}")
    print(format_food_results(perform_similarity_search(collection, BASIC_QUERY_TEXT, 3)))

    print_section("Advanced Search Style")
    print(f"Cuisine filtered query: {CUISINE_FILTER_QUERY_TEXT}")
    print(
        format_food_results(
            perform_filtered_similarity_search(
                collection,
                CUISINE_FILTER_QUERY_TEXT,
                cuisine_filter=CUISINE_FILTER_VALUE,
                n_results=3,
            )
        )
    )
    print(f"\nCalorie filtered query: {CALORIE_FILTER_QUERY_TEXT}")
    print(
        format_food_results(
            perform_filtered_similarity_search(
                collection,
                CALORIE_FILTER_QUERY_TEXT,
                max_calories=CALORIE_FILTER_VALUE,
                n_results=3,
            )
        )
    )
    print(f"\nCombined filtered query: {COMBINED_FILTER_QUERY_TEXT}")
    print(
        format_food_results(
            perform_filtered_similarity_search(
                collection,
                COMBINED_FILTER_QUERY_TEXT,
                cuisine_filter=COMBINED_FILTER_CUISINE,
                max_calories=COMBINED_FILTER_MAX_CALORIES,
                n_results=3,
            )
        )
    )

    print_section("RAG Chatbot Style")
    rag_results = perform_similarity_search(collection, RAG_QUERY_TEXT, 3)
    print(f"Query: {RAG_QUERY_TEXT}")
    print(f"Bot: {generate_food_rag_response(RAG_QUERY_TEXT, rag_results)}")
    print("\nRetrieved context:")
    print(format_food_results(rag_results))

    print_section("System Comparison")
    left_results = perform_similarity_search(collection, COMPARE_QUERY_LEFT, 3)
    right_results = perform_similarity_search(collection, COMPARE_QUERY_RIGHT, 3)
    print(f"Left query: {COMPARE_QUERY_LEFT}")
    print(format_food_results(left_results, detailed=False))
    print(f"\nRight query: {COMPARE_QUERY_RIGHT}")
    print(format_food_results(right_results, detailed=False))
    print("\nComparison insight:")
    print(compare_food_queries(COMPARE_QUERY_LEFT, left_results, COMPARE_QUERY_RIGHT, right_results))

    print_section("Summary")
    print("Interactive search: Fast discovery from semantic similarity.")
    print("Advanced search: Similarity plus cuisine and calorie filters.")
    print("RAG chatbot: Context aware explanation grounded in retrieved foods.")
