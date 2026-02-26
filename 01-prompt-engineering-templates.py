# --- LEYENDA ---
# 1.        LangChain: Prompts • Memory • Chains • Agents • Tools • RAG • LLMs
# 2.   LangChain Core: PromptTemplate • Runnable/LCEL • ChatModel/LLM • OutputParser
# 3. LangChain Ollama: llama3.1:latest • mistral:latest • phi3.5:latest

# --- INSTALACIÓN ---
# 1.           Ollama: irm https://ollama.com/install.ps1 | iex
# 2.  LLM llama3.2:3b: ollama pull llama3.2:3b
# 3.       LangChain*: pip install -U langchain langchain-core langchain-ollama
# 4. LangChain Ollama: pip install -U langchain-ollama

# --- VERIFICACIÓN ---
# 1.           Ollama: ollama --version
# 2.  Ollama Servidor: ollama serve
# 3.        LangChain: pip show langchain
# 4.   Ollama Modelos: ollama list

# --- DEPENDENCIAS ---
# 1.        OllamaLLM: Importar desde langchain_ollama.
from langchain_ollama import OllamaLLM

# --- EJERCICIO 1: PROMPT ENGINEERING ---
# Función para cargar el modelo:
# @params: prompt_txt: Texto del prompt.
# @params: params: Diccionario de parámetros.
# @return: Respuesta del modelo.
def llm_model(prompt_txt, params=None):
    # Parámetros por defecto.
    default_params = {
        # Máximo de tokens a generar en la respuesta.
        # 1 token ≈ 0.75 palabras en español.
        # 256 tokens ≈ 180–200 palabras aproximadamente.
        # Solo afecta a los tokens generados (no al prompt).
        "max_new_tokens": 256,

        # Temperatura del modelo (0.0 a 2.0).
        # Controla la aleatoriedad / creatividad.
        #       0.0 → Muy determinista, respuestas casi idénticas.
        # 0.3 - 0.7 → Balanceado (ideal para uso técnico).
        #      1.0+ → Más creativo y variado.
        #      >1.5 → Puede generar respuestas incoherentes.
        "temperature": 0.5,

        # Top-p (Nucleus Sampling) (0.0 a 1.0).
        # Limita el conjunto de palabras candidatas según probabilidad acumulada.
        # Valores bajos → Más conservador y repetitivo.
        # Valores altos → Más variedad y naturalidad.
        #    0.8 - 0.95 → Suele ser un rango equilibrado.
        #           0.2 → Es bastante restrictivo.
        "top_p": 0.2,          

        # Top-k (1 a 100+ según modelo).
        # Limita el número máximo de palabras candidatas consideradas.
        #            1  → Solo la palabra más probable (muy determinista).
        #         20-50 → Buen equilibrio entre precisión y variedad.
        # Valores altos → Más diversidad.
        #   Con top_k=1 → El modelo será muy rígido.
        "top_k": 1,            
    }

    # Actualiza los parámetros por defecto con los parámetros proporcionados.
    # None no es un diccionario, por lo que no se puede actualizar.
    if params:
        default_params.update(params)

    # Inicializa el modelo Ollama.
    llm = OllamaLLM(
        # Modelo a utilizar.
        model="llama3.2:3b",
        # Temperatura del modelo.
        temperature=default_params["temperature"],
        # Top-p del modelo.
        top_p=default_params["top_p"],
        # Top-k del modelo.
        top_k=default_params["top_k"],
        # Máximo de tokens a generar en la respuesta.
        num_predict=default_params["max_new_tokens"],
    )
    return llm.invoke(prompt_txt)

# Imprime la respuesta del modelo.
# python 01-prompt-engineering-templates.py
print(llm_model("Hola, ¿cómo estás?", params=None))

# --- EJERCICIO 2: ESCALADO DEL EJERCICIO 1 ---
# 2.1. Ajustar parámetros para controlar el comportamiento de la respuesta.
def run_baseline():
    params = {"max_new_tokens": 128, "temperature": 0.5, "top_p": 0.2, "top_k": 1}
    print(llm_model("El viento está ", params))

# 2.2. Diseñar prompts para tareas específicas con diccionario.
def run_task_prompts():
    # Modificar los parámetros para mejorar la respuesta.
    params = {"max_new_tokens": 120, "temperature": 0.3, "top_p": 0.9, "top_k": 40}

    # Definir los prompts.
    prompts = {
        "sentiment": "Clasifica como Positivo o Negativo: 'La película fue increíble.'",
        "summary": "Resume en una frase: El cambio climático...",
        "translation": "Traduce al español: 'Artificial intelligence is changing healthcare.'",
    }

    # Iterar sobre los prompts y generar las respuestas.
    for name, prompt in prompts.items():
        print(f"\n--- {name.upper()} ---")
        print(llm_model(prompt, params))

# 2.3. One-Shot Prompting: Guiar la salida con un solo ejemplo mediante un diccionario.
def run_one_shot_prompts():
    params = {"max_new_tokens": 140, "temperature": 0.3, "top_p": 0.9, "top_k": 40}

    prompts = {
        "formal_email": (
            "Escribe un correo formal para solicitar una reunion con un cliente la proxima semana.\n\nCorreo:"
        ),
        "technical_concept": (
            "Explica el concepto de aprendizaje automatico en terminos sencillos para un principiante.\n\nExplicacion:"
        ),
        "keyword_extraction": (
            "Extrae las palabras clave principales del siguiente texto:\n"
            "Artificial intelligence and machine learning are rapidly transforming industries worldwide.\n\n"
            "Palabras clave:"
        ),
    }

    for name, prompt in prompts.items():
        print(f"\n--- ONE SHOT {name.upper()} ---")
        print(llm_model(prompt, params))

# 2.4. Few-Shot Prompting: Guiar la salida con pocos ejemplos.
def run_few_shot():
    params = {"max_new_tokens": 60, "temperature": 0.1, "top_p": 0.9, "top_k": 40}

    prompt = """
        Inglés: "How are you?"
        Francés: "Comment ça va?"
        Inglés: "Where is the train station?"
        Francés:"""

    print("\n--- FEW SHOT ---")
    print(llm_model(prompt, params))

# 2.5. Convención que asegura la ejecución de las funciones si se llama al propio archivo.
if __name__ == "__main__":
    run_baseline()
    run_task_prompts()
    run_one_shot_prompts()
    run_few_shot()
