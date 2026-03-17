# --- DEPENDENCIAS ---

OLLAMA_TAGS_URL = "http://127.0.0.1:11434/api/tags"
OLLAMA_MODEL_CANDIDATES = (
    "qwen2.5:7b",
    "llama3.2:3b",
    "mistral",
)

LAB_INTRODUCTION = (
    "Practica 20 adapta el lab de agentes interactivos con tools de LangChain "
    "usando ChatOllama real y un flujo manual de tool calling."
)

INTERACTIVE_TOOL_CALLING_SYSTEM_PROMPT = (
    "You are an interactive tool calling assistant. "
    "For arithmetic or tip calculations you must use the available tools. "
    "Use structured arguments. "
    "If a calculation needs a tool do not answer from memory. "
    "After tool results arrive produce a concise final answer."
)

TOOL_CALLING_RETRY_PROMPT = (
    "Retry the last request and respond by calling the appropriate tool with structured arguments."
)

DEFAULT_MANUAL_TOOL_QUERY = "What is 3 + 2?"
DEFAULT_AGENT_QUERIES = [
    "What is 3 + 2?",
    "What is 9 - 2?",
    "What is 3 times 2?",
]
DEFAULT_TIP_QUERY = "How much should I tip on $60 at 20%?"

MAX_TOOL_AGENT_STEPS = 4
