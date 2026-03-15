# --- DEPENDENCIAS ---
# 1. PromptTemplate: Para crear plantillas con formato fijo.
# 2. RunnableLambda: Para formatear entradas antes de invocar el modelo.
# 3. StrOutputParser: Para normalizar la salida como texto.
# 4.   Modelo LCEL: Para construir el modelo usado en el ejercicio.
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

from models.prompting_model_gateway import build_lcel_llm


# Ejecuta el ejercicio de razonamiento y analisis estructurado.
def run_exercise_5_reasoning_and_reviews():
    # Crea un modelo con salida mas extensa.
    llm = build_lcel_llm(max_new_tokens=512, temperature=0.2, top_p=0.9, top_k=40)
    # Define la plantilla para analizar resenas.
    review_template = """
Analiza la siguiente resena de producto:
"{review}"

Proporciona tu analisis en el siguiente formato:
- Sentimiento: positivo negativo o neutral
- Caracteristicas clave mencionadas: lista de caracteristicas
- Resumen: resumen en una frase
"""
    review_prompt = PromptTemplate.from_template(review_template)

    # Formatea el prompt antes de pasarlo al modelo.
    def format_review_prompt(variables):
        return review_prompt.format(**variables)

    review_analysis_chain = RunnableLambda(format_review_prompt) | llm | StrOutputParser()
    reviews = [
        "I love this smartphone! The camera quality is exceptional and the battery lasts all day. The only downside is that it heats up a bit during gaming.",
        "This laptop is terrible. It's slow, crashes frequently, and the keyboard stopped working after just two months. Customer service was unhelpful.",
    ]

    # Recorre e imprime el analisis de cada resena.
    for review in reviews:
        result = review_analysis_chain.invoke({"review": review})
        print("=== EX5 REVIEW ===")
        print("Review:", review)
        print("Analysis:", result)
        print("-" * 60)

    # Define la plantilla del problema de razonamiento.
    reasoning_template = """
Resuelve el siguiente problema paso a paso y al final da una respuesta final corta.

Problema:
{problem}

Formato:
1) Datos
2) Razonamiento
3) Respuesta final
"""
    reasoning_prompt = PromptTemplate.from_template(reasoning_template)

    # Formatea el prompt de razonamiento antes de invocarlo.
    def format_reasoning_prompt(variables):
        return reasoning_prompt.format(**variables)

    reasoning_chain = RunnableLambda(format_reasoning_prompt) | llm | StrOutputParser()
    problem = "Cuando tenia 6 anos, mi hermana tenia la mitad de mi edad. Ahora tengo 70. Cuantos anos tiene mi hermana?"
    reasoning_result = reasoning_chain.invoke({"problem": problem})

    print("=== EX5 REASONING ===")
    print("Problema:", problem)
    print("Resolucion:", reasoning_result)
    print()
