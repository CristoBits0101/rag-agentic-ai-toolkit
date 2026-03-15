# --- DEPENDENCIAS ---
# 1. Configuracion local: Este archivo solo define constantes.

# --- CONFIGURACION ---
# 1. Coleccion: Nombre base usado por la demo local.
# 2. Espacio HNSW: Distancia aplicada por la coleccion en ChromaDB.
# 3. Resultados: Cantidad de vecinos recuperados por defecto.
COLLECTION_NAME = "chromadb_cheat_sheet_demo"
HNSW_SPACE = "cosine"
DEFAULT_N_RESULTS = 3
CRUD_DEMO_ID = "doc_99"

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
RAG_SUMMARY_LINES = [
    "RAG: Recupera contexto externo para generar respuestas mas precisas y con menos alucinaciones.",
    "Context Window: El modelo no puede recibir toda la informacion en un unico prompt.",
    "Vector Database: Aporta almacenamiento retrieval rapido y contexto para augmentar prompts.",
]
RAG_PIPELINE_LINES = [
    "Paso 1: Cargar documentos y dividirlos en fragmentos utiles.",
    "Paso 2: Generar embeddings de documentos y consultas.",
    "Paso 3: Guardar vectores y texto asociado en una base vectorial.",
    "Paso 4: Recuperar los fragmentos mas relevantes para la consulta.",
    "Paso 5: Unir contexto y prompt antes de llamar al LLM.",
]
RAG_RESPONSIBILITY_LINES = [
    "Embeddings: Puede generar vectores de documentos y consultas si se configura la funcion adecuada.",
    "Storage: Mantiene ids metadatos documentos y vectores en una misma coleccion.",
    "Retrieval: Busca vecinos similares con indices como HNSW y filtros por metadatos.",
    "Grounding: Devuelve el texto recuperado para enriquecer el prompt final.",
]
RAG_PITFALL_LINES = [
    "Embedding Model Drift: Usar modelos distintos para documentos y consultas rompe el retrieval.",
    "Chunking Deficiente: Fragmentos muy pequenos o muy grandes degradan la relevancia.",
    "Reindexado Olvidado: Cambiar metrica o embeddings exige recrear o clonar la coleccion.",
    "Sobreconfianza: El primer resultado no siempre es la mejor respuesta y debe evaluarse.",
]
RECOMMENDATION_SUMMARY_LINES = [
    "Recommendation Systems: Usan similitud vectorial para sugerir productos contenidos y perfiles cercanos.",
    "Metadata Filters: Permiten combinar preferencias duras con similitud semantica.",
    "ChromaDB: Sirve para retrieval de candidatos y para refinar recomendaciones por contexto.",
]
