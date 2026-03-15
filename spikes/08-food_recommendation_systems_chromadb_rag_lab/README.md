# Practica 08 Food Recommendation Systems With ChromaDB And RAG

## Leyenda

1. Dataset local: Coleccion de platos con descripcion ingredientes calorias y beneficios.
2. ChromaDB: Busqueda semantica y filtros por cocina y calorias con una coleccion en memoria.
3. RAG con Ollama: Recomendaciones conversacionales usando contexto recuperado y fallback seguro.

## Roles de Archivos

- `main.py`: Punto de entrada de la practica.
- `config/food_recommendation_config.py`: Constantes del spike y consultas de demostracion.
- `data/food_dataset.json`: Dataset local de alimentos para el laboratorio.
- `pipeline/food_data_pipeline.py`: Carga normalizacion y construccion de documentos y metadatos.
- `models/food_embedding_gateway.py`: Embeddings deterministas para mantener la practica estable.
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
4. Ollama opcional: `pip install -U langchain-ollama`.
5. Modelo opcional: `ollama pull llama3.2:3b`.

## Verificacion

1. Compilacion: `python -m compileall spikes\08-food_recommendation_systems_chromadb_rag_lab`.
2. Practica: `.\venv\Scripts\python.exe .\spikes\08-food_recommendation_systems_chromadb_rag_lab\main.py`.
3. Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_08_food_recommendation.py`.

## Nota

La practica no depende de embeddings remotos ni de `SentenceTransformers`. La parte de busqueda usa embeddings deterministas para que los tests sean reproducibles. La parte RAG intenta usar `Ollama` si esta disponible y si no genera una respuesta de respaldo basada en el contexto recuperado.
