# --- DEPENDENCIAS ---
# 1. PromptTemplate: Para crear plantillas de prompts con variables dinamicas.
# 2.  Modelo LCEL: Para construir el modelo usado en las cadenas.
from langchain_core.prompts import PromptTemplate

from prompting_llm import build_lcel_llm


# Construye una cadena LCEL con plantilla y modelo.
def build_lcel_chain(prompt_template):
    # Inicializa el modelo con parametros adecuados para LCEL.
    llm = build_lcel_llm()
    # Crea la plantilla a partir del texto recibido.
    prompt = PromptTemplate.from_template(prompt_template)
    # Encadena la plantilla con el modelo.
    chain = prompt | llm

    # Devuelve la cadena lista para invoke.
    return chain


# Ejecuta los ejemplos del ejercicio LCEL.
def run_exercise_4_lcel():
    # Genera una cadena de chistes dinamicos.
    joke_chain = build_lcel_chain("""Cuentame un chiste {adjective} sobre {content}.""")
    joke = joke_chain.invoke({"adjective": "gracioso", "content": "gallinas"})
    print("=== LCEL JOKE ===")
    print(joke)
    print()

    # Genera una cadena para resumir contenido.
    content = (
        "El rapido avance de la tecnologia en el siglo XXI ha transformado salud, educacion y transporte. "
        "IA y machine learning mejoran diagnosticos, eficiencia y acceso al conocimiento."
    )
    summarize_chain = build_lcel_chain(
        """Resume el siguiente contenido en una frase:\n{content}"""
    )
    summary = summarize_chain.invoke({"content": content})
    print("=== LCEL SUMMARY ===")
    print(summary)
    print()

    # Genera una cadena de pregunta y respuesta con contexto.
    qa_chain = build_lcel_chain(
        """
Responde la pregunta usando solo el contexto.
Si no estas seguro, responde: No estoy seguro de la respuesta.

Pregunta: {question}
Contexto: {content}

Respuesta:
"""
    )
    qa_content = (
        "Los planetas interiores del sistema solar son Mercurio, Venus, Tierra y Marte, y son rocosos. "
        "Los exteriores son gigantes gaseosos."
    )
    qa_answer = qa_chain.invoke(
        {
            "question": "Que planetas del sistema solar son rocosos?",
            "content": qa_content,
        }
    )
    print("=== LCEL QA ===")
    print(qa_answer)
    print()

    # Genera una cadena de clasificacion.
    classification_chain = build_lcel_chain(
        """
Clasifica el texto en una categoria de esta lista: {categories}
Texto: {text}
Categoria:
"""
    )
    category = classification_chain.invoke(
        {
            "text": "El concierto de anoche fue una experiencia emocionante con actuaciones excelentes.",
            "categories": "Entretenimiento, Comida y Restaurantes, Tecnologia, Literatura, Musica",
        }
    )
    print("=== LCEL CLASSIFICATION ===")
    print(category)
    print()

    # Genera una cadena para SQL dinamico.
    sql_chain = build_lcel_chain(
        """
Genera una consulta SQL basada en la descripcion.
Descripcion: {description}
SQL:
"""
    )
    sql_query = sql_chain.invoke(
        {
            "description": "Obtener nombre y email de clientes que compraron en los ultimos 30 dias usando tablas customers y purchases.",
        }
    )
    print("=== LCEL SQL ===")
    print(sql_query)
    print()
