# # --- LEYENDA ---
# # 1.        LangChain: Prompts • Memory • Chains • Agents • Tools • RAG • LLMs
# # 2.   LangChain Core: PromptTemplate • Runnable/LCEL • ChatModel/LLM • OutputParser
# # 3. LangChain Ollama: llama3.1:latest • mistral:latest • phi3.5:latest

# # --- INSTALACIÓN ---
# # 1.           Ollama: irm https://ollama.com/install.ps1 | iex
# # 2.  LLM llama3.2:3b: ollama pull llama3.2:3b
# # 3.       LangChain*: pip install -U langchain langchain-core langchain-ollama
# # 4. LangChain Ollama: pip install -U langchain-ollama

# # --- VERIFICACIÓN ---
# # 1.           Ollama: ollama --version
# # 2.  Ollama Servidor: ollama serve
# # 3.        LangChain: pip show langchain
# # 4.   Ollama Modelos: ollama list

# # --- DEPENDENCIAS ---
# # 1.        OllamaLLM: Para interactuar con modelos Ollama desde LangChain.
# # 2.   PromptTemplate: Para crear plantillas de prompts con variables dinámicas.
# from langchain_ollama import OllamaLLM
# from langchain_core.prompts import PromptTemplate
# from langchain_core.runnables import RunnableLambda
# from langchain_core.output_parsers import StrOutputParser


# # --- EJERCICIO 1: PROMPT ENGINEERING ---


# # 1.1) Función para cargar el modelo:
# # @params: prompt_txt: Texto del prompt.
# # @params: params: Diccionario de parámetros.
# # @return: Respuesta del modelo.
# def llm_model(prompt_txt, params=None):
#     # Parámetros por defecto.
#     default_params = {
#         # Máximo de tokens a generar en la respuesta.
#         # 1 token ≈ 0.75 palabras en español.
#         # 256 tokens ≈ 180–200 palabras aproximadamente.
#         # Solo afecta a los tokens generados (no al prompt).
#         "max_new_tokens": 256,
#         # Temperatura del modelo (0.0 a 2.0).
#         # Controla la aleatoriedad / creatividad.
#         #       0.0 → Muy determinista, respuestas casi idénticas.
#         # 0.3 - 0.7 → Balanceado (ideal para uso técnico).
#         #      1.0+ → Más creativo y variado.
#         #      >1.5 → Puede generar respuestas incoherentes.
#         "temperature": 0.5,
#         # Top-p (Nucleus Sampling) (0.0 a 1.0).
#         # Limita el conjunto de palabras candidatas según probabilidad acumulada.
#         # Valores bajos → Más conservador y repetitivo.
#         # Valores altos → Más variedad y naturalidad.
#         #    0.8 - 0.95 → Suele ser un rango equilibrado.
#         #           0.2 → Es bastante restrictivo.
#         "top_p": 0.2,
#         # Top-k (1 a 100+ según modelo).
#         # Limita el número máximo de palabras candidatas consideradas.
#         #            1  → Solo la palabra más probable (muy determinista).
#         #         20-50 → Buen equilibrio entre precisión y variedad.
#         # Valores altos → Más diversidad.
#         #   Con top_k=1 → El modelo será muy rígido.
#         "top_k": 1,
#     }

#     # Actualiza los parámetros por defecto con los parámetros proporcionados.
#     # None no es un diccionario, por lo que no se puede actualizar.
#     if params:
#         default_params.update(params)

#     # Inicializa el modelo Ollama.
#     llm = OllamaLLM(
#         # Modelo a utilizar.
#         model="llama3.2:3b",
#         # Temperatura del modelo.
#         temperature=default_params["temperature"],
#         # Top-p del modelo.
#         top_p=default_params["top_p"],
#         # Top-k del modelo.
#         top_k=default_params["top_k"],
#         # Máximo de tokens a generar en la respuesta.
#         num_predict=default_params["max_new_tokens"],
#     )

#     return llm.invoke(prompt_txt)


# # 1.2) Imprime la respuesta del modelo.
# # python 01-prompt-engineering-templates.py
# print(llm_model("Hola, ¿cómo estás?", params=None))


# # --- EJERCICIO 2: CREACION DE PROMPTS PARA TAREAS ESPECIFICAS ---


