# Practica 06 Vector Databases And Chroma DB Cheat Sheet

## Leyenda

1. Metricas vectoriales: Resumen de L2 producto punto y coseno para retrieval.
2. ChromaDB: Demo local con colecciones filtros y consultas por similitud.
3. Embeddings demo: Vectores deterministas para ejecutar la practica sin modelos externos.

## Roles de Archivos

- `main.py`: Punto de entrada de la practica.
- `config/chromadb_cheat_sheet_config.py`: Constantes del spike y textos del resumen.
- `data/chromadb_demo_dataset.py`: Documentos metadatos consultas y filtros de ejemplo.
- `models/chromadb_keyword_embedding_gateway.py`: Embeddings locales basados en palabras clave.
- `orchestration/chromadb_collection_orchestration.py`: Cliente creacion de coleccion y carga de datos.
- `orchestration/chromadb_query_orchestration.py`: Filtros consultas y formateo de resultados.
- `orchestration/chromadb_cheat_sheet_runner.py`: Ejecucion guiada del resumen y la demo.
- `state/chromadb_runtime_state.py`: Estado compartido del cliente y la coleccion.

## Instalacion

1. Activar entorno: `.\venv\Scripts\Activate.ps1`.
2. ChromaDB: `pip install -U chromadb`.
3. Numpy: `pip install -U numpy`.

## Verificacion

1. Compilacion: `python -m compileall spikes\06-vector_databases_chromadb_cheat_sheet_lab`.
2. ChromaDB: `python -c "import chromadb; print(chromadb.__version__)"`.
3. Practica: `python .\spikes\06-vector_databases_chromadb_cheat_sheet_lab\main.py`.
