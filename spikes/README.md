# README de Spikes

Este archivo resume de forma rapida de que va cada practica del directorio `spikes` y que aprendizaje principal deja cada una.

## Vista Rapida

| Practica | Tema | De que va | Que aprendes | Enlace |
| --- | --- | --- | --- | --- |
| 01 | Prompting y LCEL. | Introduce prompts basicos plantillas y composicion de flujos con `LangChain` y `LCEL`. | A estructurar prompts encadenar pasos y razonar sobre salidas de un `LLM` local. | [01-prompting_lcel_lab](./01-prompting_lcel_lab/README.md) |
| 02 | Interfaz con Gradio y Llama. | Construye una interfaz sencilla que conecta formulario estado y modelo local con `Gradio`. | A separar UI estado y acceso a modelo en una app minima de IA. | [02-gradio_llama_lab](./02-gradio_llama_lab/README.md) |
| 03 | RAG sobre PDF. | Implementa un bot de preguntas y respuestas sobre un PDF con carga division embeddings retrieval y respuesta. | A montar un flujo `RAG` clasico de extremo a extremo sobre documentos. | [03-rag_pdf_qa_bot_lab](./03-rag_pdf_qa_bot_lab/README.md) |
| 04 | LinkedIn Icebreaker Bot. | Usa perfiles mock tipo LinkedIn para generar contexto preguntas y respuestas conversacionales con `RAG`. | A convertir datos estructurados en contexto util para personalizacion y conversacion. | [04-linkedin_icebreaker_bot_lab](./04-linkedin_icebreaker_bot_lab/README.md) |
| 05 | Similarity Search by Hand. | Explica la busqueda por similitud desde cero con embeddings normalizacion y calculo manual de metricas. | A entender como funcionan coseno distancia y ranking sin depender de una vector DB. | [05-similarity_search_by_hand_lab](./05-similarity_search_by_hand_lab/README.md) |
| 06 | ChromaDB Cheat Sheet. | Resume conceptos de vector databases y demuestra operaciones CRUD consultas y filtros en `ChromaDB`. | A manejar colecciones metadatos y consultas semanticas basicas en una base vectorial. | [06-vector_databases_chromadb_cheat_sheet_lab](./06-vector_databases_chromadb_cheat_sheet_lab/README.md) |
| 07 | Similaridad en empleados y libros. | Aplica `ChromaDB` a dos dominios pequenos con embeddings deterministas y filtros de metadatos. | A modelar colecciones distintas y comparar busqueda semantica con restricciones de negocio. | [07-employee_similarity_search_chromadb_lab](./07-employee_similarity_search_chromadb_lab/README.md) |
| 08 | Recomendaciones de comida con RAG. | Combina retrieval en `ChromaDB` con generacion para recomendar platos segun consulta contexto y filtros. | A construir un sistema de recomendacion simple apoyado en retrieval y respuesta generada. | [08-food_recommendation_systems_chromadb_rag_lab](./08-food_recommendation_systems_chromadb_rag_lab/README.md) |
| 09 | Context Retrieval con LangChain. | Explora `top k` `MMR` `score threshold` `MultiQueryRetriever` `SelfQueryRetriever` y `ParentDocumentRetriever`. | A elegir tecnicas de retrieval segun consulta expansion filtros y preservacion de contexto. | [09-langchain_context_retrieval_lab](./09-langchain_context_retrieval_lab/README.md) |
| 10 | Advanced Retrievers con LlamaIndex. | Recorre `VectorIndexRetriever` `BM25` `DocumentSummaryIndex` `AutoMergingRetriever` `RecursiveRetriever` y `QueryFusionRetriever`. | A comparar retrievers avanzados y a crear estrategias hibridas y pipelines `RAG` mas robustos. | [10-advanced_retrievers_llamaindex_lab](./10-advanced_retrievers_llamaindex_lab/README.md) |
| 11 | Semantic Similarity con FAISS. | Implementa preprocesamiento vectorizacion e indexacion con `FAISS IndexFlatL2` sobre un corpus local. | A entender el flujo completo de semantic search con un indice vectorial real. | [11-semantic_similarity_faiss_lab](./11-semantic_similarity_faiss_lab/README.md) |
| 12 | YouTube Summarizer y QA con FAISS. | Procesa transcriptos chunking retrieval con `LangChain FAISS` y genera resumenes y respuestas sobre un video. | A construir una mini aplicacion `RAG` para contenido multimedia basado en transcriptos. | [12-youtube_summarizer_rag_faiss_lab](./12-youtube_summarizer_rag_faiss_lab/README.md) |
| 13 | Story Generator y Text to Speech. | Genera una historia educativa para un tema dado y la transforma en un artefacto de audio local o en variantes reales con `Ollama` `Mistral API` y `edge-tts`. | A combinar prompting generacion de texto y una salida de audio reproducible dentro del repo o con proveedores reales. | [13-story_generator_text_to_speech_lab](./13-story_generator_text_to_speech_lab/README.md) |
| 14 | Vision Multimodal Basica. | Construye mensajes con imagen y texto responde preguntas visuales y hace matching simple contra un catalogo. Tambien incluye variantes reales con `llava` `llama3.2-vision` y `qwen2.5vl` en `Ollama`. | A entender el patron basico de `vision querying` `VQA` y similitud visual ligera con demo local o modelos reales. | [14-basic_vision_multimodal_lab](./14-basic_vision_multimodal_lab/README.md) |
| 15 | AI Meeting Assistant. | Transcribe audio de reunion normaliza terminos financieros y genera acta con tareas descargables. | A encadenar `Speech to Text` limpieza de transcript y generacion estructurada en una app de reuniones. | [15-ai_meeting_assistant_lab](./15-ai_meeting_assistant_lab/README.md) |
| 16 | DALL-E Image Generation. | Genera imagenes desde prompts con `dall-e-2` y `dall-e-3` y guarda los resultados en archivos locales. | A comparar dos versiones reales de la API de imagenes de `OpenAI` y adaptar salidas de notebook a un flujo ejecutable desde terminal. | [16-dalle_image_generation_lab](./16-dalle_image_generation_lab/README.md) |

## Ruta de Aprendizaje Sugerida

1. Empieza por `01` y `02` si quieres dominar prompts `LCEL` y una interfaz minima.
2. Sigue con `03` `05` y `06` para entender `RAG` embeddings similitud y bases vectoriales.
3. Continua con `07` y `08` para ver casos de uso concretos de retrieval y recomendacion.
4. Pasa a `09` y `10` cuando quieras profundizar en retrievers avanzados.
5. Cierra con `11` `12` `13` `14` `15` y `16` para trabajar `FAISS` contenido multimedia `Text to Speech` vision multimodal asistentes de reunion y generacion de imagenes.

## Nota

La mayoria de practicas estan adaptadas para ejecutarse de forma local y reproducible. Cuando un laboratorio original dependia de servicios externos el repositorio usa datos locales embeddings deterministas o modelos de demostracion para mantener estabilidad y trazabilidad en tests.

Cuando una practica de `spikes` puede resolverse bien con `Ollama` se prioriza esa via. Si la practica es multimodal o el caso de uso no encaja con `Ollama` se debe usar el modelo recomendado en el `README` de la propia practica. Si para ese mismo caso existe una alternativa gratuita y accesible en internet se debe priorizar esa opcion gratuita.
