# --- DEPENDENCIAS ---
# 1. Configuracion local: Este archivo solo define constantes.

# --- CONFIGURACION ---
# 1. Modelo QA: Modelo local de Ollama para responder preguntas.
# 2. Embeddings QA: Modelo local de Ollama para representar texto en vectores.
# 3. Host Gradio: Direccion para publicar la interfaz.
# 4. Puerto Gradio: Puerto usado por la practica.
MODEL_NAME = "llama3.2:3b"
EMBED_MODEL_NAME = "nomic-embed-text"
# Define la direccion donde se publicara la interfaz.
SERVER_HOST = "0.0.0.0"
# Define el puerto donde se abrira la interfaz.
SERVER_PORT = 7860
# Define el tamano maximo de cada trozo.
CHUNK_SIZE = 1000
# Define el texto repetido entre trozos seguidos.
CHUNK_OVERLAP = 50
# Define cuantos trozos recupera la busqueda.
TOP_K = 4
# Define el nombre interno de la coleccion vectorial.
COLLECTION_NAME = "rag_pdf_qa_bot"
