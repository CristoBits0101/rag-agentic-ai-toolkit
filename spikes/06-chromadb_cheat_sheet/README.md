# Practica 06 Vector Databases And Chroma DB Cheat Sheet

## Leyenda

1. Metricas vectoriales: Resumen de L2 producto punto y coseno para retrieval.
2. RAG y recommendation systems: Resumen operativo de responsabilidades riesgos y casos de uso.
3. ChromaDB: Flujo local con colecciones filtros consultas por similitud y operaciones CRUD.
4. Embeddings reales locales: Vectores servidos por `Ollama` con `nomic-embed-text`.

## Roles de Archivos

- `main.py`: Punto de entrada de la practica.
- `config/chromadb_cheat_sheet_config.py`: Constantes del spike y textos del resumen.
- `data/chromadb_demo_dataset.py`: Documentos metadatos consultas y filtros de ejemplo.
- `models/chromadb_keyword_embedding_gateway.py`: Embeddings reales locales servidos por `Ollama`.
- `orchestration/chromadb_collection_orchestration.py`: Cliente coleccion y operaciones CRUD de la demo.
- `orchestration/chromadb_query_orchestration.py`: Filtros consultas lecturas por id y formateo de resultados.
- `orchestration/chromadb_cheat_sheet_runner.py`: Ejecucion guiada del resumen y la demo.
- `state/chromadb_runtime_state.py`: Estado compartido del cliente y la coleccion.

## Cobertura

1. Metricas de similitud: L2 producto punto y coseno con enfoque de uso.
2. Fundamentos de RAG: Pipeline responsabilidades de la base vectorial y errores frecuentes.
3. Recommendation systems: Retrieval semantico combinado con filtros de negocio.
4. Operaciones de ChromaDB: `create_collection` `get_collection` `modify` `add` `get` `query` `update` y `delete`.
5. Filtros: `where` `where_document` busqueda sensible a mayusculas y filtros compuestos.

## Instalacion

1. Activar entorno: `.\venv\Scripts\Activate.ps1`.
2. ChromaDB: `pip install -U chromadb`.
3. Numpy: `pip install -U numpy`.
4. LangChain Ollama: `pip install -U langchain-ollama`.
5. Arrancar `Ollama`: `ollama serve`.
6. Descargar embedding local: `ollama pull nomic-embed-text`.

## Verificacion

1. Compilacion: `python -m compileall spikes\06-chromadb_cheat_sheet`.
2. ChromaDB: `python -c "import chromadb; print(chromadb.__version__)"`.
3. Practica: `python .\spikes\06-chromadb_cheat_sheet\main.py`.
4. Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_06_chromadb_cheat_sheet.py`.
