# --- DEPENDENCIAS ---
# 1.    OllamaLLM: Para interactuar con modelos Ollama desde LangChain.
# 2. Configuracion: Para leer el modelo y parametros por defecto.
from langchain_ollama import OllamaLLM

from prompting_config import DEFAULT_LLM_PARAMS
from prompting_config import MODEL_NAME


# Construye un modelo Ollama con parametros explicitos.
def build_llm(max_new_tokens=256, temperature=0.5, top_p=0.2, top_k=1):
    # Inicializa el modelo Ollama con la configuracion recibida.
    return OllamaLLM(
        model=MODEL_NAME,
        temperature=temperature,
        top_p=top_p,
        top_k=top_k,
        num_predict=max_new_tokens,
    )


# Ejecuta un prompt directo usando el modelo local.
def llm_model(prompt_txt, params=None):
    # Parte de los parametros por defecto de la practica.
    merged_params = dict(DEFAULT_LLM_PARAMS)

    # Actualiza los parametros si llegan valores personalizados.
    if params:
        merged_params.update(params)

    # Construye el modelo con los parametros finales.
    llm = build_llm(
        max_new_tokens=merged_params["max_new_tokens"],
        temperature=merged_params["temperature"],
        top_p=merged_params["top_p"],
        top_k=merged_params["top_k"],
    )

    # Devuelve la respuesta generada por el modelo.
    return llm.invoke(prompt_txt)


# Construye un modelo orientado a ejercicios LCEL.
def build_lcel_llm(max_new_tokens=256, temperature=0.3, top_p=0.9, top_k=40):
    # Reutiliza el mismo constructor con parametros adecuados para LCEL.
    return build_llm(
        max_new_tokens=max_new_tokens,
        temperature=temperature,
        top_p=top_p,
        top_k=top_k,
    )
