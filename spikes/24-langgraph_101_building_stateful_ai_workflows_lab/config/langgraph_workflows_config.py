# --- DEPENDENCIAS ---
from pathlib import Path

SPIKE_ROOT = Path(__file__).resolve().parents[1]

OLLAMA_TAGS_URL = "http://127.0.0.1:11434/api/tags"
OLLAMA_MODEL_CANDIDATES = (
    "qwen2.5:7b",
    "llama3.2:3b",
    "mistral",
)

AUTH_VALID_USERNAME = "test_user"
AUTH_VALID_PASSWORD = "secure_password"
AUTH_MAX_ATTEMPTS = 3
AUTH_DEMO_ATTEMPTS = [
    {"username": "test_user", "password": "wrongpassword"},
    {"username": "test_user", "password": "secure_password"},
]
AUTH_LOCKOUT_ATTEMPTS = [
    {"username": "test_user", "password": "wrongpassword"},
    {"username": "unknown_user", "password": "still_wrong"},
    {"username": "", "password": "secure_password"},
]

LANGGRAPH_GUIDED_PROJECT_CONTEXT = (
    "This guided project is about using LangGraph, a Python library to design "
    "state based workflows. LangGraph helps you define state schemas, implement "
    "nodes as units of work, connect them with edges and conditional edges, and "
    "support both linear and cyclical execution for agent style systems."
)

QA_RELEVANT_KEYWORDS = (
    "langgraph",
    "guided project",
    "workflow",
    "state",
    "stategraph",
    "node",
    "edge",
    "conditional edge",
    "agent",
)

QA_SAMPLE_QUESTIONS = [
    "What is LangGraph?",
    "How do conditional edges work in this guided project?",
    "What is the weather today?",
]

COUNTER_INITIAL_STATE = {"n": 1, "letter": ""}

LAB_INTRODUCTION = (
    "Practica 24 adapta el lab LangGraph 101 a un spike ejecutable con LangGraph, "
    "StateGraph y un flujo QA conectado a ChatOllama."
)