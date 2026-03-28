# --- DEPENDENCIAS ---
OLLAMA_TAGS_URL = "http://127.0.0.1:11434/api/tags"
OLLAMA_MODEL_CANDIDATES = (
    "qwen2.5:7b",
    "llama3.2:3b",
    "mistral",
)

LAB_INTRODUCTION = (
    "Practica 27 adapta el lab de ReAct con LangGraph a un spike local con "
    "StateGraph, ChatOllama y herramientas reales con fallback sin API keys."
)

DEFAULT_WEATHER_QUERY = "What's the weather like in Zurich, and what should I wear based on the temperature?"
DEFAULT_CALC_QUERY = "Calculate 15% of 250 plus the square root of 144."
DEFAULT_NEWS_QUERY = "Find recent AI news and summarize the top 3 articles."

SEARCH_MAX_RESULTS = 3

SYSTEM_PROMPT = (
    "You are a helpful AI assistant that thinks step by step and uses tools when needed. "
    "First decide what information you need. Use tools when the task requires current data, "
    "structured calculation, or domain specific processing. After receiving tool results, reason "
    "about them and either call another tool or answer clearly. Explain your approach briefly but do not expose chain of thought."
)