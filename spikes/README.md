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
| 07 | Similaridad en empleados y libros. | Aplica `ChromaDB` a dos dominios pequenos con embeddings reales locales y filtros de metadatos. | A modelar colecciones distintas y comparar busqueda semantica con restricciones de negocio. | [07-employee_similarity_search_chromadb_lab](./07-employee_similarity_search_chromadb_lab/README.md) |
| 08 | Recomendaciones de comida con RAG. | Combina retrieval en `ChromaDB` con generacion para recomendar platos segun consulta contexto y filtros. | A construir un sistema de recomendacion simple apoyado en retrieval y respuesta generada. | [08-food_recommendation_systems_chromadb_rag_lab](./08-food_recommendation_systems_chromadb_rag_lab/README.md) |
| 09 | Context Retrieval con LangChain. | Explora `top k` `MMR` `score threshold` `MultiQueryRetriever` `SelfQueryRetriever` y `ParentDocumentRetriever`. | A elegir tecnicas de retrieval segun consulta expansion filtros y preservacion de contexto. | [09-langchain_context_retrieval_lab](./09-langchain_context_retrieval_lab/README.md) |
| 10 | Advanced Retrievers con LlamaIndex. | Recorre `VectorIndexRetriever` `BM25` `DocumentSummaryIndex` `AutoMergingRetriever` `RecursiveRetriever` y `QueryFusionRetriever`. | A comparar retrievers avanzados y a crear estrategias hibridas y pipelines `RAG` mas robustos. | [10-advanced_retrievers_llamaindex_lab](./10-advanced_retrievers_llamaindex_lab/README.md) |
| 11 | Semantic Similarity con FAISS. | Implementa preprocesamiento vectorizacion e indexacion con `FAISS IndexFlatL2` sobre un corpus local. | A entender el flujo completo de semantic search con un indice vectorial real. | [11-semantic_similarity_faiss_lab](./11-semantic_similarity_faiss_lab/README.md) |
| 12 | YouTube Summarizer y QA con FAISS. | Procesa transcriptos chunking retrieval con `LangChain FAISS` y genera resumenes y respuestas sobre un video. | A construir una mini aplicacion `RAG` para contenido multimedia basado en transcriptos. | [12-youtube_summarizer_rag_faiss_lab](./12-youtube_summarizer_rag_faiss_lab/README.md) |
| 13 | Story Generator y Text to Speech. | Genera una historia educativa con un `LLM` real en `Ollama` y la transforma en audio con `edge-tts` o variantes adicionales. | A combinar prompting generacion de texto y una salida de audio gratuita o local sin perder el objetivo del laboratorio. | [13-story_generator_text_to_speech_lab](./13-story_generator_text_to_speech_lab/README.md) |
| 14 | Vision Multimodal Basica. | Construye mensajes con imagen y texto responde preguntas visuales con un modelo real de vision en `Ollama` hace captioning en lote matching local contra un catalogo y se extiende con `Style Finder` en `Gradio` y `Nutrition Coach` en `Flask`. | A entender el patron basico de `vision querying` `VQA` `Image Captioning` y como escalarlo a apps completas de `multimodal RAG` para moda y nutricion. | [14-basic_vision_multimodal_lab](./14-basic_vision_multimodal_lab/README.md) |
| 15 | AI Meeting Assistant. | Transcribe audio de reunion normaliza terminos financieros y genera acta con tareas descargables con un modelo real de `Ollama` para la parte textual. | A encadenar `Speech to Text` limpieza de transcript y generacion estructurada en una app de reuniones. | [15-ai_meeting_assistant_lab](./15-ai_meeting_assistant_lab/README.md) |
| 16 | DALL-E Image Generation. | Genera imagenes desde prompts con `dall-e-2` y `dall-e-3` guarda los resultados en archivos locales y define requests configurables para tamano calidad y salida multiple. | A comparar dos versiones reales de la API de imagenes de `OpenAI` y adaptar salidas de notebook a un flujo ejecutable desde terminal. | [16-dalle_image_generation_lab](./16-dalle_image_generation_lab/README.md) |
| 17 | Voice Desktop Assistant. | Escucha ordenes desde un micro con `push to talk` las transcribe en local con `Whisper` y ejecuta acciones seguras de escritorio con `Ollama` incluyendo cierre confirmado de apps envio a papelera con confirmacion verificacion del estado real del proceso al cerrar y un estado resumido en una sola linea. | A combinar audio local `Speech to Text` planificacion segura con `Ollama` y automatizacion de escritorio con una politica de permisos minima. | [17-voice_desktop_assistant_lab](./17-voice_desktop_assistant_lab/README.md) |
| 18 | LangChain Tool Calling Math Assistant. | Construye un asistente matematico con tools de `LangChain` definidas con `@tool` y `ChatOllama` como modelo principal junto con un catalogo factual local y un bucle controlado de tool calling. | A entender el contrato real de `tool calling` probar herramientas por separado y componer calculos multi paso con un modelo real compatible con el stack del repo. | [18-langchain_tool_calling_math_assistant_lab](./18-langchain_tool_calling_math_assistant_lab/README.md) |
| 19 | DataWizard AI Powered Data Analysis. | Construye un asistente de analisis de datos con `LangChain` y `ChatOllama` que descubre CSV locales mantiene una cache de `DataFrame` resume datasets ejecuta metodos seguros de `pandas` y evalua modelos de clasificacion o regresion con `scikit-learn`. | A conectar lenguaje natural con analisis tabular real y a comparar un baseline conversacional sin tools frente a un executor agent con modelo real y workflows multi paso. | [19-datawizard_ai_powered_data_analysis_lab](./19-datawizard_ai_powered_data_analysis_lab/README.md) |
| 20 | Interactive LLM Agents with Tools. | Construye un laboratorio de `manual tool calling` con `LangChain` y `ChatOllama` que define tools aritmeticas y de propina parsea `tool_calls` ejecuta `ToolMessage` y encapsula el flujo en agentes interactivos. | A entender paso a paso como se enlaza un modelo con herramientas reales y como convertir ese ciclo en clases de agente reutilizables. | [20-interactive_llm_agents_with_tools_lab](./20-interactive_llm_agents_with_tools_lab/README.md) |
| 21 | YouTube Tool Calling Agent. | Construye un agente con `LangChain` y `ChatOllama` que usa tools reales de YouTube para extraer `video_id` buscar videos recuperar transcriptos leer metadatos y thumbnails y automatizar tanto un flujo fijo como una cadena recursiva. | A llevar el `tool calling` a un caso multi paso contra servicios externos reales y a comparar orquestacion manual automatizada y recursiva. | [21-youtube_tool_calling_agent_lab](./21-youtube_tool_calling_agent_lab/README.md) |
| 22 | Natural Language Data Visualization Agent. | Construye un agente de `LangChain` con `create_pandas_dataframe_agent` y `ChatOllama` para consultar un CSV en lenguaje natural generar charts y extraer el Python usado para cada respuesta o visualizacion. | A unir analisis tabular conversacional con graficos reproducibles en disco y a inspeccionar el codigo que el agente ejecuta sobre `pandas` y `matplotlib`. | [22-natural_language_data_visualization_agent_lab](./22-natural_language_data_visualization_agent_lab/README.md) |
| 23 | Natural Language SQL Agent. | Construye un agente SQL de `LangChain` con `ChatOllama` y una base Chinook local en `SQLite` para traducir preguntas en lenguaje natural a consultas SQL inspeccionables. | A levantar una base relacional reproducible conectar `SQLDatabase Toolkit` y revisar las sentencias SQL que el agente ejecuta sobre un esquema real. | [23-natural_language_sql_agent_lab](./23-natural_language_sql_agent_lab/README.md) |
| 24 | LangGraph 101 Stateful AI Workflows. | Construye tres workflows con `LangGraph`: autenticacion con reintentos QA contextual sobre el propio lab y un contador ciclico basado en nodos y aristas condicionales. | A modelar estado compartido nodos aristas condicionales y ciclos reproducibles con `StateGraph` y `ChatOllama`. | [24-langgraph_101_building_stateful_ai_workflows_lab](./24-langgraph_101_building_stateful_ai_workflows_lab/README.md) |
| 25 | Reflection Agent with LangGraph. | Construye un agente reflexivo con `MessageGraph` que genera un post de LinkedIn critica su propio borrador y lo refina en varias iteraciones. | A modelar historiales de mensajes routers condicionales y bucles de auto mejora con `LangGraph` y `ChatOllama`. | [25-building_reflection_agent_with_langgraph_lab](./25-building_reflection_agent_with_langgraph_lab/README.md) |
| 26 | Reflection Agent with External Knowledge. | Construye un agente reflexivo que responde se critica usa conocimiento externo y revisa su respuesta con evidencia adicional. | A combinar `MessageGraph` `ToolMessage` salida estructurada y busqueda externa real dentro de un bucle reflexivo. | [26-building_reflection_agent_with_external_knowledge_integration](./26-building_reflection_agent_with_external_knowledge_integration/README.md) |
| 27 | ReAct Agents with LangGraph. | Construye un agente ReAct con `StateGraph` que razona usa herramientas de busqueda clima calculo y resumen de noticias y decide cuando detenerse. | A implementar el ciclo razonar actuar observar con `add_messages` `ToolMessage` y tool calling moderno sobre `ChatOllama`. | [27-react_build_reasoning_and_acting_ai_agents_with_langgraph](./27-react_build_reasoning_and_acting_ai_agents_with_langgraph/README.md) |
| 28 | DocChat Multi Agent RAG. | Construye un sistema DocChat con parser cacheado retrieval hibrido y tres agentes para relevancia investigacion y verificacion sobre documentos largos. | A combinar procesamiento documental `Chroma` BM25 `LangGraph` y una UI `Gradio` en un flujo multiagente grounded. | [28-docchat_multi_agent_rag_system](./28-docchat_multi_agent_rag_system/README.md) |
| 29 | Workflow Patterns with LangGraph. | Construye ejemplos ejecutables de prompt chaining routing parallelization y un router multiagente de servicios. | A reconocer los tres patrones base de workflows con `LangGraph` y a implementarlos sobre `ChatOllama`. | [29-implement_workflow_patterns_with_langgraph](./29-implement_workflow_patterns_with_langgraph/README.md) |
| 30 | LangGraph Orchestration and Evaluation. | Construye un patron orchestrator worker para planificacion de comidas y un patron de reflection para planes de inversion. | A coordinar workers en paralelo con `Send` y a cerrar bucles de generacion evaluacion y refinamiento. | [30-build_langgraph_design_patterns_orchestration_evaluation](./30-build_langgraph_design_patterns_orchestration_evaluation/README.md) |
| 31 | CrewAI 101 Multi Agent Systems. | Construye un pipeline de investigacion redaccion y social media siguiendo el modelo conceptual de `CrewAI`. | A separar agentes tareas y crews secuenciales para transformar research en contenido publicable. | [31-crewai_101_building_multi_agent_ai_systems](./31-crewai_101_building_multi_agent_ai_systems/README.md) |
| 32 | Structured Meal Grocery Planner with CrewAI. | Construye un sistema de meal planning y grocery planning con modelos `Pydantic` YAML y un flujo multiagente estilo `CrewAI`. | A combinar agentes especializados modelos estructurados configuracion YAML y reporte final en un pipeline reproducible. | [32-structured_meal_grocery_planner_with_crewai](./32-structured_meal_grocery_planner_with_crewai/README.md) |
| 33 | Agents with Tools versus Tasks with Tools in CrewAI. | Construye un chatbot para The Daily Dish y compara tools dadas al agente contra tools dadas a cada tarea en un flujo tipo `CrewAI`. | A medir por que la asignacion de tools por tarea hace el workflow mas predecible depurable y mantenible. | [33-agents_with_tools_versus_tasks_with_tools_in_crewai](./33-agents_with_tools_versus_tasks_with_tools_in_crewai/README.md) |
| 34 | AI Nutrition Coach with Multi Agent and Multimodal AI. | Construye NourishBot con analisis nutricional recipe remix y una UI `Gradio` sobre imagenes de comidas y agentes especializados. | A combinar vision ligera o multimodal real con agentes de nutricion dieta recetas y una interfaz lista para uso local. | [34-building_your_own_ai_nutrition_coach_using_a_multi_agent_system_and_multimodal_ai](./34-building_your_own_ai_nutrition_coach_using_a_multi_agent_system_and_multimodal_ai/README.md) |
| 35 | Building Agentic AI Systems with the BeeAI Framework. | Construye un tutorial BeeAI compatible con chat plantillas salida estructurada tools requirements aprobaciones y handoffs multiagente. | A entender los conceptos centrales de BeeAI sin depender del runtime real ni de credenciales externas. | [35-building_agentic_ai_systems_with_the_beeai_framework](./35-building_agentic_ai_systems_with_the_beeai_framework/README.md) |
| 36 | AG2 101 Complete Tutorial. | Construye una practica AG2 compatible con agentes conversacionales HITL group chat tools ejecucion local de codigo y salida estructurada. | A aprender los patrones base de AG2 y AutoGen con un flujo local determinista y testeable. | [36-ag2_101_complete_tutorial](./36-ag2_101_complete_tutorial/README.md) |
| 37 | Build a Multi Agent Chatbot with AG2 for Healthcare. | Construye un chatbot sanitario multiagente con roles clinicos y un ejercicio adicional de salud mental usando una capa AG2 compatible. | A modelar colaboracion entre agentes especializados y a coordinar decisiones multiagente en un dominio regulado. | [37-build_a_multi_agent_chatbot_with_ag2_for_healthcare](./37-build_a_multi_agent_chatbot_with_ag2_for_healthcare/README.md) |

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

