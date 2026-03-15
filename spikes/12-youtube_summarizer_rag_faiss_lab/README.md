# Practica 12 AI Powered YouTube Summarizer QA Tool With RAG LangChain And FAISS

## Leyenda

1. Extraccion del identificador de un video de YouTube.
2. Carga de transcriptos desde un catalogo local estable.
3. Procesamiento y chunking con `RecursiveCharacterTextSplitter`.
4. Retrieval con `LangChain FAISS` y embeddings deterministas.
5. Resumen y QA mediante prompts y un `DemoLLM` local.

## Adaptacion

Esta practica adapta el lab original sin depender de `watsonx.ai` ni de llamadas remotas a YouTube. En lugar de descargar transcriptos y usar modelos externos el repositorio trabaja con un transcript local asociado a la URL de ejemplo y un `DemoLLM` reproducible. El flujo sigue siendo el mismo: transcriptos procesados chunking retrieval con `FAISS` resumen y preguntas con `RAG`.

## Roles de Archivos

- `main.py`: Punto de entrada de la practica.
- `config/youtube_rag_config.py`: URL del video consultas y parametros de chunking.
- `data/youtube_transcript_catalog.py`: Catalogo local de transcriptos con marcas de tiempo.
- `models/youtube_rag_embedding_gateway.py`: Embeddings deterministas compatibles con `LangChain FAISS`.
- `models/youtube_rag_demo_llm.py`: LLM de demostracion para resumen y QA.
- `orchestration/youtube_transcript_orchestration.py`: Extraccion de video id carga del transcripto y chunking.
- `orchestration/youtube_rag_orchestration.py`: Indice FAISS prompts resumen retrieval y respuestas.
- `orchestration/youtube_rag_lab_runner.py`: Ejecucion guiada del laboratorio.

## Instalacion

1. Activar entorno: `.\venv\Scripts\Activate.ps1`.
2. Dependencias ya cubiertas por el repo: `langchain` `langchain-community` y `faiss-cpu`.

## Verificacion

1. Compilacion: `python -m compileall spikes\12-youtube_summarizer_rag_faiss_lab`.
2. Practica: `.\venv\Scripts\python.exe .\spikes\12-youtube_summarizer_rag_faiss_lab\main.py`.
3. Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_12_youtube_summarizer_rag_faiss.py`.

## Cobertura

1. `get_video_id`: Extraccion del identificador de un enlace de YouTube.
2. `get_transcript`: Recuperacion del transcript local del video.
3. `process_transcript`: Transformacion del transcript en texto lineal con marcas de tiempo.
4. `chunk_transcript`: Division del transcript para retrieval.
5. `create_faiss_index`: Construccion del vector store `FAISS`.
6. `summarize_video`: Resumen del video con prompt y LLM local.
7. `answer_question`: QA sobre contexto recuperado con `RAG`.