# # 2.1) Ajustar parámetros para controlar el comportamiento de la respuesta.
# def run_baseline():
#     params = {"max_new_tokens": 128, "temperature": 0.5, "top_p": 0.2, "top_k": 1}
#     print(llm_model("El viento está ", params))


# # 2.2) Diseñar prompts para tareas específicas con diccionario.
# def run_task_prompts():
#     # Modificar los parámetros para mejorar la respuesta.
#     params = {"max_new_tokens": 120, "temperature": 0.3, "top_p": 0.9, "top_k": 40}

#     # Definir los prompts.
#     prompts = {
#         "sentiment": "Clasifica como Positivo o Negativo: 'La película fue increíble.'",
#         "summary": "Resume en una frase: El cambio climático...",
#         "translation": "Traduce al español: 'Artificial intelligence is changing healthcare.'",
#     }

#     # Iterar sobre los prompts y generar las respuestas.
#     for name, prompt in prompts.items():
#         print(f"\n--- {name.upper()} ---")
#         print(llm_model(prompt, params))


# # 2.3) One-Shot Prompting: Guiar la salida con un solo ejemplo mediante un diccionario.
# def run_one_shot_prompts(
#     formal_email_prompt, technical_concept_prompt, keyword_extraction_prompt
# ):
#     params = {"max_new_tokens": 140, "temperature": 0.3, "top_p": 0.9, "top_k": 40}

#     # ():
#     # Permite partir expresiones largas en varias líneas sin \.
#     # Deja claro el orden de evaluación en operaciones ((a + b) * c).
#     # En literales ayuda a formatear código limpio.
#     prompts = {
#         "formal_email_prompt": (formal_email_prompt),
#         "technical_concept_prompt": (technical_concept_prompt),
#         "keyword_extraction_prompt": (keyword_extraction_prompt),
#     }

#     for name, prompt in prompts.items():
#         print(f"\n--- ONE SHOT {name.upper()} ---")
#         print(llm_model(prompt, params))


# # 2.4) Few-Shot Prompting: Guiar la salida con pocos ejemplos.
# def run_few_shot():
#     params = {"max_new_tokens": 60, "temperature": 0.1, "top_p": 0.9, "top_k": 40}

#     prompt = """
#         Inglés: "How are you?"
#         Francés: "Comment ça va?"
#         Inglés: "Where is the train station?"
#         Francés:"""

#     print("\n--- FEW SHOT ---")
#     print(llm_model(prompt, params))


# # --- EJERCICIO 3: CREACION DE PROMPTS PARA EXPLICAR PROCESOS PASO A PASO ---


# def run_exercise_3_step_by_step():
#     params = {"max_new_tokens": 220, "temperature": 0.3, "top_p": 0.9, "top_k": 40}

#     # 3.1) Solicitar explicar un proceso.
#     decision_making_prompt = """Explica el proceso de toma de decisiones paso a paso para elegir el mejor portatil para comprar.

# Respuesta:
# """

#     # 3.2) Solicitar instrucciones.
#     sandwich_making_prompt = """Explica paso a paso como hacer un sandwich simple.

# Instrucciones:
# """

#     # 3.3) Generar las respuestas para ambos prompts.
#     responses = {
#         "decision_making": llm_model(decision_making_prompt, params),
#         "sandwich_making": llm_model(sandwich_making_prompt, params),
#     }

#     for prompt_type, response in responses.items():
#         print(f"=== RESPUESTA {prompt_type.upper()} ===")
#         print(response)
#         print()

#     # 3.4) Razonamiento guiado.
#     # Aumentamos el max_new_tokens para permitir respuestas más largas y detalladas.
#     params_reasoning = {
#         "max_new_tokens": 512,
#         "temperature": 0.2,
#         "top_p": 0.9,
#         "top_k": 40,
#     }

#     # Solicitar multiples caminos de razonamiento para resolver un problema y luego determinar el resultado más coherente.
#     reasoning_prompt = """Cuando tenia 6 anos, mi hermana tenia la mitad de mi edad. Ahora tengo 70, que edad tiene mi hermana?

# Proporciona tres calculos y explicaciones independientes y, a continuacion, determina el resultado mas coherente.
# """

