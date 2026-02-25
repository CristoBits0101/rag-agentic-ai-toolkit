# --- LEYENDA ---
# 1.        LangChain: Prompts • Memory • Chains • Agents • Tools • RAG • LLMs
# 2.   LangChain Core: PromptTemplate • Runnable/LCEL • ChatModel/LLM • OutputParser
# 3. LangChain Ollama: llama3.1:latest • mistral:latest • phi3.5:latest

# --- INSTALACIÓN ---
# 1.           Ollama: irm https://ollama.com/install.ps1 | iex
# 2.  LLM llama3.2:3b: ollama pull llama3.2:3b
# 3.        LangChain: pip install -U langchain langchain-core langchain-ollama
# 4. LangChain Ollama: pip install -U langchain-ollama

# --- VERIFICACIÓN ---
# 1.           Ollama: ollama --version
# 2.  Ollama Servidor: ollama serve
# 3.        LangChain: pip show langchain
# 4.   Ollama Modelos: ollama list

# --- DEPENDENCIAS ---
# 1.        OllamaLLM: Importar desde langchain_ollama
from langchain_ollama import OllamaLLM

# Función para cargar el modelo:
# @params: prompt_txt: Texto del prompt
# @params: params: Diccionario de parámetros
# @return: Respuesta del modelo
def llm_model(prompt_txt, params=None):
    # Parámetros por defecto
    default_params = {
        # Mínimo de tokens a generar (1 token ≈ 0.75 palabras)
        # Máximo de tokens a generar (256 tokens ≈ 180–200 palabras)
        "max_new_tokens": 256, 
        # Temperatura del modelo (0.0 a 2.0)
        #       0.0 → Muy determinista, siempre responde casi igual.
        # 0.3 - 0.7 → Balanceado (recomendado para la mayoría de usos).
        #      1.0+ → Más creativo, más impredecible.
        #      >1.5 → Puede empezar a decir cosas raras.
        "temperature": 0.5,    
        # Top-p del modelo (0.0 a 1.0)
        # 
        "top_p": 0.2,          
        # Top-k del modelo (1 a 100)
        
        "top_k": 1,            
    }

    if params:
        default_params.update(params)

    llm = OllamaLLM(
        model="llama3.2:3b",
        temperature=default_params["temperature"],
        top_p=default_params["top_p"],
        top_k=default_params["top_k"],
        num_predict=default_params["max_new_tokens"],
    )
    return llm.invoke(prompt_txt)


