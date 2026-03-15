# Plantillas base por ejercicio (solo contenido de prompts).

# --- EJERCICIO 2: PROMPTS PARA TAREAS ESPECIFICAS ---
# 2.1) Ajustar parámetros para controlar el comportamiento de la respuesta.
DEFAULT_BASELINE_PROMPT = "El viento esta "

# 2.2) Diseñar prompts para tareas específicas con diccionario.
DEFAULT_TASK_PROMPTS = {
    "sentiment": "Clasifica como Positivo o Negativo: 'La pelicula fue increible.'",
    "summary": "Resume en una frase: El cambio climatico afecta a ecosistemas, economias y salud.",
    "translation": "Traduce al espanol: 'Artificial intelligence is changing healthcare.'",
}

# 2.3) One-Shot Prompting: Guiar la salida con un solo ejemplo.
DEFAULT_ONE_SHOT_PROMPTS = {
    "formal_email": "Escribe un correo formal para solicitar una reunion con un cliente la proxima semana.\\n\\nCorreo:",
    "technical_concept": "Explica el concepto de aprendizaje automatico en terminos sencillos para un principiante.\\n\\nExplicacion:",
    "keyword_extraction": "Extrae las palabras clave principales del siguiente texto:\\nArtificial intelligence and machine learning are rapidly transforming industries worldwide.\\n\\nPalabras clave:",
}

# 2.4) Few-Shot Prompting: Guiar la salida con pocos ejemplos.
DEFAULT_FEW_SHOT_PROMPT = (
    'Ingles: "How are you?"\\n'
    'Frances: "Comment ca va?"\\n'
    'Ingles: "Where is the train station?"\\n'
    "Frances:"
)

# --- EJERCICIO 3: PROMPTS PASO A PASO ---
# 3.1) Solicitar explicar un proceso.
DEFAULT_DECISION_PROMPT = "Explica el proceso de toma de decisiones paso a paso para elegir el mejor portatil para comprar."

# 3.2) Solicitar instrucciones.
DEFAULT_SANDWICH_PROMPT = "Explica paso a paso como hacer un sandwich simple."

# 3.4) Razonamiento guiado con salida mas extensa.
DEFAULT_REASONING_PROMPT = (
    "Cuando tenia 6 anos, mi hermana tenia la mitad de mi edad. Ahora tengo 70, que edad tiene mi hermana?\\n\\n"
    "Proporciona tres calculos y explicaciones independientes y, a continuacion, "
    "determina el resultado mas coherente."
)

# --- EJERCICIO 5: PLANTILLAS DE ANALISIS Y RAZONAMIENTO ---
# 5.2) Plantilla para analizar resenas con formato fijo.
DEFAULT_REVIEW_TEMPLATE = """
Analiza la siguiente resena de producto:
"{review}"

Proporciona tu analisis en el siguiente formato:
- Sentimiento: (positivo, negativo o neutral)
- Caracteristicas clave mencionadas: (lista de caracteristicas)
- Resumen: (resumen en una frase)
""".strip()

# 5.5) Prompt de razonamiento paso a paso con formato de salida.
DEFAULT_REASONING_TEMPLATE = """
Resuelve el siguiente problema paso a paso y al final da una respuesta final corta.

Problema:
{problem}

Formato:
1) Datos
2) Razonamiento
3) Respuesta final
""".strip()
