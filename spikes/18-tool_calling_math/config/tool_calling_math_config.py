# --- DEPENDENCIAS ---

OLLAMA_API_URL = "http://127.0.0.1:11434/api/chat"
OLLAMA_TAGS_URL = "http://127.0.0.1:11434/api/tags"
OLLAMA_MODEL_CANDIDATES = (
    "qwen2.5:7b",
    "llama3.2:3b",
    "mistral",
)

LAB_INTRODUCTION = (
    "Practica 18 adapta el lab de tool calling de LangChain con un modelo real "
    "servido por Ollama y un catalogo factual local."
)

TOOL_CALLING_SYSTEM_PROMPT = (
    "You are a mathematical assistant that must use tools for arithmetic or factual "
    "questions. Use one tool call at a time. For multi step questions complete the "
    "first tool call then decide the next one using the tool result. Do not invent "
    "numeric results when a tool can compute them."
)

DEFAULT_TOOL_CALLING_QUERIES = [
    "Add 25 and 15.",
    "Add 25 and 15 then multiply by 2.",
    "Subtract 100, 20 and 10.",
    "Divide 100 by 5 and then by 2.",
    "Raise 3 to the power of 4.",
    "What is the population of Canada. Multiply it by 0.75.",
]

MAX_TOOL_CALLING_STEPS = 4