Prerequisito: arrancar `ollama serve` y descargar `nomic-embed-text`.
Compilacion: `python -m compileall spikes\06-vector_databases_chromadb_cheat_sheet_lab`.
Ejecucion: `python .\spikes\06-vector_databases_chromadb_cheat_sheet_lab\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_06_chromadb_cheat_sheet.py`.

### Practica 07

Prerequisito: arrancar `ollama serve` y descargar `nomic-embed-text`.
Compilacion: `python -m compileall spikes\07-employee_similarity_search_chromadb_lab`.
Ejecucion: `python .\spikes\07-employee_similarity_search_chromadb_lab\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_07_employee_similarity.py`.

### Practica 08

Prerequisito: arrancar `ollama serve` y descargar `nomic-embed-text` y `llama3.2:3b`.
Compilacion: `python -m compileall spikes\08-food_recommendation_systems_chromadb_rag_lab`.
Ejecucion: `python .\spikes\08-food_recommendation_systems_chromadb_rag_lab\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_08_food_recommendation.py`.

### Practica 09

Prerequisito: arrancar `ollama serve` y descargar `nomic-embed-text` y `qwen2.5:7b`.
Compilacion: `python -m compileall spikes\09-langchain_context_retrieval_lab`.
Ejecucion: `python .\spikes\09-langchain_context_retrieval_lab\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_09_context_retrieval.py`.

