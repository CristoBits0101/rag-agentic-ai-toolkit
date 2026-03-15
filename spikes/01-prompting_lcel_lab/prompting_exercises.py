# --- DEPENDENCIAS ---
# 1. Modelo Prompting: Para ejecutar prompts directos con Ollama.
from prompting_llm import llm_model


# Imprime la respuesta del ejemplo inicial.
def run_greeting_example():
    # Ejecuta un saludo minimo para validar el modelo.
    print(llm_model("Hola, como estas?", params=None))


# Ejecuta el ajuste basico de parametros.
def run_baseline():
    # Define un conjunto simple de parametros.
    params = {"max_new_tokens": 128, "temperature": 0.5, "top_p": 0.2, "top_k": 1}
    # Ejecuta el prompt base de la practica.
    print(llm_model("El viento esta ", params))


# Ejecuta varios prompts de tareas especificas.
def run_task_prompts():
    # Usa parametros mas flexibles para tareas variadas.
    params = {"max_new_tokens": 120, "temperature": 0.3, "top_p": 0.9, "top_k": 40}
    # Define los prompts a ejecutar.
    prompts = {
        "sentiment": "Clasifica como Positivo o Negativo: 'La pelicula fue increible.'",
        "summary": "Resume en una frase: El cambio climatico...",
        "translation": "Traduce al espanol: 'Artificial intelligence is changing healthcare.'",
    }

    # Recorre e imprime cada resultado.
    for name, prompt in prompts.items():
        print(f"\n--- {name.upper()} ---")
        print(llm_model(prompt, params))


# Ejecuta el bloque de one shot prompting.
def run_one_shot_prompts(
    formal_email_prompt,
    technical_concept_prompt,
    keyword_extraction_prompt,
):
    # Usa parametros mas precisos para seguir el ejemplo dado.
    params = {"max_new_tokens": 140, "temperature": 0.3, "top_p": 0.9, "top_k": 40}
    # Agrupa los prompts para iterar sobre ellos.
    prompts = {
        "formal_email_prompt": formal_email_prompt,
        "technical_concept_prompt": technical_concept_prompt,
        "keyword_extraction_prompt": keyword_extraction_prompt,
    }

    # Recorre e imprime cada resultado.
    for name, prompt in prompts.items():
        print(f"\n--- ONE SHOT {name.upper()} ---")
        print(llm_model(prompt, params))


# Ejecuta el bloque de few shot prompting.
def run_few_shot():
    # Usa parametros bajos para una salida mas controlada.
    params = {"max_new_tokens": 60, "temperature": 0.1, "top_p": 0.9, "top_k": 40}
    # Define el prompt con ejemplos previos.
    prompt = """
        Ingles: "How are you?"
        Frances: "Comment ca va?"
        Ingles: "Where is the train station?"
        Frances:"""

    print("\n--- FEW SHOT ---")
    print(llm_model(prompt, params))


# Ejecuta el ejercicio de procesos paso a paso.
def run_exercise_3_step_by_step():
    # Usa parametros amplios para respuestas explicativas.
    params = {"max_new_tokens": 220, "temperature": 0.3, "top_p": 0.9, "top_k": 40}
    # Prompt para explicar una decision.
    decision_making_prompt = """Explica el proceso de toma de decisiones paso a paso para elegir el mejor portatil para comprar.

Respuesta:
"""
    # Prompt para explicar instrucciones.
    sandwich_making_prompt = """Explica paso a paso como hacer un sandwich simple.

Instrucciones:
"""
    # Ejecuta ambos prompts y guarda las respuestas.
    responses = {
        "decision_making": llm_model(decision_making_prompt, params),
        "sandwich_making": llm_model(sandwich_making_prompt, params),
    }

    # Imprime los resultados del bloque.
    for prompt_type, response in responses.items():
        print(f"=== RESPUESTA {prompt_type.upper()} ===")
        print(response)
        print()

    # Usa un bloque extra para razonamiento mas extenso.
    params_reasoning = {
        "max_new_tokens": 512,
        "temperature": 0.2,
        "top_p": 0.9,
        "top_k": 40,
    }
    # Define un problema con varias lineas de razonamiento.
    reasoning_prompt = """Cuando tenia 6 anos, mi hermana tenia la mitad de mi edad. Ahora tengo 70, que edad tiene mi hermana?

Proporciona tres calculos y explicaciones independientes y, a continuacion, determina el resultado mas coherente.
"""
    # Ejecuta e imprime la respuesta.
    response = llm_model(reasoning_prompt, params_reasoning)
    print(f"entrada: {reasoning_prompt}\n")
    print(f"respuesta: {response}\n")
