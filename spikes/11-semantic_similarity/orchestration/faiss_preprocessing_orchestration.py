# --- DEPENDENCIAS ---
# 1. Regex: Para limpiar los textos de entrada.
import re

# --- PREPROCESAMIENTO ---
def preprocess_text(text: str) -> str:
    # Elimina encabezados correos signos y espacios sobrantes.
    text = re.sub(r"^From:.*\n?", "", text, flags=re.MULTILINE)
    text = re.sub(r"\S*@\S*\s?", "", text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = text.lower()
    text = re.sub(r"\s+", " ", text).strip()
    return text