### Practica 10

Prerequisito: arrancar `ollama serve` y descargar `nomic-embed-text` y `qwen2.5:7b`.
Compilacion: `python -m compileall spikes\10-advanced_retrievers_llamaindex_lab`.
Ejecucion: `python .\spikes\10-advanced_retrievers_llamaindex_lab\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_10_advanced_retrievers_llamaindex.py`.

### Practica 11

Prerequisito: arrancar `ollama serve` y descargar `nomic-embed-text`.
Compilacion: `python -m compileall spikes\11-semantic_similarity_faiss_lab`.
Ejecucion: `python .\spikes\11-semantic_similarity_faiss_lab\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_11_semantic_similarity_faiss.py`.

### Practica 12

Prerequisito: arrancar `ollama serve` y descargar `nomic-embed-text` y `qwen2.5:7b`.
Compilacion: `python -m compileall spikes\12-youtube_summarizer_rag_faiss_lab`.
Ejecucion: `python .\spikes\12-youtube_summarizer_rag_faiss_lab\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_12_youtube_summarizer_rag_faiss.py`.

### Practica 13

Prerequisito: arrancar `ollama serve` y descargar `qwen2.5:7b`.
Compilacion: `python -m compileall spikes\13-story_generator_text_to_speech_lab`.
Ejecucion base: `python .\spikes\13-story_generator_text_to_speech_lab\main.py`.
Variantes: `python .\spikes\13-story_generator_text_to_speech_lab\ollama_mistral_story_tts\main.py` `python .\spikes\13-story_generator_text_to_speech_lab\mistral_api_story_tts\main.py` `python .\spikes\13-story_generator_text_to_speech_lab\ollama_mistral_edge_tts_story_tts\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_13_story_generator_text_to_speech.py tests\unit\test_spike_13_story_generator_real_variants.py`.

