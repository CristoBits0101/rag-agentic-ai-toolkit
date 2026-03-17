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
| 14 | Vision Multimodal Basica. | Construye mensajes con imagen y texto responde preguntas visuales hace captioning en lote matching simple contra un catalogo y se extiende con `Style Finder` en `Gradio` y `Nutrition Coach` en `Flask`. Tambien incluye variantes reales con `llava` `llama3.2-vision` y `qwen2.5vl` en `Ollama`. | A entender el patron basico de `vision querying` `VQA` `Image Captioning` y como escalarlo a apps completas de `multimodal RAG` para moda y nutricion. | [14-basic_vision_multimodal_lab](./14-basic_vision_multimodal_lab/README.md) |
| 15 | AI Meeting Assistant. | Transcribe audio de reunion normaliza terminos financieros y genera acta con tareas descargables. | A encadenar `Speech to Text` limpieza de transcript y generacion estructurada en una app de reuniones. | [15-ai_meeting_assistant_lab](./15-ai_meeting_assistant_lab/README.md) |
| 16 | DALL-E Image Generation. | Genera imagenes desde prompts con `dall-e-2` y `dall-e-3` guarda los resultados en archivos locales y define requests configurables para tamano calidad y salida multiple. | A comparar dos versiones reales de la API de imagenes de `OpenAI` y adaptar salidas de notebook a un flujo ejecutable desde terminal. | [16-dalle_image_generation_lab](./16-dalle_image_generation_lab/README.md) |
| 17 | Voice Desktop Assistant. | Escucha ordenes desde un micro con `push to talk` las transcribe en local con `Whisper` y ejecuta acciones seguras de escritorio con `Ollama` incluyendo cierre confirmado de apps envio a papelera con confirmacion fallback si `Ollama` devuelve un plan invalido verificacion del estado real del proceso al cerrar y un estado resumido en una sola linea. | A combinar audio local `Speech to Text` planificacion segura con `Ollama` y automatizacion de escritorio con una politica de permisos minima. | [17-voice_desktop_assistant_lab](./17-voice_desktop_assistant_lab/README.md) |
| 18 | LangChain Tool Calling Math Assistant. | Construye un asistente matematico con tools de `LangChain` definidas con `@tool` y `ChatOllama` como modelo principal junto con un catalogo factual local y un bucle controlado de tool calling. | A entender el contrato real de `tool calling` probar herramientas por separado y componer calculos multi paso con un modelo real compatible con el stack del repo. | [18-langchain_tool_calling_math_assistant_lab](./18-langchain_tool_calling_math_assistant_lab/README.md) |
| 19 | DataWizard AI Powered Data Analysis. | Construye un asistente de analisis de datos con `LangChain` y `ChatOllama` que descubre CSV locales mantiene una cache de `DataFrame` resume datasets ejecuta metodos seguros de `pandas` y evalua modelos de clasificacion o regresion con `scikit-learn`. | A conectar lenguaje natural con analisis tabular real y a comparar un baseline conversacional sin tools frente a un executor agent con modelo real y workflows multi paso. | [19-datawizard_ai_powered_data_analysis_lab](./19-datawizard_ai_powered_data_analysis_lab/README.md) |

## Guia de Prueba

Estas instrucciones asumen que estas en la raiz del repositorio y que ya activaste el entorno con `.\venv\Scripts\Activate.ps1`. Cuando una practica usa `Ollama` debes arrancar `ollama serve` antes de ejecutarla y descargar los modelos indicados en el `README` propio del spike.

### Practica 01

Compilacion: `python -m compileall spikes\01-prompting_lcel_lab`.
Ejecucion: `python .\spikes\01-prompting_lcel_lab\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_01_prompting.py`.

### Practica 02

Compilacion: `python -m compileall spikes\02-gradio_llama_lab`.
Ejecucion: `python .\spikes\02-gradio_llama_lab\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_02_gradio_llama.py`.

