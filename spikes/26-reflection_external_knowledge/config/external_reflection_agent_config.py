# --- DEPENDENCIAS ---
OLLAMA_TAGS_URL = "http://127.0.0.1:11434/api/tags"
OLLAMA_MODEL_CANDIDATES = (
    "qwen2.5:7b",
    "llama3.2:3b",
    "mistral",
)

MAX_ITERATIONS = 3
SEARCH_MAX_RESULTS = 3

LAB_INTRODUCTION = (
    "Practica 26 adapta el lab de Reflection con conocimiento externo a un spike "
    "local con LangGraph, ChatOllama y busqueda Tavily opcional con fallback a Europe PMC."
)

SAMPLE_QUESTION = (
    "I am pre diabetic and have heart issues. What breakfast foods should I eat and avoid?"
)

RESPONDER_PROMPT_TEMPLATE = (
    "You are an evidence based nutrition expert. Answer the user's question with clear, "
    "practical and clinically cautious guidance. "
    "{first_instruction} "
    "Explain the physiological rationale behind your advice. "
    "Reflect on gaps or weak claims in your own answer. "
    "After the reflection list 1 to 3 search queries separately for missing evidence or clarifications. "
    "Prefer evidence relevant to glycemic control cardiovascular risk breakfast composition protein quality "
    "fiber whole foods and individual variability."
)

REVISOR_INSTRUCTIONS = (
    "Revise your previous answer using the new external evidence. Incorporate the prior critique. "
    "Use precise evidence based language and distinguish strong evidence from weaker signals. "
    "Mention uncertainty when appropriate. Add a short references section at the end using URLs. "
    "Keep the answer under 250 words and optimize for a person with pre diabetes and cardiovascular concerns."
)