#     # Generar la respuesta para el prompt de razonamiento guiado.
#     response = llm_model(reasoning_prompt, params_reasoning)
#     print(f"entrada: {reasoning_prompt}\n")
#     print(f"respuesta: {response}\n")


# # --- EJERCICIO 4: LOGICA LCEL ---


# # 4.1) Función para construir un chain LCEL con PromptTemplate y OllamaLLM:
# # @params: prompt_template: Texto del template con variables entre llaves {variable}.
# # @return: Chain de LCEL que puede ser invocado con invoke().
# def build_lcel_chain(prompt_template):
#     # Inicializa el modelo Ollama con parámetros por defecto.
#     llm = OllamaLLM(
#         model="llama3.2:3b",
#         temperature=0.3,
#         top_p=0.9,
#         top_k=40,
#         num_predict=256,
#     )

#     # Crea un PromptTemplate a partir de un texto con variables dinámicas entre llaves {}.
#     prompt = PromptTemplate.from_template(prompt_template)

#     # En LangChain "LCEL" significa que todo componente ejecutable es un Runnable.
#     # Un Runnable es un objeto que implementa .invoke() recibe una entrada y devuelve una salida.
#     # Construimos un Runnable Chain usando LCEL con el operador | (pipe) se encadena Runnables.
#     # Creando un chain que primero procesa el prompt introduciendo el valor de las variables al momento de la invocación.
#     # Luego se pasa el prompt formateado al LLM que genera la respuesta mediante el operador | (pipe).
#     chain = prompt | llm

#     # Se puede invocar el chain con invoke() pasando un diccionario con los valores de las variables.
#     return chain


# # 4.2) Ejercicios con LCEL
# def run_exercise_4_lcel():
#     # CHISTES DINÁMICOS
#     # Generar un Chain sobre chistes dinámicos con variables para adjetivo y contenido.
#     joke_chain = build_lcel_chain("""Cuentame un chiste {adjective} sobre {content}.""")
#     # Invocar el chain pasando un diccionario con los valores de las variables.
#     joke = joke_chain.invoke({"adjective": "gracioso", "content": "gallinas"})
#     # Imprimir el resultado.
#     print("=== LCEL JOKE ===")
#     print(joke)
#     print()

#     # RESUMENES DINÁMICOS
#     # Contenido para resumir.
#     content = (
#         "El rapido avance de la tecnologia en el siglo XXI ha transformado salud, educacion y transporte. "
#         "IA y machine learning mejoran diagnosticos, eficiencia y acceso al conocimiento."
#     )
#     # Generar un Chain para resumir contenido dinámico con una variable para el contenido a resumir.
#     summarize_chain = build_lcel_chain(
#         """Resume el siguiente contenido en una frase:\n{content}"""
#     )
#     # Invocar el chain pasando un diccionario con el contenido a resumir.
#     summary = summarize_chain.invoke({"content": content})
#     print("=== LCEL SUMMARY ===")
#     print(summary)
#     print()

#     # PREGUNTAS Y RESPUESTAS DINÁMICAS
#     # Dar contexto y pregunta para obtener respuesta.
#     qa_chain = build_lcel_chain(
#         """
# Responde la pregunta usando solo el contexto.
# Si no estas seguro, responde: No estoy seguro de la respuesta.

# Pregunta: {question}
# Contexto: {content}

# Respuesta:
# """
#     )

#     # Contenido para el contexto.
#     qa_content = (
#         "Los planetas interiores del sistema solar son Mercurio, Venus, Tierra y Marte, y son rocosos. "
#         "Los exteriores son gigantes gaseosos."
#     )

#     # Invocar el chain pasando un diccionario con la pregunta y el contexto.
#     qa_answer = qa_chain.invoke(
#         {
#             "question": "Que planetas del sistema solar son rocosos?",
#             "content": qa_content,
#         }
#     )

#     # Imprimir el resultado.
#     print("=== LCEL QA ===")
#     print(qa_answer)
#     print()

#     # CLASIFICACION DINÁMICA
#     # Dar categorias y clasificar texto en una de ellas.
#     classification_chain = build_lcel_chain(
#         """
# Clasifica el texto en una categoria de esta lista: {categories}
# Texto: {text}
# Categoria:
# """
#     )
#     category = classification_chain.invoke(
#         {
#             "text": "El concierto de anoche fue una experiencia emocionante con actuaciones excelentes.",
#             "categories": "Entretenimiento, Comida y Restaurantes, Tecnologia, Literatura, Musica",
#         }
#     )