### Practica 14

Prerequisito: arrancar `ollama serve` y descargar `qwen2.5vl:3b`.
Compilacion: `python -m compileall spikes\14-basic_vision_multimodal_lab`.
Ejecucion base: `python .\spikes\14-basic_vision_multimodal_lab\main.py`.
Variantes principales: `python .\spikes\14-basic_vision_multimodal_lab\llava_vision_querying\main.py` `python .\spikes\14-basic_vision_multimodal_lab\llama3_2_vision_querying\main.py` `python .\spikes\14-basic_vision_multimodal_lab\qwen2_5vl_vision_querying\main.py`.
Apps extendidas: `python .\spikes\14-basic_vision_multimodal_lab\style_finder_fashion_rag_app\main.py` `python .\spikes\14-basic_vision_multimodal_lab\nutrition_coach_flask_app\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_14_basic_vision_multimodal.py tests\unit\test_spike_14_real_vision_variants.py tests\unit\test_spike_14_style_finder_fashion_rag_app.py tests\unit\test_spike_14_nutrition_coach_flask_app.py`.

### Practica 15

Prerequisito: arrancar `ollama serve` y descargar `llama3.2:3b`.
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

### Practica 20

Prerequisito: arrancar `ollama serve` y descargar `qwen2.5:7b` o `llama3.2:3b`.
Compilacion: `python -m compileall spikes\20-interactive_llm_agents_with_tools_lab`.
Ejecucion: `python .\spikes\20-interactive_llm_agents_with_tools_lab\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_20_interactive_llm_agents_with_tools.py`.

