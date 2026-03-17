# Practica 07 Employee Similarity Search With ChromaDB

## Leyenda

1. ChromaDB: Colecciones en memoria para empleados y libros.
2. Embeddings locales reales: Vectores servidos por `Ollama` con `nomic-embed-text`.
3. Busqueda avanzada: Similitud filtros de metadatos y consultas combinadas.

## Roles de Archivos

- `main.py`: Punto de entrada de la practica.
- `config/employee_similarity_config.py`: Constantes de colecciones y busquedas.
- `data/employee_records.py`: Dataset de empleados del laboratorio.
- `data/book_records.py`: Dataset de libros del ejercicio de practica.
- `models/employee_book_embedding_gateway.py`: Embeddings reales locales para empleados y libros.
- `orchestration/employee_collection_orchestration.py`: Creacion y carga de la coleccion de empleados.
- `orchestration/employee_search_orchestration.py`: Similarity search y filtros sobre empleados.
- `orchestration/book_collection_orchestration.py`: Creacion y carga de la coleccion de libros.
- `orchestration/book_search_orchestration.py`: Similarity search y filtros sobre libros.
- `orchestration/employee_similarity_lab_runner.py`: Ejecucion guiada de toda la practica.
- `state/employee_similarity_state.py`: Estado compartido del cliente y colecciones.

## Instalacion

1. Activar entorno: `.\venv\Scripts\Activate.ps1`.
2. ChromaDB: `pip install -U chromadb`.
3. Numpy: `pip install -U numpy`.
4. LangChain Ollama: `pip install -U langchain-ollama`.
5. Arrancar `Ollama`: `ollama serve`.
6. Descargar embedding local: `ollama pull nomic-embed-text`.

## Verificacion

1. Compilacion: `python -m compileall spikes\07-employee_similarity_search_chromadb_lab`.
2. ChromaDB: `python -c "import chromadb; print(chromadb.__version__)"`.
3. Practica: `.\venv\Scripts\python.exe .\spikes\07-employee_similarity_search_chromadb_lab\main.py`.

## Nota

Esta adaptacion no descarga `SentenceTransformers`. La practica usa embeddings reales locales de `Ollama` para mantener una ejecucion gratuita y alineada con el resto del repositorio.