### Practica 03

Compilacion: `python -m compileall spikes\03-rag_pdf_qa_bot_lab`.
Ejecucion: `python .\spikes\03-rag_pdf_qa_bot_lab\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_03_rag_pdf_qa_bot.py`.

### Practica 04

Compilacion: `python -m compileall spikes\04-linkedin_icebreaker_bot_lab`.
Ejecucion: `python .\spikes\04-linkedin_icebreaker_bot_lab\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_04_profile_pipeline.py`.

### Practica 05

Dependencias extra: `pip install -U sentence-transformers==4.1.0 scipy torch`.
Compilacion: `python -m compileall spikes\05-similarity_search_by_hand_lab`.
Ejecucion: `python .\spikes\05-similarity_search_by_hand_lab\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_05_similarity_metrics.py`.

### Practica 06

Compilacion: `python -m compileall spikes\06-vector_databases_chromadb_cheat_sheet_lab`.
Ejecucion: `python .\spikes\06-vector_databases_chromadb_cheat_sheet_lab\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_06_chromadb_cheat_sheet.py`.

### Practica 07

Compilacion: `python -m compileall spikes\07-employee_similarity_search_chromadb_lab`.
Ejecucion: `python .\spikes\07-employee_similarity_search_chromadb_lab\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_07_employee_similarity.py`.

### Practica 08

Compilacion: `python -m compileall spikes\08-food_recommendation_systems_chromadb_rag_lab`.
Ejecucion: `python .\spikes\08-food_recommendation_systems_chromadb_rag_lab\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_08_food_recommendation.py`.

### Practica 09

Compilacion: `python -m compileall spikes\09-langchain_context_retrieval_lab`.
Ejecucion: `python .\spikes\09-langchain_context_retrieval_lab\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_09_context_retrieval.py`.

### Practica 10

Compilacion: `python -m compileall spikes\10-advanced_retrievers_llamaindex_lab`.
Ejecucion: `python .\spikes\10-advanced_retrievers_llamaindex_lab\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_10_advanced_retrievers_llamaindex.py`.

### Practica 11

Compilacion: `python -m compileall spikes\11-semantic_similarity_faiss_lab`.
Ejecucion: `python .\spikes\11-semantic_similarity_faiss_lab\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_11_semantic_similarity_faiss.py`.

### Practica 12

Compilacion: `python -m compileall spikes\12-youtube_summarizer_rag_faiss_lab`.
Ejecucion: `python .\spikes\12-youtube_summarizer_rag_faiss_lab\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_12_youtube_summarizer_rag_faiss.py`.

### Practica 13

Compilacion: `python -m compileall spikes\13-story_generator_text_to_speech_lab`.
Ejecucion base: `python .\spikes\13-story_generator_text_to_speech_lab\main.py`.
Variantes: `python .\spikes\13-story_generator_text_to_speech_lab\ollama_mistral_story_tts\main.py` `python .\spikes\13-story_generator_text_to_speech_lab\mistral_api_story_tts\main.py` `python .\spikes\13-story_generator_text_to_speech_lab\ollama_mistral_edge_tts_story_tts\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_13_story_generator_text_to_speech.py tests\unit\test_spike_13_story_generator_real_variants.py`.

### Practica 14

Compilacion: `python -m compileall spikes\14-basic_vision_multimodal_lab`.
Ejecucion base: `python .\spikes\14-basic_vision_multimodal_lab\main.py`.
Variantes principales: `python .\spikes\14-basic_vision_multimodal_lab\llava_vision_querying\main.py` `python .\spikes\14-basic_vision_multimodal_lab\llama3_2_vision_querying\main.py` `python .\spikes\14-basic_vision_multimodal_lab\qwen2_5vl_vision_querying\main.py`.
Apps extendidas: `python .\spikes\14-basic_vision_multimodal_lab\style_finder_fashion_rag_app\main.py` `python .\spikes\14-basic_vision_multimodal_lab\nutrition_coach_flask_app\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_14_basic_vision_multimodal.py tests\unit\test_spike_14_real_vision_variants.py tests\unit\test_spike_14_style_finder_fashion_rag_app.py tests\unit\test_spike_14_nutrition_coach_flask_app.py`.