### Practica 21

Dependencias extra: `pip install -U yt-dlp youtube-transcript-api`.
Prerequisito: arrancar `ollama serve` y descargar `qwen2.5:7b` o `llama3.2:3b`.
Compilacion: `python -m compileall spikes\21-youtube_tool_calling_agent_lab`.
Ejecucion: `python .\spikes\21-youtube_tool_calling_agent_lab\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_21_youtube_tool_calling_agent.py`.

### Practica 22

Dependencias extra: `pip install -U langchain-experimental matplotlib seaborn`.
Prerequisito: arrancar `ollama serve` y descargar `qwen2.5:7b` o `llama3.2:3b`.
Compilacion: `python -m compileall spikes\22-natural_language_data_visualization_agent_lab`.
Ejecucion: `python .\spikes\22-natural_language_data_visualization_agent_lab\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_22_natural_language_data_visualization_agent.py`.

### Practica 23

Dependencias extra: `pip install -U langchain-community`.
Prerequisito: arrancar `ollama serve` y descargar `qwen2.5:7b` o `llama3.2:3b`.
Compilacion: `python -m compileall spikes\23-natural_language_sql_agent_lab`.
Ejecucion: `python .\spikes\23-natural_language_sql_agent_lab\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_23_natural_language_sql_agent.py`.

### Practica 24

Dependencias extra: `pip install -U langgraph==0.2.57`.
Prerequisito: arrancar `ollama serve` y descargar `qwen2.5:7b` o `llama3.2:3b`.
Compilacion: `python -m compileall spikes\24-langgraph_101_building_stateful_ai_workflows_lab`.
Ejecucion: `python .\spikes\24-langgraph_101_building_stateful_ai_workflows_lab\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_24_langgraph_101_building_stateful_ai_workflows.py`.

### Practica 25

Dependencias extra: `pip install -U langgraph==0.2.57`.
Dependencia opcional para PNG: `pip install -U pygraphviz==1.14`.
Prerequisito: arrancar `ollama serve` y descargar `qwen2.5:7b` o `llama3.2:3b`.
Compilacion: `python -m compileall spikes\25-building_reflection_agent_with_langgraph_lab`.
Ejecucion: `python .\spikes\25-building_reflection_agent_with_langgraph_lab\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_25_building_reflection_agent_with_langgraph.py`.

### Practica 26

