# --- DEPENDENCIAS ---
from pathlib import Path

SPIKE_ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS_DIR = SPIKE_ROOT / "artifacts"
CACHE_DIR = ARTIFACTS_DIR / "cache"
CHROMA_DB_PATH = ARTIFACTS_DIR / "chroma_db"
EXAMPLES_DIR = SPIKE_ROOT / "examples"

MAX_TOTAL_SIZE = 30 * 1024 * 1024
CACHE_EXPIRE_DAYS = 7
VECTOR_SEARCH_K = 4
RELEVANCE_TOP_K = 4
HYBRID_RETRIEVER_WEIGHTS = [0.45, 0.55]
LOCAL_EMBEDDING_DIMENSION = 128
MAX_CORRECTION_LOOPS = 2

LAB_INTRODUCTION = (
    "Practica 28 adapta DocChat a un spike local con parser estructurado, "
    "retrieval hibrido, workflow multiagente en LangGraph y UI Gradio opcional."
)

EXAMPLES = {
    "Google Environmental Report Excerpt": {
        "question": "What is the Singapore second facility PUE and what is Asia Pacific CFE?",
        "file_paths": [str(EXAMPLES_DIR / "google_environment_report_excerpt.md")],
    },
    "DeepSeek Technical Report Excerpt": {
        "question": "What benchmark score is mentioned for DeepSeek R1 on math evaluation?",
        "file_paths": [str(EXAMPLES_DIR / "deepseek_r1_technical_report_excerpt.md")],
    },
}