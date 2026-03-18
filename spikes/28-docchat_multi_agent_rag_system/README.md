# Practica 28 DocChat Multi Agent RAG System

## Leyenda

1. Multi-agent RAG: La practica usa agentes separados para relevancia investigacion y verificacion.
2. Hybrid retrieval: Combina BM25 y busqueda vectorial con `Chroma`.
3. Parser con cache: Procesa documentos y evita trabajo repetido con hashes y cache local.
4. Verificacion anti alucinacion: La respuesta inicial se revisa antes de presentarse.
5. UI opcional: Incluye una interfaz `Gradio` para cargar documentos y consultar el sistema.

## Adaptacion

Esta practica adapta DocChat al stack local del repositorio. En lugar de `watsonx.ai` usa `ChatOllama` como modelo principal. En lugar de depender exclusivamente de `docling`, el parser usa `docling` si esta disponible y hace fallback a `pypdf`, texto plano y `python-docx` cuando corresponde. Para evitar una dependencia obligatoria de embeddings remotos, el spike implementa embeddings locales deterministas mediante hashing, suficientes para ejecutar un retriever hibrido real sobre documentos largos sin bloquear el laboratorio por credenciales o descargas de modelos adicionales.

## Roles de Archivos

- `main.py`: Punto de entrada CLI de la practica.
- `app.py`: Punto de entrada de la app `Gradio` en el puerto 5000.
- `config/docchat_config.py`: Rutas constantes y ejemplos.
- `models/docchat_state.py`: Estado tipado del workflow multiagente.
- `models/docchat_entities.py`: Resultado tipado del pipeline.
- `models/docchat_ollama_gateway.py`: Seleccion de modelo y construccion de `ChatOllama`.
- `models/docchat_embedding_gateway.py`: Embeddings locales deterministas para `Chroma`.
- `pipeline/file_handler.py`: Parser chunking cache y deduplicacion de documentos.
- `orchestration/retriever_builder.py`: Construccion del retriever hibrido BM25 + vector search.
- `agents/relevance_checker.py`: Clasifica la relevancia de la pregunta respecto al documento.
- `agents/research_agent.py`: Genera el primer borrador usando el contexto recuperado.
- `agents/verification_agent.py`: Revisa soporte factual y relevancia del borrador.
- `orchestration/workflow.py`: Grafo LangGraph con pasos de relevancia investigacion y verificacion.
- `orchestration/docchat_lab_runner.py`: Runner CLI con los ejemplos incluidos.
- `ui/docchat_ui.py`: Interfaz `Gradio` con carga de archivos y ejemplos.

## Instalacion

1. Activar entorno: `\.venv\Scripts\Activate.ps1`.
2. Instalar dependencias base del repo: `pip install -r requirements.txt`.
3. Arrancar `Ollama`: `ollama serve`.
4. Descargar un modelo recomendado: `ollama pull qwen2.5:7b`.
5. Modelo compatible de menor consumo: `ollama pull llama3.2:3b`.
6. Opcional para parser avanzado: `pip install -U docling`.
7. Opcional para `.docx`: `pip install -U python-docx`.

## Verificacion

1. Compilacion: `python -m compileall spikes\28-docchat_multi_agent_rag_system`.
2. Practica CLI: `.\venv\Scripts\python.exe .\spikes\28-docchat_multi_agent_rag_system\main.py`.
3. App UI: `.\venv\Scripts\python.exe .\spikes\28-docchat_multi_agent_rag_system\app.py`.
4. Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_28_docchat_multi_agent_rag_system.py`.

## Cobertura

1. `DocumentProcessor`: Parsea chunkifica cachea y deduplica documentos.
2. `RetrieverBuilder`: Construye un `EnsembleRetriever` con BM25 y Chroma.
3. `RelevanceChecker`: Decide entre `CAN_ANSWER`, `PARTIAL` y `NO_MATCH`.
4. `ResearchAgent`: Redacta un borrador grounded en el contexto.
5. `VerificationAgent`: Detecta afirmaciones no soportadas y relevancia.
6. `AgentWorkflow`: Orquesta el bucle con re investigacion si falla la verificacion.
7. `build_demo`: Expone una UI Gradio para subir documentos y preguntar.