### Practica 15

Compilacion: `python -m compileall spikes\15-ai_meeting_assistant_lab`.
Ejecucion: `python .\spikes\15-ai_meeting_assistant_lab\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_15_ai_meeting_assistant.py`.

### Practica 16

Prerequisito: exportar `OPENAI_API_KEY` si quieres probar las variantes reales.
Compilacion: `python -m compileall spikes\16-dalle_image_generation_lab`.
Ejecucion base: `python .\spikes\16-dalle_image_generation_lab\main.py`.
Variantes: `python .\spikes\16-dalle_image_generation_lab\dall_e_2_generation\main.py` `python .\spikes\16-dalle_image_generation_lab\dall_e_3_generation\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_16_dalle_image_generation.py`.

### Practica 17

Dependencias extra: `pip install -U transformers torch sounddevice pyautogui Send2Trash`.
Dependencia opcional del runner de consola: `pip install -U keyboard`.
Compilacion: `python -m compileall src spikes\17-voice_desktop_assistant_lab`.
Ejecucion: `python .\spikes\17-voice_desktop_assistant_lab\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_17_voice_desktop_assistant.py`.

### Practica 18

Prerequisito: arrancar `ollama serve` y descargar `qwen2.5:7b` o `llama3.2:3b`.
Compilacion: `python -m compileall spikes\18-langchain_tool_calling_math_assistant_lab`.
Ejecucion: `python .\spikes\18-langchain_tool_calling_math_assistant_lab\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_18_langchain_tool_calling_math_assistant.py`.

### Practica 19

Dependencias extra: `pip install -U pandas numpy scikit-learn`.
Prerequisito: arrancar `ollama serve` y descargar `qwen2.5:7b` o `llama3.2:3b`.
Compilacion: `python -m compileall spikes\19-datawizard_ai_powered_data_analysis_lab`.
Ejecucion: `python .\spikes\19-datawizard_ai_powered_data_analysis_lab\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_19_datawizard_ai_powered_data_analysis.py`.

## Ruta de Aprendizaje Sugerida

1. Empieza por `01` y `02` si quieres dominar prompts `LCEL` y una interfaz minima.
2. Sigue con `03` `05` y `06` para entender `RAG` embeddings similitud y bases vectoriales.
3. Continua con `07` y `08` para ver casos de uso concretos de retrieval y recomendacion.
4. Pasa a `09` y `10` cuando quieras profundizar en retrievers avanzados.
5. Cierra con `11` `12` `13` `14` `15` `16` `17` `18` y `19` para trabajar `FAISS` contenido multimedia `Text to Speech` vision multimodal captioning visual apps `Gradio` y `Flask` asistentes de reunion generacion de imagenes control local por voz con permisos `tool calling` moderno en `LangChain` y analisis tabular con `pandas` y `scikit-learn`.

## Nota

La mayoria de practicas estan adaptadas para ejecutarse de forma local y reproducible. Cuando un laboratorio original dependia de servicios externos el repositorio prioriza modelos reales locales como `Ollama` si encajan tecnicamente con el caso de uso. Los datos locales los embeddings deterministas y los modelos de demostracion se reservan sobre todo para tests o para respaldos justificados cuando la practica no puede depender de red o credenciales.

Cuando una practica de `spikes` puede resolverse bien con `Ollama` se prioriza esa via. Si la practica es multimodal o el caso de uso no encaja con `Ollama` se debe usar el modelo recomendado en el `README` de la propia practica. Si para ese mismo caso existe una alternativa gratuita y accesible en internet se debe priorizar esa opcion gratuita.
