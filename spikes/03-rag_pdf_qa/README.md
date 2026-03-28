# Practica 03 RAG PDF QA Bot

## Leyenda

1. LangChain Community: PyPDFLoader Chroma RetrievalQA para construir el flujo RAG.
2. LangChain Ollama: OllamaLLM y OllamaEmbeddings para responder y vectorizar con Ollama.
3. Gradio: Interfaz simple para cargar un PDF y hacer preguntas sobre su contenido.

## Roles de Archivos

- `main.py`: Punto de entrada de la practica.
- `bootstrap/rag_bootstrap.py`: Configuracion de warnings.
- `config/rag_config.py`: Constantes de configuracion.
- `pipeline/rag_document_pipeline.py`: Carga y division del PDF en trozos.
- `models/rag_models.py`: Carga del LLM y del modelo de embeddings.
- `orchestration/rag_orchestration_qa.py`: Orquestacion principal de pregunta y respuesta.
- `orchestration/rag_orchestration_retrieval.py`: Orquestacion de indexacion y retrieval.
- `state/rag_state.py`: Estado compartido en memoria.
- `ui/rag_ui.py`: Construccion de la interfaz.

## Instalacion

1. Ollama: `irm https://ollama.com/install.ps1 | iex`.
2. LLM llama3.2:3b: `ollama pull llama3.2:3b`.
3. Embeddings QA: `ollama pull nomic-embed-text`.
4. Dependencias: `pip install -U gradio langchain langchain-community langchain-ollama chromadb pypdf`.

## Verificacion

1. Ollama: `ollama --version`.
2. Ollama Servidor: `ollama serve`.
3. Ollama Modelos: `ollama list`.
4. Gradio: `pip show gradio`.
