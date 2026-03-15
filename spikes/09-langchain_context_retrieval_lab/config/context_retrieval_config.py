# --- DEPENDENCIAS ---
# 1. Path: Para resolver rutas locales del laboratorio.
from pathlib import Path

# --- RUTAS ---
SPIKE_ROOT = Path(__file__).resolve().parents[1]
DATA_DIRECTORY = SPIKE_ROOT / "data"
COMPANY_POLICIES_FILE = DATA_DIRECTORY / "company_policies.txt"
RETRIEVAL_NOTES_FILE = DATA_DIRECTORY / "langchain_retrieval_notes.txt"

# --- COLECCIONES ---
POLICY_COLLECTION_PREFIX = "policy_context_retrieval"
NOTES_COLLECTION_PREFIX = "notes_context_retrieval"
MOVIE_COLLECTION_PREFIX = "movie_context_retrieval"
PARENT_COLLECTION_PREFIX = "parent_context_retrieval"

# --- CHUNKING ---
POLICY_CHUNK_SIZE = 180
POLICY_CHUNK_OVERLAP = 20
NOTES_CHUNK_SIZE = 220
NOTES_CHUNK_OVERLAP = 20
PARENT_CHUNK_SIZE = 420
PARENT_CHUNK_OVERLAP = 40
CHILD_CHUNK_SIZE = 100
CHILD_CHUNK_OVERLAP = 10

# --- CONSULTAS ---
POLICY_QUERY = "email policy"
PARENT_QUERY = "smoking policy"
MULTI_QUERY_QUESTION = "What does the paper say about LangChain retrieval?"
SELF_QUERY_PROMPTS = [
    "I want to watch a movie rated higher than 8.5",
    "Has Greta Gerwig directed any movies about women",
    "What's a highly rated science fiction film?",
]
