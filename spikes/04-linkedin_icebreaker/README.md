# Practica 04 LinkedIn Icebreaker Bot

## Leyenda

1. Datos mock locales: Perfiles tipo LinkedIn guardados en JSON para evitar APIs externas.
2. LangChain Ollama y Chroma: Flujo RAG local para retrieval respuestas y generacion de icebreakers.
3. Gradio: Interfaz simple para procesar un perfil demo y conversar sobre su experiencia.

## Roles de Archivos

- `main.py`: Punto de entrada de la practica.
- `config/icebreaker_config.py`: Constantes de configuracion prompts y rutas.
- `data/*.json`: Perfiles mock usados por la practica.
- `models/icebreaker_models.py`: Acceso al LLM de Ollama y al modelo de embeddings.
- `orchestration/icebreaker_orchestration_profile.py`: Orquestacion de carga del perfil y del chat.
- `orchestration/icebreaker_orchestration_qa.py`: Construccion de contexto y respuestas.
- `orchestration/icebreaker_orchestration_retrieval.py`: Indexacion local y retriever.
- `pipeline/icebreaker_profile_pipeline.py`: Carga del JSON y division en trozos.
- `state/icebreaker_state.py`: Estado compartido del retriever y embeddings.
- `ui/icebreaker_ui.py`: Construccion de la interfaz Gradio.

## Instalacion

1. Ollama: `irm https://ollama.com/install.ps1 | iex`.
2. LLM local: `ollama pull llama3.2:3b`.
3. Embeddings: `ollama pull nomic-embed-text`.
4. Dependencias: `pip install -U gradio langchain langchain-community langchain-core langchain-ollama chromadb`.

## Verificacion

1. Ollama: `ollama --version`.
2. Ollama Servidor: `ollama serve`.
3. Ollama Modelos: `ollama list`.
4. Compilacion: `python -m compileall spikes\04-linkedin_icebreaker`.

## Ejecucion

1. Activar entorno: `.\venv\Scripts\Activate.ps1`.
2. Lanzar la practica: `python .\spikes\04-linkedin_icebreaker\main.py`.
3. Abrir la interfaz: `http://127.0.0.1:7861`.
