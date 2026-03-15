# --- DEPENDENCIAS ---
# 1. Configuracion local: Este archivo solo define constantes.

# --- CONFIGURACION ---
# 1. Coleccion: Nombre base usado por la demo local.
# 2. Espacio HNSW: Distancia aplicada por la coleccion en ChromaDB.
# 3. Resultados: Cantidad de vecinos recuperados por defecto.
COLLECTION_NAME = "chromadb_cheat_sheet_demo"
HNSW_SPACE = "cosine"
DEFAULT_N_RESULTS = 3

# --- RESUMEN ---
# 1. Metricas: Lineas breves para imprimir el resumen del laboratorio.
METRIC_SUMMARY_LINES = [
    "L2 Distance: Mide distancia recta y es sensible a magnitud y direccion.",
    "Dot Product: Mide similitud y premia direccion y magnitud.",
    "Cosine Similarity: Mide orientacion y funciona muy bien para texto y embeddings.",
]
VECTOR_DATABASE_SUMMARY_LINES = [
    "Vector Database: Guarda datos como vectores y consulta por similitud.",
    "Traditional Database: Trabaja sobre tablas filas columnas y filtros exactos.",
    "HNSW: Indice aproximado basado en grafos para recuperar vecinos cercanos con baja latencia.",
]
