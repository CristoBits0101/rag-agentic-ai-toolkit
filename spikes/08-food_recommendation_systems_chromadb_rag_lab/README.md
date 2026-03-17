# Practica 08 Food Recommendation Systems With ChromaDB And RAG

## Leyenda

1. Dataset local: Coleccion de platos con descripcion ingredientes calorias y beneficios.
2. ChromaDB: Busqueda semantica y filtros por cocina y calorias con una coleccion en memoria.
3. RAG con Ollama: Recomendaciones conversacionales usando contexto recuperado y un modelo local real.

## Roles de Archivos

- `main.py`: Punto de entrada de la practica.
- `config/food_recommendation_config.py`: Constantes del spike y consultas de demostracion.
- `data/food_dataset.json`: Dataset local de alimentos para el laboratorio.
- `pipeline/food_data_pipeline.py`: Carga normalizacion y construccion de documentos y metadatos.
- `models/food_embedding_gateway.py`: Embeddings reales locales con `nomic-embed-text`.
- `models/food_ollama_gateway.py`: Acceso perezoso al modelo local de Ollama.
- `orchestration/food_collection_orchestration.py`: Creacion y carga de la coleccion de recomendaciones.
- `orchestration/food_search_orchestration.py`: Similarity search y filtered search.
- `orchestration/food_rag_orchestration.py`: Contexto prompt respuesta RAG y comparacion.
- `orchestration/food_recommendation_lab_runner.py`: Ejecucion guiada de los tres modos del sistema.
- `state/food_recommendation_state.py`: Estado compartido del cliente y el LLM.

## Instalacion

1. Activar entorno: `.\venv\Scripts\Activate.ps1`.
2. ChromaDB: `pip install -U chromadb`.
3. Numpy: `pip install -U numpy`.
4. LangChain Ollama: `pip install -U langchain-ollama`.
5. Arrancar `Ollama`: `ollama serve`.
6. Embedding local: `ollama pull nomic-embed-text`.
7. Modelo de texto: `ollama pull llama3.2:3b`.

## Verificacion

1. Compilacion: `python -m compileall spikes\08-food_recommendation_systems_chromadb_rag_lab`.
2. Practica: `.\venv\Scripts\python.exe .\spikes\08-food_recommendation_systems_chromadb_rag_lab\main.py`.
3. Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_08_food_recommendation.py`.

## Nota

La practica no depende de embeddings remotos ni de `SentenceTransformers`. La busqueda usa embeddings reales locales de `Ollama` y la generacion `RAG` exige un modelo local real para mantener el objetivo del laboratorio sin demos falsas.
