# --- DEPENDENCIAS ---
from config.daily_dish_chatbot_config import DEFAULT_TEXT_MODEL
from langchain_ollama import ChatOllama


def build_daily_dish_model(model_name: str = DEFAULT_TEXT_MODEL):
    return ChatOllama(model=model_name, temperature=0)