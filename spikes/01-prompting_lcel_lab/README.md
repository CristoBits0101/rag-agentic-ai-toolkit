# Practica 01 Prompting LCEL

## Leyenda

1. LangChain: Prompts Memory Chains Agents Tools RAG LLMs.
2. LangChain Core: PromptTemplate Runnable LCEL ChatModel LLM OutputParser.
3. LangChain Ollama: llama3.1 latest mistral latest phi3.5 latest.

## Roles de Archivos

- `main.py`: Punto de entrada de la practica.
- `config/prompting_runtime_config.py`: Constantes y parametros por defecto.
- `models/prompting_model_gateway.py`: Acceso al modelo Ollama.
- `orchestration/prompting_orchestration_basic.py`: Orquestacion de ejercicios basicos de prompting.
- `orchestration/prompting_orchestration_lcel.py`: Orquestacion de ejercicios LCEL.
- `orchestration/prompting_orchestration_reasoning.py`: Orquestacion de ejercicios de razonamiento.

## Instalacion

1. Ollama: `irm https://ollama.com/install.ps1 | iex`.
2. LLM llama3.2:3b: `ollama pull llama3.2:3b`.
3. LangChain: `pip install -U langchain langchain-core langchain-ollama`.
4. LangChain Ollama: `pip install -U langchain-ollama`.

## Verificacion

1. Ollama: `ollama --version`.
2. Ollama Servidor: `ollama serve`.
3. LangChain: `pip show langchain`.
4. Ollama Modelos: `ollama list`.
