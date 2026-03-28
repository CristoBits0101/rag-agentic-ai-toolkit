# --- DEPENDENCIAS ---
import os

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

# --- MODEL ---
def build_openai_image_client():
    if OpenAI is None:
        raise RuntimeError("OpenAI is not available. Install it with pip install -U openai.")

    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required for the DALL-E practice.")

    return OpenAI(api_key=api_key)
