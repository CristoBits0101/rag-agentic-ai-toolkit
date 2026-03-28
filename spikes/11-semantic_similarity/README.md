# Practica 11 Semantic Similarity With FAISS

## Leyenda

1. Dataset local tipo foro para emular un corpus multi tema.
2. Preprocesamiento de texto con limpieza de encabezados correos y ruido.
3. Vectorizacion semantica local con embeddings reales de `Ollama`.
4. Indexacion real con `FAISS IndexFlatL2`.
5. Busqueda semantica con consultas exactas y consultas por sinonimia cercana.

## Adaptacion

Esta practica adapta el lab de Skills Network sin depender de `tensorflow` ni del `Universal Sentence Encoder` remoto. En lugar del dataset `20 Newsgroups` y de descargas pesadas el repositorio usa un corpus local tipo foro y embeddings reales de `Ollama` para demostrar el flujo completo de semantic similarity con `FAISS`.

## Roles de Archivos

- `main.py`: Punto de entrada de la practica.
- `config/faiss_similarity_config.py`: Consultas y parametros del laboratorio.
- `data/faiss_forum_posts.py`: Corpus local con posts de motorcycles space graphics y medicine.
- `models/faiss_semantic_embedding_gateway.py`: Embeddings reales locales compatibles con `FAISS`.
- `orchestration/faiss_preprocessing_orchestration.py`: Limpieza y normalizacion de texto.
- `orchestration/faiss_index_orchestration.py`: Construccion cacheada del indice y la matriz de embeddings.
- `orchestration/faiss_search_orchestration.py`: Consultas por similitud y empaquetado de resultados.
- `orchestration/faiss_similarity_lab_runner.py`: Ejecucion guiada del laboratorio.

## Instalacion

1. Activar entorno: `.\venv\Scripts\Activate.ps1`.
2. FAISS: `pip install -U faiss-cpu==1.13.2`.
3. LangChain Ollama: `pip install -U langchain-ollama`.
4. Arrancar `Ollama`: `ollama serve`.
5. Descargar embedding local: `ollama pull nomic-embed-text`.

## Verificacion

1. Compilacion: `python -m compileall spikes\11-semantic_similarity`.
2. Practica: `.\venv\Scripts\python.exe .\spikes\11-semantic_similarity\main.py`.
3. Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_11_semantic_similarity.py`.

## Cobertura

1. `preprocess_text`: Limpieza base para estandarizar documentos y consultas.
2. `build_semantic_vector`: Vectorizacion local de texto mediante `Ollama`.
3. `IndexFlatL2`: Indexado y busqueda por distancia euclidiana.
4. `search_semantic_posts`: Recuperacion de resultados con distancias titulos y categorias.
