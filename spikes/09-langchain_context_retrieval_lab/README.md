# Practica 09 Build A Smarter Search With LangChain Context Retrieval

## Leyenda

1. Retriever clasico: Similaridad top k MMR y score threshold sobre politicas de empresa.
2. Multi Query Retrieval: Expansion de consultas con un `LLM` real local en `Ollama`.
3. Self Query Retrieval: Traduccion de lenguaje natural a filtros de metadatos sobre peliculas.
4. Parent Document Retrieval: Recuperacion por child chunks con devolucion de contexto padre.

## Adaptacion

Esta practica toma el notebook de IBM Skills Network y lo adapta al repositorio sin depender de watsonx ni de descargas remotas. Los documentos son locales. Los embeddings y el `LLM` de apoyo se sirven desde `Ollama` para mantener una ejecucion local real y gratuita.

## Roles de Archivos

- `main.py`: Punto de entrada de la practica.
- `config/context_retrieval_config.py`: Rutas chunk sizes y consultas del laboratorio.
- `data/company_policies.txt`: Politicas de empresa para retrieval clasico y parent retrieval.
- `data/langchain_retrieval_notes.txt`: Notas locales para MultiQueryRetriever.
- `data/context_retrieval_movie_dataset.py`: Dataset local de peliculas para SelfQueryRetriever.
- `models/context_retrieval_embedding_gateway.py`: Embeddings reales locales compatibles con LangChain.
- `models/context_retrieval_ollama_gateway.py`: `LLM` real local para `MultiQueryRetriever` y `SelfQueryRetriever`.
- `orchestration/context_retrieval_collection_orchestration.py`: Carga de documentos splitters y vector stores.
- `orchestration/context_retrieval_search_orchestration.py`: Retrieval clasico y MultiQueryRetriever.
- `orchestration/context_retrieval_self_query_orchestration.py`: SelfQueryRetriever y filtros por metadatos.
- `orchestration/context_retrieval_parent_orchestration.py`: ParentDocumentRetriever y comparacion child parent.
- `orchestration/context_retrieval_lab_runner.py`: Ejecucion guiada del laboratorio.

## Instalacion

1. Activar entorno: `.\venv\Scripts\Activate.ps1`.
2. ChromaDB: `pip install -U chromadb`.
3. Lark: `pip install -U lark==1.1.9`.
4. LangChain Ollama: `pip install -U langchain-ollama`.
5. Arrancar `Ollama`: `ollama serve`.
6. Embedding local: `ollama pull nomic-embed-text`.
7. Modelo de texto: `ollama pull qwen2.5:7b`.

## Verificacion

1. Compilacion: `python -m compileall spikes\09-langchain_context_retrieval_lab`.
2. Practica: `.\venv\Scripts\python.exe .\spikes\09-langchain_context_retrieval_lab\main.py`.
3. Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_09_context_retrieval.py`.

## Cobertura

1. `as_retriever`: Similarity top k MMR y similarity score threshold.
2. `MultiQueryRetriever`: Expansion de consultas desde una sola pregunta.
3. `SelfQueryRetriever`: Separacion entre consulta semantica y filtros por metadatos.
4. `ParentDocumentRetriever`: Diferencia entre child chunks indexados y parent docs devueltos.
