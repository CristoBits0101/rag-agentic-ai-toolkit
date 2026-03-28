# --- DEPENDENCIAS ---
# 1. Path: Para resolver la ruta de los perfiles mock.
from pathlib import Path

# --- CONFIGURACION ---
# 1. Modelo LLM: Modelo local de Ollama para redactar hechos y respuestas.
# 2. Modelo Embeddings: Modelo local de Ollama para vectorizar el perfil.
# 3. Host Gradio: Direccion usada por la practica.
# 4. Puerto Gradio: Puerto usado por la practica.
DEFAULT_LLM_MODEL = "llama3.2:3b"
EMBED_MODEL_NAME = "nomic-embed-text"
LLM_MODEL_OPTIONS = ["llama3.2:3b", "mistral:latest"]
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 7861
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K = 4
COLLECTION_PREFIX = "linkedin_icebreaker"
DEFAULT_PROFILE_KEY = "ana_martinez"
PROFILE_DATA_DIR = Path(__file__).resolve().parents[1] / "data"
FACT_QUERY = "Provide three interesting facts about this person's career or education."
INITIAL_FACTS_TEMPLATE = """You are an assistant that studies a LinkedIn style profile.
Use only the context below.
If some details are missing say so briefly.
Write exactly three numbered facts about the person's career or education.
Each fact must be concrete and grounded in the context.

Context:
{context_str}

Answer:
"""
USER_QUESTION_TEMPLATE = """You answer questions about a LinkedIn style profile.
Use only the context below.
If the answer is not present say I do not know.
Keep the answer precise and factual.

Context:
{context_str}

Question:
{query_str}

Answer:
"""
