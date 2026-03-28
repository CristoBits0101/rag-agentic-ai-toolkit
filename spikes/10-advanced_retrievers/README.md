# Practica 10 Explore Advanced Retrievers In LlamaIndex

## Leyenda

1. Vector Index Retriever: Retrieval semantico con `VectorStoreIndex`.
2. BM25 Retriever: Retrieval lexico con ranking clasico sobre nodos.
3. Document Summary Index: Seleccion previa de documentos con resumenes.
4. Auto Merging Retriever: Preservacion de contexto con nodos padre e hijo.
5. Recursive Retriever: Seguimiento de referencias entre recuperadores.
6. Query Fusion Retriever: Fusion de consultas con `reciprocal_rerank` `relative_score` y `dist_based_score`.
7. Ejercicio 1: Recuperador hibrido con vector search y `BM25`.
8. Ejercicio 2: Pipeline `RAG` simple con `RetrieverQueryEngine`.

## Adaptacion

Esta practica adapta el notebook de IBM Skills Network a una version local y reproducible del repositorio. El laboratorio original usa watsonx.ai y embeddings remotos. En esta adaptacion todo corre con `LlamaIndex` real mas un `LLM` y embeddings servidos por `Ollama`.

## Roles de Archivos

- `main.py`: Punto de entrada de la practica.
- `config/advanced_retrievers_config.py`: Consultas y parametros del laboratorio.
- `data/advanced_retrievers_documents.py`: Documentos base documentos largos y corpus recursivo.
- `models/advanced_retrievers_ollama_gateway.py`: `LLM` y embeddings reales locales compatibles con `LlamaIndex`.
- `orchestration/advanced_retrievers_index_orchestration.py`: Construccion cacheada de indices y retrievers base.
- `orchestration/advanced_retrievers_core_orchestration.py`: Vector retrieval BM25 y document summary.
- `orchestration/advanced_retrievers_context_orchestration.py`: Auto merging y recursive retrieval.
- `orchestration/advanced_retrievers_fusion_orchestration.py`: Query fusion retriever recuperador hibrido y pipeline RAG.
- `orchestration/advanced_retrievers_lab_runner.py`: Ejecucion guiada del laboratorio.

## Instalacion

1. Activar entorno: `.\venv\Scripts\Activate.ps1`.
2. LlamaIndex Core: `pip install -U llama-index-core==0.12.49`.
3. BM25 Retriever: `pip install -U llama-index-retrievers-bm25==0.5.2 rank-bm25==0.2.2 PyStemmer==2.2.0.3`.
4. LangChain Ollama: `pip install -U langchain-ollama`.
5. Arrancar `Ollama`: `ollama serve`.
6. Embedding local: `ollama pull nomic-embed-text`.
7. Modelo de texto: `ollama pull qwen2.5:7b`.

## Verificacion

1. Compilacion: `python -m compileall spikes\10-advanced_retrievers`.
2. Practica: `.\venv\Scripts\python.exe .\spikes\10-advanced_retrievers\main.py`.
3. Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_10_advanced_retrievers.py`.

## Cobertura

1. `VectorIndexRetriever`: Recuperacion por similitud semantica.
2. `BM25Retriever`: Ranking basado en terminos exactos.
3. `DocumentSummaryIndexLLMRetriever`: Seleccion de documentos mediante resumenes y `LLM`.
4. `DocumentSummaryIndexEmbeddingRetriever`: Seleccion de documentos mediante embeddings de resumen.
5. `AutoMergingRetriever`: Union automatica de chunks hijos cuando el contexto lo requiere.
6. `RecursiveRetriever`: Salto desde un nodo indice a recuperadores especializados.
7. `QueryFusionRetriever`: Comparacion de tres modos de fusion.
8. `WeightedHybridRetriever`: Ejercicio de recuperacion hibrida.
9. `RetrieverQueryEngine`: Ejercicio de pipeline `RAG`.
