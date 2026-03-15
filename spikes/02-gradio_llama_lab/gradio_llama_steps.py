# --- DEPENDENCIAS ---
# 1. Modelo Llama: Para ejecutar la consulta al modelo local.
from gradio_llama_model import get_llama_model

# Objetivos disponibles para la tarea final con Llama.
PROMPTS_BY_GOAL = {
    "Explicar": "Explica el contenido con lenguaje claro y directo.",
    "Resumir": "Resume el contenido en una sola frase.",
    "Traducir": "Traduce el contenido al espanol.",
}


# Valida una interaccion numerica minima.
def add_numbers(first_number: float, second_number: float) -> float:
    # Devuelve la suma directa de los dos valores introducidos.
    return first_number + second_number


# Construye una frase desde varios componentes.
def build_sentence(
    quantity: int,
    role: str,
    countries: list[str],
    place: str,
    activities: list[str],
    morning: bool,
) -> str:
    # Obliga a seleccionar al menos un pais para evitar una frase incompleta.
    if not countries:
        return "Selecciona al menos un pais."

    # Obliga a seleccionar al menos una actividad para mantener sentido en la salida.
    if not activities:
        return "Selecciona al menos una actividad."

    # Convierte los valores del formulario en texto listo para mostrar.
    time_of_day = "manana" if morning else "noche"
    countries_text = " y ".join(countries)
    activities_text = " y ".join(activities)

    # Construye una sola frase final con el contenido del formulario.
    return (
        f"{quantity} {role.lower()} de {countries_text} fueron a {place} "
        f"donde {activities_text} hasta la {time_of_day}."
    )


# Ejecuta una tarea minima con Llama.
def run_llama_step(goal: str, user_text: str) -> str:
    # Limpia espacios para evitar enviar prompts vacios al modelo.
    cleaned_text = user_text.strip()

    if not cleaned_text:
        return "Escribe una pregunta o un texto."

    # Une objetivo y contenido en un prompt corto y directo.
    prompt = (
        f"{PROMPTS_BY_GOAL[goal]}\n\n"
        f"Contenido:\n{cleaned_text}\n\n"
        "Respuesta:"
    )

    try:
        # Ejecuta el prompt contra Llama local servido por Ollama.
        response = get_llama_model().invoke(prompt)
    except Exception as exc:
        # Devuelve el error como texto para que se vea dentro de la interfaz.
        return f"No se pudo ejecutar Llama: {exc}"

    # Normaliza la salida final antes de mostrarla en Gradio.
    return str(response).strip()
