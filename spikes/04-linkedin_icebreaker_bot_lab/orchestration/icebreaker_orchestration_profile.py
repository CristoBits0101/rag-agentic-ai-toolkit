# --- DEPENDENCIAS ---
# 1. Configuracion: Para usar el modelo por defecto.
# 2. Pipeline: Para leer y rotular el perfil mock.
# 3. QA: Para generar hechos iniciales y responder preguntas.
# 4. Retrieval: Para asegurar que el perfil este indexado.
from config.icebreaker_config import DEFAULT_LLM_MODEL
from pipeline.icebreaker_profile_pipeline import build_profile_label
from pipeline.icebreaker_profile_pipeline import load_profile_data
from orchestration.icebreaker_orchestration_qa import answer_user_query
from orchestration.icebreaker_orchestration_qa import generate_initial_facts
from orchestration.icebreaker_orchestration_retrieval import get_profile_retriever

# --- ORQUESTACION ---
# 1.1. Funcion para preparar un perfil y generar el resumen inicial.
def process_profile(profile_key: str, model_name: str):
    # Usa el modelo por defecto si la interfaz no envia uno.
    active_model = model_name or DEFAULT_LLM_MODEL
    # Carga el perfil para validar que exista.
    profile_data = load_profile_data(profile_key)
    # Asegura que el perfil quede indexado antes del primer prompt.
    get_profile_retriever(profile_key)
    # Genera los tres hechos iniciales del perfil seleccionado.
    facts = generate_initial_facts(profile_key, active_model)
    # Construye un encabezado corto para la interfaz.
    header = build_profile_label(profile_data)

    # Devuelve el resumen y los valores de estado para el chat.
    return (
        f"Perfil cargado: {header}\n\nTres hechos interesantes:\n\n{facts}",
        profile_key,
        active_model,
        [],
    )


# 1.2. Funcion para conversar con el perfil activo.
def chat_with_profile(
    active_profile_key: str,
    active_model_name: str,
    user_query: str,
    chat_history,
):
    # Inicializa el historial si Gradio todavia no envio mensajes.
    history = chat_history or []

    # Exige procesar un perfil antes de abrir el chat.
    if not active_profile_key:
        return history + [[user_query, "Procesa un perfil antes de preguntar."]], ""

    # Ignora entradas vacias para no ensuciar el chat.
    if not user_query or not user_query.strip():
        return history, ""

    # Genera una respuesta basada solo en el contexto recuperado.
    answer = answer_user_query(
        active_profile_key,
        user_query,
        active_model_name or DEFAULT_LLM_MODEL,
    )

    # Devuelve el historial actualizado y limpia la caja de entrada.
    return history + [[user_query, answer]], ""