Dependencias extra: `pip install -U langgraph==0.2.57`.
Dependencia opcional para Tavily: `pip install -U tavily-python`.
Prerequisito: arrancar `ollama serve` y descargar `qwen2.5:7b` o `llama3.2:3b`.
Compilacion: `python -m compileall spikes\26-building_reflection_agent_with_external_knowledge_integration`.
Ejecucion: `python .\spikes\26-building_reflection_agent_with_external_knowledge_integration\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_26_building_reflection_agent_with_external_knowledge_integration.py`.

### Practica 27

Dependencias extra: `pip install -U langgraph==0.2.57`.
Dependencia opcional para Tavily: `pip install -U tavily-python`.
Prerequisito: arrancar `ollama serve` y descargar `qwen2.5:7b` o `llama3.2:3b`.
Compilacion: `python -m compileall spikes\27-react_build_reasoning_and_acting_ai_agents_with_langgraph`.
Ejecucion: `python .\spikes\27-react_build_reasoning_and_acting_ai_agents_with_langgraph\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_27_react_build_reasoning_and_acting_ai_agents_with_langgraph.py`.

### Practica 28

Dependencias opcionales: `pip install -U docling python-docx`.
Prerequisito: arrancar `ollama serve` y descargar `qwen2.5:7b` o `llama3.2:3b`.
Compilacion: `python -m compileall spikes\28-docchat_multi_agent_rag_system`.
CLI demo: `python .\spikes\28-docchat_multi_agent_rag_system\main.py`.
UI: `python .\spikes\28-docchat_multi_agent_rag_system\app.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_28_docchat_multi_agent_rag_system.py`.

### Practica 29

Prerequisito: arrancar `ollama serve` y descargar `qwen2.5:7b` o `llama3.2:3b`.
Compilacion: `python -m compileall spikes\29-implement_workflow_patterns_with_langgraph`.
Ejecucion: `python .\spikes\29-implement_workflow_patterns_with_langgraph\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_29_implement_workflow_patterns_with_langgraph.py`.

### Practica 30

Prerequisito: arrancar `ollama serve` y descargar `qwen2.5:7b` o `llama3.2:3b`.
Compilacion: `python -m compileall spikes\30-build_langgraph_design_patterns_orchestration_evaluation`.
Ejecucion: `python .\spikes\30-build_langgraph_design_patterns_orchestration_evaluation\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_30_build_langgraph_design_patterns_orchestration_evaluation.py`.

### Practica 31

Prerequisito: arrancar `ollama serve` y descargar `qwen2.5:7b` o `llama3.2:3b`.
Dependencias opcionales para CrewAI real: `pip install -U crewai crewai-tools`.
Compilacion: `python -m compileall spikes\31-crewai_101_building_multi_agent_ai_systems`.
Ejecucion: `python .\spikes\31-crewai_101_building_multi_agent_ai_systems\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_31_crewai_101_building_multi_agent_ai_systems.py`.

### Practica 32

Prerequisito: arrancar `ollama serve` y descargar `qwen2.5:7b` o `llama3.2:3b`.
Dependencias opcionales para CrewAI real: `pip install -U crewai crewai-tools`.
Compilacion: `python -m compileall spikes\32-structured_meal_grocery_planner_with_crewai`.
Ejecucion: `python .\spikes\32-structured_meal_grocery_planner_with_crewai\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_32_structured_meal_grocery_planner_with_crewai.py`.

### Practica 33

Prerequisito: arrancar `ollama serve` y descargar `qwen2.5:7b` o `llama3.2:3b`.
Dependencias opcionales para CrewAI real: `pip install -U crewai crewai-tools`.
Compilacion: `python -m compileall spikes\33-agents_with_tools_versus_tasks_with_tools_in_crewai`.
Ejecucion: `python .\spikes\33-agents_with_tools_versus_tasks_with_tools_in_crewai\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_33_agents_with_tools_versus_tasks_with_tools_in_crewai.py`.

### Practica 34

