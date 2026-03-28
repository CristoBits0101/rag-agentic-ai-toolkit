# --- DEPENDENCIAS ---
# 1. Configuracion local: Este archivo solo define constantes.

# --- CONFIGURACION ---
# 1. Coleccion: Nombre usado por la practica de recomendaciones.
# 2. Espacio HNSW: Distancia aplicada por ChromaDB.
# 3. Resultados: Cantidad de vecinos recuperados por defecto.
# 4. LLM: Modelo local de Ollama usado para la parte RAG.
COLLECTION_NAME = "food_recommendation_collection"
HNSW_SPACE = "cosine"
DEFAULT_N_RESULTS = 5
MAX_CONTEXT_ITEMS = 3
OLLAMA_MODEL_NAME = "llama3.2:3b"
DATA_FILE_NAME = "food_dataset.json"

# --- CONSULTAS ---
# 1. Basica: Consulta de similitud sin filtros.
# 2. Cocina: Consulta y cocina objetivo para filtrar por metadatos.
# 3. Calorias: Consulta saludable con limite calorico.
# 4. Combinada: Consulta con cocina y calorias a la vez.
# 5. RAG: Consulta conversacional para recomendacion contextual.
# 6. Comparacion: Par de consultas para contrastar preferencias.
BASIC_QUERY_TEXT = "chocolate dessert"
CUISINE_FILTER_QUERY_TEXT = "creamy pasta"
CUISINE_FILTER_VALUE = "Italian"
CALORIE_FILTER_QUERY_TEXT = "healthy meal"
CALORIE_FILTER_VALUE = 300
COMBINED_FILTER_QUERY_TEXT = "light fresh meal"
COMBINED_FILTER_CUISINE = "Japanese"
COMBINED_FILTER_MAX_CALORIES = 250
RAG_QUERY_TEXT = "I want something spicy and healthy for dinner."
COMPARE_QUERY_LEFT = "chocolate dessert"
COMPARE_QUERY_RIGHT = "healthy breakfast"
