# --- DEPENDENCIAS ---
# 1. Configuracion local: Este archivo solo define constantes.

# --- CONFIGURACION ---
# 1. Modelo Ollama: Modelo local usado en la practica.
MODEL_NAME = "llama3.2:3b"

# Parametros por defecto para invocaciones directas.
DEFAULT_LLM_PARAMS = {
    "max_new_tokens": 256,
    "temperature": 0.5,
    "top_p": 0.2,
    "top_k": 1,
}
