# Practica 05 Similarity Search By Hand

## Leyenda

1. Sentence Transformers: Modelo para convertir texto en embeddings vectoriales.
2. Numpy: Base numerica para calcular distancias similitudes y normalizaciones.
3. Scipy y Torch: Soporte opcional para comparar calculos manuales con librerias.

## Roles de Archivos

- `main.py`: Punto de entrada de la practica.
- `config/similarity_runtime_config.py`: Constantes del modelo y textos del laboratorio.
- `data/similarity_documents.py`: Documentos y consulta de ejemplo.
- `models/similarity_embedding_gateway.py`: Carga perezosa del modelo de embeddings.
- `orchestration/similarity_lab_runner.py`: Ejecucion guiada de toda la practica.
- `orchestration/similarity_metrics_orchestration.py`: Distancias similitudes y normalizacion manual.
- `orchestration/similarity_search_orchestration.py`: Embedding de consulta y busqueda por coseno.
- `state/similarity_runtime_state.py`: Cache en memoria del modelo de embeddings.

## Instalacion

1. Activar entorno: `.\venv\Scripts\Activate.ps1`.
2. Numpy: `pip install -U numpy`.
3. Sentence Transformers: `pip install -U sentence-transformers==4.1.0`.
4. Scipy y Torch: `pip install -U scipy torch`.

## Verificacion

1. Compilacion: `python -m compileall spikes\05-similarity_search_by_hand_lab`.
2. Numpy: `python -c "import numpy; print(numpy.__version__)"`.
3. Sentence Transformers: `python -c "from sentence_transformers import SentenceTransformer; print('ok')"`.
4. Practica: `python .\spikes\05-similarity_search_by_hand_lab\main.py`.
