# --- DEPENDENCIAS ---
from pathlib import Path

SPIKE_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = SPIKE_ROOT / "data"
ARTIFACTS_DIR = SPIKE_ROOT / "artifacts"
SQL_SEED_PATH = DATA_DIR / "chinook.sql"
DATABASE_PATH = ARTIFACTS_DIR / "chinook.db"

OLLAMA_TAGS_URL = "http://127.0.0.1:11434/api/tags"
OLLAMA_MODEL_CANDIDATES = (
    "qwen2.5:7b",
    "llama3.2:3b",
    "mistral",
)

LAB_INTRODUCTION = (
    "Practica 23 adapta el lab de agente SQL con una base Chinook local en SQLite "
    "y un agente real de LangChain con ChatOllama."
)

SQL_AGENT_PREFIX = (
    "You are a read only SQL analyst working with a {dialect} database. "
    "Use the available tools to inspect the schema before answering when needed. "
    "Generate only SELECT statements or schema inspection queries. "
    "Never modify data or schema. "
    "Limit results to {top_k} rows unless the user asks for more."
)

SAMPLE_QUERIES = [
    {
        "title": "Album Count",
        "query": "How many albums are there in the database?",
    },
    {
        "title": "Top Customers",
        "query": "List the top 5 customers by total invoice amount.",
    },
    {
        "title": "Top Genres",
        "query": "Which 5 genres have the highest number of tracks?",
    },
]
