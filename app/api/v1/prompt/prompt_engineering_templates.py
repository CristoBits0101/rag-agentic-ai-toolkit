# --- LEYENDA ---
# 1.        LangChain: Prompts, Memory, Chains, Agents, Tools, RAG, LLMs
# 2.   LangChain Core: PromptTemplate, Runnable/LCEL, ChatModel/LLM, OutputParser
# 3. LangChain Ollama: llama3.1:latest, mistral:latest, phi3.5:latest

# --- INSTALACION ---
# 1.           Ollama: irm https://ollama.com/install.ps1 | iex
# 2.  LLM llama3.2:3b: ollama pull llama3.2:3b
# 3.       LangChain*: pip install -U langchain langchain-core langchain-ollama
# 4. LangChain Ollama: pip install -U langchain-ollama

# --- VERIFICACION ---
# 1.           Ollama: ollama --version
# 2.  Ollama Servidor: ollama serve
# 3.        LangChain: pip show langchain
# 4.   Ollama Modelos: ollama list

# --- DEPENDENCIAS ---
# 1.        OllamaLLM: Para interactuar con modelos Ollama desde LangChain.
# 2.   PromptTemplate: Para crear plantillas de prompts con variables dinamicas.

# Nota:
# Este modulo mantiene intactos los comentarios pedagogicos de los ejercicios.
# La ejecucion real por API se implementa en:
# - app/service/prompt_service.py
# - app/api/v1/prompt/router.py


# --- EJERCICIO 1: PROMPT ENGINEERING ---

# 1.1) Funcion para cargar el modelo:
# @params: prompt_txt: Texto del prompt.
# @params: params: Diccionario de parametros.
# @return: Respuesta del modelo.
#
# Parametros por defecto explicados:
# - max_new_tokens: Maximo de tokens a generar en la respuesta.
#   1 token ~= 0.75 palabras en espanol.
# - temperature: Controla aleatoriedad/creatividad (0.0 a 2.0).
# - top_p: Nucleus sampling (0.0 a 1.0).
# - top_k: Numero maximo de palabras candidatas consideradas.

# 1.2) Imprime la respuesta del modelo.
# python 01-prompt-engineering-templates.py


# --- EJERCICIO 2: CREACION DE PROMPTS PARA TAREAS ESPECIFICAS ---

# 2.1) Ajustar parametros para controlar el comportamiento de la respuesta.
# 2.2) Disenar prompts para tareas especificas con diccionario.
# 2.3) One-Shot Prompting: Guiar la salida con un solo ejemplo.
# 2.4) Few-Shot Prompting: Guiar la salida con pocos ejemplos.


# --- EJERCICIO 3: CREACION DE PROMPTS PARA EXPLICAR PROCESOS PASO A PASO ---

# 3.1) Solicitar explicar un proceso.
# 3.2) Solicitar instrucciones.
# 3.3) Generar respuestas para ambos prompts.
# 3.4) Razonamiento guiado con salida mas extensa.


# --- EJERCICIO 4: LOGICA LCEL ---

# 4.1) Funcion para construir un chain LCEL con PromptTemplate y OllamaLLM.
# 4.2) Ejercicios con LCEL:
# - Chistes dinamicos
# - Resumenes dinamicos
# - Preguntas y respuestas dinamicas
# - Clasificacion dinamica
# - Generacion SQL dinamica


# --- EJERCICIO 5: RAZONAMIENTO GUIADO + ANALISIS ESTRUCTURADO EN LCEL ---

# 5.1) LLM dedicado para este ejercicio con salida mas extensa.
# 5.2) Plantilla para analizar resenas con formato fijo.
# 5.3) Formateador explicito + parser de texto para cadena LCEL completa.
# 5.4) Procesar multiples resenas (batch simple).
# 5.5) Prompt de razonamiento paso a paso con formato de salida.


DEFAULT_BASELINE_PROMPT = "El viento esta "

DEFAULT_TASK_PROMPTS = {
    "sentiment": "Clasifica como Positivo o Negativo: 'La pelicula fue increible.'",
    "summary": "Resume en una frase: El cambio climatico afecta a ecosistemas, economias y salud.",
    "translation": "Traduce al espanol: 'Artificial intelligence is changing healthcare.'",
}

DEFAULT_ONE_SHOT_PROMPTS = {
    "formal_email": "Escribe un correo formal para solicitar una reunion con un cliente la proxima semana.\\n\\nCorreo:",
    "technical_concept": "Explica el concepto de aprendizaje automatico en terminos sencillos para un principiante.\\n\\nExplicacion:",
    "keyword_extraction": "Extrae las palabras clave principales del siguiente texto:\\nArtificial intelligence and machine learning are rapidly transforming industries worldwide.\\n\\nPalabras clave:",
}

DEFAULT_FEW_SHOT_PROMPT = (
    'Ingles: "How are you?"\\n'
    'Frances: "Comment ca va?"\\n'
    'Ingles: "Where is the train station?"\\n'
    "Frances:"
)

DEFAULT_DECISION_PROMPT = "Explica el proceso de toma de decisiones paso a paso para elegir el mejor portatil para comprar."

DEFAULT_SANDWICH_PROMPT = "Explica paso a paso como hacer un sandwich simple."

DEFAULT_REASONING_PROMPT = (
    "Cuando tenia 6 anos, mi hermana tenia la mitad de mi edad. Ahora tengo 70, que edad tiene mi hermana?\\n\\n"
    "Proporciona tres calculos y explicaciones independientes y, a continuacion, "
    "determina el resultado mas coherente."
)

DEFAULT_REVIEW_TEMPLATE = """
Analiza la siguiente resena de producto:
"{review}"

Proporciona tu analisis en el siguiente formato:
- Sentimiento: (positivo, negativo o neutral)
- Caracteristicas clave mencionadas: (lista de caracteristicas)
- Resumen: (resumen en una frase)
""".strip()

DEFAULT_REASONING_TEMPLATE = """
Resuelve el siguiente problema paso a paso y al final da una respuesta final corta.

Problema:
{problem}

Formato:
1) Datos
2) Razonamiento
3) Respuesta final
""".strip()
