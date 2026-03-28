# --- DEPENDENCIAS ---

OLLAMA_API_URL = "http://127.0.0.1:11434/api/chat"
OLLAMA_TAGS_URL = "http://127.0.0.1:11434/api/tags"
OLLAMA_MODEL_CANDIDATES = (
    "qwen2.5:7b",
    "llama3.2:3b",
    "mistral",
)

DATAWIZARD_INTRODUCTION = (
    "Practica 19 adapta DataWizard con datasets locales herramientas de analisis "
    "y un modelo real servido por Ollama como executor principal."
)

DATAWIZARD_SYSTEM_PROMPT = (
    "You are DataWizard. Always use tools to inspect local CSV datasets. If a dataset "
    "name is unknown list the available CSV files first. Preload datasets before "
    "summarizing them or before calling DataFrame methods or model evaluation tools. "
    "Use one tool call at a time and rely on tool results instead of guessing."
)

BASELINE_QUERY = (
    "Can you summarize the datasets and tell me which one is classification or regression?"
)

DEFAULT_DATAWIZARD_QUERIES = [
    "What datasets are available?",
    "Can you summarize the datasets and tell me which one is classification or regression?",
    "Show me the first rows of classification-dataset.csv.",
    "Evaluate classification-dataset.csv using target column will_buy.",
    "Evaluate regression-dataset.csv using target column weekly_sales_k.",
]

MAX_DATAWIZARD_STEPS = 4
