# --- DEPENDENCIAS ---
OLLAMA_TAGS_URL = "http://127.0.0.1:11434/api/tags"
OLLAMA_MODEL_CANDIDATES = (
    "qwen2.5:7b",
    "llama3.2:3b",
    "mistral",
)

MAX_REFLECTION_MESSAGES = 6

LAB_INTRODUCTION = (
    "Practica 25 adapta el lab de Reflection Agent con LangGraph a un spike "
    "local con MessageGraph y ChatOllama."
)

SAMPLE_LINKEDIN_REQUEST = (
    "Write a LinkedIn post announcing that I got a software developer job at IBM "
    "under 160 characters."
)

GENERATION_SYSTEM_PROMPT = (
    "You are a professional LinkedIn content assistant tasked with crafting "
    "engaging, insightful, and well structured LinkedIn posts. Generate the best "
    "LinkedIn post possible for the user's request. If the user provides feedback "
    "or critique, respond with a refined version of your previous attempts, "
    "improving clarity, tone, credibility, and engagement."
)

REFLECTION_SYSTEM_PROMPT = (
    "You are a professional LinkedIn content strategist and thought leadership "
    "expert. Critically evaluate the given LinkedIn post and provide a concise and "
    "actionable critique. Assess quality professionalism structure tone clarity "
    "readability engagement potential relevance formatting hashtags and call to "
    "action. Explain strengths and weaknesses and provide specific improvement "
    "instructions that can be used in the next revision."
)