Prerequisito: arrancar `ollama serve` y descargar `qwen2.5:7b` y `qwen2.5vl:3b`.
Modelos alternativos de vision: `llava` o `llama3.2-vision`.
Compilacion: `python -m compileall spikes\34-building_your_own_ai_nutrition_coach_using_a_multi_agent_system_and_multimodal_ai`.
Demo CLI: `python .\spikes\34-building_your_own_ai_nutrition_coach_using_a_multi_agent_system_and_multimodal_ai\main.py`.
UI `Gradio`: `python .\spikes\34-building_your_own_ai_nutrition_coach_using_a_multi_agent_system_and_multimodal_ai\app.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_34_building_your_own_ai_nutrition_coach_using_a_multi_agent_system_and_multimodal_ai.py`.

### Practica 35

Dependencias opcionales para BeeAI real: `pip install openai==1.99.9 beeai-framework[wikipedia]==0.1.35 pydantic==2.11.7 pydantic-core==2.33.2`.
Compilacion: `python -m compileall spikes\35-building_agentic_ai_systems_with_the_beeai_framework`.
Ejecucion: `python .\spikes\35-building_agentic_ai_systems_with_the_beeai_framework\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_35_building_agentic_ai_systems_with_the_beeai_framework.py`.

### Practica 36

Dependencias opcionales para AG2 real: `pip install ag2[openai] python-dotenv`.
Compilacion: `python -m compileall spikes\36-ag2_101_complete_tutorial`.
Ejecucion: `python .\spikes\36-ag2_101_complete_tutorial\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_36_ag2_101_complete_tutorial.py`.

### Practica 37

Dependencias opcionales para AutoGen real: `pip install autogen==0.7 openai==1.64.0 python-dotenv==1.1.0`.
Compilacion: `python -m compileall spikes\37-build_a_multi_agent_chatbot_with_ag2_for_healthcare`.
Ejecucion: `python .\spikes\37-build_a_multi_agent_chatbot_with_ag2_for_healthcare\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_37_build_a_multi_agent_chatbot_with_ag2_for_healthcare.py`.

## Ruta de Aprendizaje Sugerida

1. Empieza por `01` y `02` si quieres dominar prompts `LCEL` y una interfaz minima.
2. Sigue con `03` `05` y `06` para entender `RAG` embeddings similitud y bases vectoriales.
3. Continua con `07` y `08` para ver casos de uso concretos de retrieval y recomendacion.
4. Pasa a `09` y `10` cuando quieras profundizar en retrievers avanzados.
5. Cierra con `11` `12` `13` `14` `15` `16` `17` `18` `19` `20` `21` `22` `23` `24` `25` `26` `27` `28` `29` `30` `31` `32` `33` `34` `35` `36` y `37` para trabajar `FAISS` contenido multimedia `Text to Speech` vision multimodal captioning visual apps `Gradio` y `Flask` asistentes de reunion generacion de imagenes control local por voz con permisos `tool calling` moderno en `LangChain` analisis tabular con `pandas` y `scikit-learn` el ciclo manual completo de agentes interactivos con tools la integracion multi paso con YouTube real la visualizacion conversacional de datos con `pandas` consultas SQL en lenguaje natural sobre un esquema relacional workflows con estado en `LangGraph` agentes de reflexion auto mejorables revision guiada por conocimiento externo el patron ReAct completo un DocChat multiagente con retrieval hibrido y verificacion patrones de workflow con `LangGraph` patrones de orquestacion y reflexion pipelines estilo `CrewAI` para contenido y grocery planning una comparativa formal entre tools por agente contra tools por tarea una app multimodal multiagente de coaching nutricional y nuevas practicas sobre patrones BeeAI y AG2 con agents tools approvals handoffs group chat y colaboracion multiagente en salud.

## Nota

La mayoria de practicas estan adaptadas para ejecutarse de forma local y reproducible. Cuando un laboratorio original dependia de servicios externos el repositorio prioriza modelos reales locales como `Ollama` si encajan tecnicamente con el caso de uso. Los datos locales y los mocks de test pueden simplificar el aislamiento de pruebas pero no sustituyen el camino ejecutable principal de cada practica.

Cuando una practica de `spikes` puede resolverse bien con `Ollama` se prioriza esa via. Si la practica es multimodal o el caso de uso no encaja con `Ollama` se debe usar el modelo recomendado en el `README` de la propia practica. Si para ese mismo caso existe una alternativa gratuita y accesible en internet se debe priorizar esa opcion gratuita.