#     # Imprimir el resultado.
#     print("=== LCEL CLASSIFICATION ===")
#     print(category)
#     print()

#     # GENERACION SQL DINÁMICA
#     # Dar descripcion para generar consulta SQL.
#     sql_chain = build_lcel_chain(
#         """
# Genera una consulta SQL basada en la descripcion.
# Descripcion: {description}
# SQL:
# """
#     )
#     sql_query = sql_chain.invoke(
#         {
#             "description": "Obtener nombre y email de clientes que compraron en los ultimos 30 dias usando tablas customers y purchases.",
#         }
#     )
#     print("=== LCEL SQL ===")
#     print(sql_query)
#     print()


# # --- EJERCICIO 5: RAZONAMIENTO GUIADO + ANALISIS ESTRUCTURADO EN LCEL ---


# def run_exercise_5_reasoning_and_reviews():
#     # 5.1) LLM dedicado para este ejercicio con salida mas extensa.
#     llm = OllamaLLM(
#         model="llama3.2:3b",
#         temperature=0.2,
#         top_p=0.9,
#         top_k=40,
#         num_predict=512,
#     )

#     # 5.2) Plantilla para analizar resenas con formato fijo.
#     review_template = """
# Analiza la siguiente resena de producto:
# "{review}"

# Proporciona tu analisis en el siguiente formato:
# - Sentimiento: (positivo, negativo o neutral)
# - Caracteristicas clave mencionadas: (lista de caracteristicas)
# - Resumen: (resumen en una frase)
# """
#     review_prompt = PromptTemplate.from_template(review_template)

#     # 5.3) Formateador explicito + parser de texto para cadena LCEL completa.
#     def format_review_prompt(variables):
#         return review_prompt.format(**variables)

#     review_analysis_chain = RunnableLambda(format_review_prompt) | llm | StrOutputParser()

#     # 5.4) Procesar multiples resenas (batch simple).
#     reviews = [
#         "I love this smartphone! The camera quality is exceptional and the battery lasts all day. The only downside is that it heats up a bit during gaming.",
#         "This laptop is terrible. It's slow, crashes frequently, and the keyboard stopped working after just two months. Customer service was unhelpful.",
#     ]

#     for review in reviews:
#         result = review_analysis_chain.invoke({"review": review})
#         print("=== EX5 REVIEW ===")
#         print("Review:", review)
#         print("Analysis:", result)
#         print("-" * 60)

#     # 5.5) Prompt de razonamiento paso a paso con formato de salida.
#     reasoning_template = """
# Resuelve el siguiente problema paso a paso y al final da una respuesta final corta.

# Problema:
# {problem}

# Formato:
# 1) Datos
# 2) Razonamiento
# 3) Respuesta final
# """
#     reasoning_prompt = PromptTemplate.from_template(reasoning_template)

#     def format_reasoning_prompt(variables):
#         return reasoning_prompt.format(**variables)

#     reasoning_chain = (
#         RunnableLambda(format_reasoning_prompt) | llm | StrOutputParser()
#     )
#     problem = "Cuando tenia 6 anos, mi hermana tenia la mitad de mi edad. Ahora tengo 70. Cuantos anos tiene mi hermana?"
#     reasoning_result = reasoning_chain.invoke({"problem": problem})

#     print("=== EX5 REASONING ===")
#     print("Problema:", problem)
#     print("Resolucion:", reasoning_result)
#     print()


# if __name__ == "__main__":
#     run_baseline()
#     run_task_prompts()
#     run_one_shot_prompts(
#         "Escribe un correo formal para solicitar una reunion con un cliente la proxima semana.\n\nCorreo:",
#         "Explica el concepto de aprendizaje automatico en terminos sencillos para un principiante.\n\nExplicacion:",
#         "Extrae las palabras clave principales del siguiente texto:\nArtificial intelligence and machine learning are rapidly transforming industries worldwide.\n\nPalabras clave:",
#     )
#     run_few_shot()
#     run_exercise_3_step_by_step()
#     run_exercise_4_lcel()
#     run_exercise_5_reasoning_and_reviews()
