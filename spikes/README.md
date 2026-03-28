# README de Spikes

Este archivo resume de forma rapida de que va cada practica del directorio `spikes` y que aprendizaje principal deja cada una.

## Convencion de Nombres

1. Convencion oficial para nuevos spikes: `NN-descriptive_project_slug`.
2. `NN` debe usar dos digitos con cero a la izquierda cuando aplique.
3. El slug debe ir en minusculas y separar palabras con guion bajo.
4. Todo spike activo del repositorio usa el mismo patron canonico sin sufijo `_lab`.
5. Los tests nuevos deben reflejar exactamente el slug del spike con el formato `test_spike_NN_descriptive_project_slug.py`.
6. El titulo visible del `README` puede ser mas libre para lectura humana pero el directorio el test y la documentacion global deben usar el mismo slug canonico.

## Vista Rapida

| Practica | Tema | De que va | Que aprendes | Enlace |
| --- | --- | --- | --- | --- |
| 01 | Prompting y LCEL. | Introduce prompts basicos plantillas y composicion de flujos con `LangChain` y `LCEL`. | A estructurar prompts encadenar pasos y razonar sobre salidas de un `LLM` local. | [01-prompting_lcel](./01-prompting_lcel/README.md) |
| 02 | Interfaz con Gradio y Llama. | Construye una interfaz sencilla que conecta formulario estado y modelo local con `Gradio`. | A separar UI estado y acceso a modelo en una app minima de IA. | [02-gradio_llama](./02-gradio_llama/README.md) |
| 03 | RAG sobre PDF. | Implementa un bot de preguntas y respuestas sobre un PDF con carga division embeddings retrieval y respuesta. | A montar un flujo `RAG` clasico de extremo a extremo sobre documentos. | [03-rag_pdf_qa](./03-rag_pdf_qa/README.md) |
| 04 | LinkedIn Icebreaker Bot. | Usa perfiles mock tipo LinkedIn para generar contexto preguntas y respuestas conversacionales con `RAG`. | A convertir datos estructurados en contexto util para personalizacion y conversacion. | [04-linkedin_icebreaker](./04-linkedin_icebreaker/README.md) |
| 05 | Similarity Search by Hand. | Explica la busqueda por similitud desde cero con embeddings normalizacion y calculo manual de metricas. | A entender como funcionan coseno distancia y ranking sin depender de una vector DB. | [05-similarity_search](./05-similarity_search/README.md) |
| 06 | ChromaDB Cheat Sheet. | Resume conceptos de vector databases y demuestra operaciones CRUD consultas y filtros en `ChromaDB`. | A manejar colecciones metadatos y consultas semanticas basicas en una base vectorial. | [06-chromadb_cheat_sheet](./06-chromadb_cheat_sheet/README.md) |
| 07 | Similaridad en empleados y libros. | Aplica `ChromaDB` a dos dominios pequenos con embeddings reales locales y filtros de metadatos. | A modelar colecciones distintas y comparar busqueda semantica con restricciones de negocio. | [07-employee_similarity](./07-employee_similarity/README.md) |
| 08 | Recomendaciones de comida con RAG. | Combina retrieval en `ChromaDB` con generacion para recomendar platos segun consulta contexto y filtros. | A construir un sistema de recomendacion simple apoyado en retrieval y respuesta generada. | [08-food_recommendation_rag](./08-food_recommendation_rag/README.md) |
| 09 | Context Retrieval con LangChain. | Explora `top k` `MMR` `score threshold` `MultiQueryRetriever` `SelfQueryRetriever` y `ParentDocumentRetriever`. | A elegir tecnicas de retrieval segun consulta expansion filtros y preservacion de contexto. | [09-context_retrieval](./09-context_retrieval/README.md) |
| 10 | Advanced Retrievers con LlamaIndex. | Recorre `VectorIndexRetriever` `BM25` `DocumentSummaryIndex` `AutoMergingRetriever` `RecursiveRetriever` y `QueryFusionRetriever`. | A comparar retrievers avanzados y a crear estrategias hibridas y pipelines `RAG` mas robustos. | [10-advanced_retrievers](./10-advanced_retrievers/README.md) |
| 11 | Semantic Similarity con FAISS. | Implementa preprocesamiento vectorizacion e indexacion con `FAISS IndexFlatL2` sobre un corpus local. | A entender el flujo completo de semantic search con un indice vectorial real. | [11-semantic_similarity](./11-semantic_similarity/README.md) |
| 12 | YouTube Summarizer y QA con FAISS. | Procesa transcriptos chunking retrieval con `LangChain FAISS` y genera resumenes y respuestas sobre un video. | A construir una mini aplicacion `RAG` para contenido multimedia basado en transcriptos. | [12-youtube_rag_faiss](./12-youtube_rag_faiss/README.md) |
| 13 | Story Generator y Text to Speech. | Genera una historia educativa con un `LLM` real en `Ollama` y la transforma en audio con `edge-tts` o variantes adicionales. | A combinar prompting generacion de texto y una salida de audio gratuita o local sin perder el objetivo del laboratorio. | [13-story_tts](./13-story_tts/README.md) |
| 14 | Vision Multimodal Basica. | Construye mensajes con imagen y texto responde preguntas visuales con un modelo real de vision en `Ollama` hace captioning en lote matching local contra un catalogo y se extiende con `Style Finder` en `Gradio` y `Nutrition Coach` en `Flask`. | A entender el patron basico de `vision querying` `VQA` `Image Captioning` y como escalarlo a apps completas de `multimodal RAG` para moda y nutricion. | [14-vision_multimodal](./14-vision_multimodal/README.md) |
| 15 | AI Meeting Assistant. | Transcribe audio de reunion normaliza terminos financieros y genera acta con tareas descargables con un modelo real de `Ollama` para la parte textual. | A encadenar `Speech to Text` limpieza de transcript y generacion estructurada en una app de reuniones. | [15-meeting_assistant](./15-meeting_assistant/README.md) |
| 16 | DALL-E Image Generation. | Genera imagenes desde prompts con `dall-e-2` y `dall-e-3` guarda los resultados en archivos locales y define requests configurables para tamano calidad y salida multiple. | A comparar dos versiones reales de la API de imagenes de `OpenAI` y adaptar salidas de notebook a un flujo ejecutable desde terminal. | [16-dalle_generation](./16-dalle_generation/README.md) |
| 17 | Voice Desktop Assistant. | Escucha ordenes desde un canal de voz continuo o desde un campo de texto las transcribe en local con `Whisper` y ejecuta acciones seguras de escritorio con `Ollama` incluyendo clicks visuales sobre la UI de `League of Legends` cierre confirmado de apps envio a papelera con confirmacion verificacion del estado real del proceso al cerrar y un estado resumido en una sola linea. | A combinar audio local `Speech to Text` planificacion segura con `Ollama` vision sobre pantalla y automatizacion de escritorio con una politica de permisos minima. | [17-voice_assistant](./17-voice_assistant/README.md) |
| 18 | LangChain Tool Calling Math Assistant. | Construye un asistente matematico con tools de `LangChain` definidas con `@tool` y `ChatOllama` como modelo principal junto con un catalogo factual local y un bucle controlado de tool calling. | A entender el contrato real de `tool calling` probar herramientas por separado y componer calculos multi paso con un modelo real compatible con el stack del repo. | [18-tool_calling_math](./18-tool_calling_math/README.md) |
| 19 | DataWizard AI Powered Data Analysis. | Construye un asistente de analisis de datos con `LangChain` y `ChatOllama` que descubre CSV locales mantiene una cache de `DataFrame` resume datasets ejecuta metodos seguros de `pandas` y evalua modelos de clasificacion o regresion con `scikit-learn`. | A conectar lenguaje natural con analisis tabular real y a comparar un baseline conversacional sin tools frente a un executor agent con modelo real y workflows multi paso. | [19-datawizard_analysis](./19-datawizard_analysis/README.md) |
| 20 | Interactive LLM Agents with Tools. | Construye un laboratorio de `manual tool calling` con `LangChain` y `ChatOllama` que define tools aritmeticas y de propina parsea `tool_calls` ejecuta `ToolMessage` y encapsula el flujo en agentes interactivos. | A entender paso a paso como se enlaza un modelo con herramientas reales y como convertir ese ciclo en clases de agente reutilizables. | [20-interactive_agents](./20-interactive_agents/README.md) |
| 21 | YouTube Tool Calling Agent. | Construye un agente con `LangChain` y `ChatOllama` que usa tools reales de YouTube para extraer `video_id` buscar videos recuperar transcriptos leer metadatos y thumbnails y automatizar tanto un flujo fijo como una cadena recursiva. | A llevar el `tool calling` a un caso multi paso contra servicios externos reales y a comparar orquestacion manual automatizada y recursiva. | [21-youtube_tool_agent](./21-youtube_tool_agent/README.md) |
| 22 | Natural Language Data Visualization Agent. | Construye un agente de `LangChain` con `create_pandas_dataframe_agent` y `ChatOllama` para consultar un CSV en lenguaje natural generar charts y extraer el Python usado para cada respuesta o visualizacion. | A unir analisis tabular conversacional con graficos reproducibles en disco y a inspeccionar el codigo que el agente ejecuta sobre `pandas` y `matplotlib`. | [22-nl_data_viz](./22-nl_data_viz/README.md) |
| 23 | Natural Language SQL Agent. | Construye un agente SQL de `LangChain` con `ChatOllama` y una base Chinook local en `SQLite` para traducir preguntas en lenguaje natural a consultas SQL inspeccionables. | A levantar una base relacional reproducible conectar `SQLDatabase Toolkit` y revisar las sentencias SQL que el agente ejecuta sobre un esquema real. | [23-nl_sql](./23-nl_sql/README.md) |
| 24 | LangGraph 101 Stateful AI Workflows. | Construye tres workflows con `LangGraph`: autenticacion con reintentos QA contextual sobre el propio lab y un contador ciclico basado en nodos y aristas condicionales. | A modelar estado compartido nodos aristas condicionales y ciclos reproducibles con `StateGraph` y `ChatOllama`. | [24-langgraph_stateful_workflows](./24-langgraph_stateful_workflows/README.md) |
| 25 | Reflection Agent with LangGraph. | Construye un agente reflexivo con `MessageGraph` que genera un post de LinkedIn critica su propio borrador y lo refina en varias iteraciones. | A modelar historiales de mensajes routers condicionales y bucles de auto mejora con `LangGraph` y `ChatOllama`. | [25-reflection_agent](./25-reflection_agent/README.md) |
| 26 | Reflection Agent with External Knowledge. | Construye un agente reflexivo que responde se critica usa conocimiento externo y revisa su respuesta con evidencia adicional. | A combinar `MessageGraph` `ToolMessage` salida estructurada y busqueda externa real dentro de un bucle reflexivo. | [26-reflection_external_knowledge](./26-reflection_external_knowledge/README.md) |
| 27 | ReAct Agents with LangGraph. | Construye un agente ReAct con `StateGraph` que razona usa herramientas de busqueda clima calculo y resumen de noticias y decide cuando detenerse. | A implementar el ciclo razonar actuar observar con `add_messages` `ToolMessage` y tool calling moderno sobre `ChatOllama`. | [27-react_langgraph_agents](./27-react_langgraph_agents/README.md) |
| 28 | DocChat Multi Agent RAG. | Construye un sistema DocChat con parser cacheado retrieval hibrido y tres agentes para relevancia investigacion y verificacion sobre documentos largos. | A combinar procesamiento documental `Chroma` BM25 `LangGraph` y una UI `Gradio` en un flujo multiagente grounded. | [28-docchat_multi_agent_rag](./28-docchat_multi_agent_rag/README.md) |
| 29 | Workflow Patterns with LangGraph. | Construye ejemplos ejecutables de prompt chaining routing parallelization y un router multiagente de servicios. | A reconocer los tres patrones base de workflows con `LangGraph` y a implementarlos sobre `ChatOllama`. | [29-langgraph_workflow_patterns](./29-langgraph_workflow_patterns/README.md) |
| 30 | LangGraph Orchestration and Evaluation. | Construye un patron orchestrator worker para planificacion de comidas y un patron de reflection para planes de inversion. | A coordinar workers en paralelo con `Send` y a cerrar bucles de generacion evaluacion y refinamiento. | [30-langgraph_design_patterns](./30-langgraph_design_patterns/README.md) |
| 31 | CrewAI 101 Multi Agent Systems. | Construye un pipeline de investigacion redaccion y social media siguiendo el modelo conceptual de `CrewAI`. | A separar agentes tareas y crews secuenciales para transformar research en contenido publicable. | [31-crewai_multi_agent](./31-crewai_multi_agent/README.md) |
| 32 | Structured Meal Grocery Planner with CrewAI. | Construye un sistema de meal planning y grocery planning con modelos `Pydantic` YAML y un flujo multiagente estilo `CrewAI`. | A combinar agentes especializados modelos estructurados configuracion YAML y reporte final en un pipeline reproducible. | [32-meal_grocery_planner](./32-meal_grocery_planner/README.md) |
| 33 | Agents with Tools versus Tasks with Tools in CrewAI. | Construye un chatbot para The Daily Dish y compara tools dadas al agente contra tools dadas a cada tarea en un flujo tipo `CrewAI`. | A medir por que la asignacion de tools por tarea hace el workflow mas predecible depurable y mantenible. | [33-crewai_tools_vs_tasks](./33-crewai_tools_vs_tasks/README.md) |
| 34 | AI Nutrition Coach with Multi Agent and Multimodal AI. | Construye NourishBot con analisis nutricional recipe remix y una UI `Gradio` sobre imagenes de comidas y agentes especializados. | A combinar vision ligera o multimodal real con agentes de nutricion dieta recetas y una interfaz lista para uso local. | [34-nutrition_coach_multi_agent](./34-nutrition_coach_multi_agent/README.md) |
| 35 | Building Agentic AI Systems with the BeeAI Framework. | Construye un tutorial BeeAI compatible con chat plantillas salida estructurada tools requirements aprobaciones y handoffs multiagente. | A entender los conceptos centrales de BeeAI sin depender del runtime real ni de credenciales externas. | [35-beeai_agentic_systems](./35-beeai_agentic_systems/README.md) |
| 36 | AG2 101 Complete Tutorial. | Construye una practica AG2 compatible con agentes conversacionales HITL group chat tools ejecucion local de codigo y salida estructurada. | A aprender los patrones base de AG2 y AutoGen con un flujo local determinista y testeable. | [36-ag2_tutorial](./36-ag2_tutorial/README.md) |
| 37 | Build a Multi Agent Chatbot with AG2 for Healthcare. | Construye un chatbot sanitario multiagente con roles clinicos y un ejercicio adicional de salud mental usando una capa AG2 compatible. | A modelar colaboracion entre agentes especializados y a coordinar decisiones multiagente en un dominio regulado. | [37-ag2_healthcare_chatbot](./37-ag2_healthcare_chatbot/README.md) |
| 38 | Run Existing MCP Servers. | Construye un laboratorio con `FastMCP Client` y un servidor Context7 compatible local para practicar `STDIO` y `HTTP` con las mismas tools. | A entender que el transporte cambia el cable de conexion pero no la forma de listar ni llamar tools MCP. | [38-mcp_existing_servers](./38-mcp_existing_servers/README.md) |
| 39 | Build an MCP Application. | Construye una aplicacion con `MultiServerMCPClient` que combina documentacion tipo Context7 por HTTP y un catalogo del Met Museum por STDIO. | A coordinar varios servidores MCP desde un solo host y a dar memoria de sesion a un agente que usa sus tools. | [39-mcp_application](./39-mcp_application/README.md) |
| 40 | Hello World of MCP Servers. | Construye un servidor `FastMCP` con tools resources y prompts y lo prueba por `in-memory` `HTTP` `STDIO` y escenario multi servidor. | A dominar el flujo basico de creacion y consumo de servidores MCP antes de pasar a clientes mas custom. | [40-mcp_hello_world](./40-mcp_hello_world/README.md) |
| 41 | Build an Enhanced MCP Server. | Construye un servidor MCP enriquecido para archivos con `Context` progreso logging recursos prompts y un cliente CLI asociado. | A usar `ctx.report_progress` `ctx.elicit` y workflows guiados por prompts sobre tools de escritura y lectura de archivos. | [41-enhanced_mcp_server](./41-enhanced_mcp_server/README.md) |
| 42 | Build a Custom MCP Client with Python. | Construye un cliente MCP minimo con `ClientSession` y `stdio_client` para descubrir tools leer recursos y renderizar prompts. | A bajar al nivel del SDK MCP y entender el handshake la sesion y el patron de lectura de URIs desde un cliente propio. | [42-custom_mcp_client](./42-custom_mcp_client/README.md) |
| 43 | Advanced MCP Applications with Streamable HTTP Roots and Sampling. | Construye un servidor HTTP con `FastMCP` y un cliente base con `ClientSession` que soporta roots declarados por el cliente y sampling iniciado por servidor. | A dominar patrones remotos de MCP con `Streamable HTTP` boundaries de filesystem y callbacks de sampling reales. | [43-mcp_http_roots_sampling](./43-mcp_http_roots_sampling/README.md) |
| 44 | MCP Security with Permissions and Elicitation. | Construye un sistema MCP con permisos `allow` `deny` `ask` auditoria y aprobaciones estructuradas usando `ctx.elicit`. | A aplicar controles de seguridad de cliente y servidor para operaciones sensibles con trazabilidad completa. | [44-mcp_security_permissions](./44-mcp_security_permissions/README.md) |

## Guia de Prueba

Estas instrucciones asumen que estas en la raiz del repositorio y que ya activaste el entorno con `.\venv\Scripts\Activate.ps1`. Cuando una practica usa `Ollama` debes arrancar `ollama serve` antes de ejecutarla y descargar los modelos indicados en el `README` propio del spike.

### Practica 01

Compilacion: `python -m compileall spikes\01-prompting_lcel`.
Ejecucion: `python .\spikes\01-prompting_lcel\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_01_prompting_lcel_lcel.py`.

### Practica 02

Compilacion: `python -m compileall spikes\02-gradio_llama`.
Ejecucion: `python .\spikes\02-gradio_llama\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_02_gradio_llama.py`.

### Practica 03

Compilacion: `python -m compileall spikes\03-rag_pdf_qa`.
Ejecucion: `python .\spikes\03-rag_pdf_qa\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_03_rag_pdf_qa.py`.

### Practica 04

Compilacion: `python -m compileall spikes\04-linkedin_icebreaker`.
Ejecucion: `python .\spikes\04-linkedin_icebreaker\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_04_linkedin_icebreaker.py`.

### Practica 05

Dependencias extra: `pip install -U sentence-transformers==4.1.0 scipy torch`.
Compilacion: `python -m compileall spikes\05-similarity_search`.
Ejecucion: `python .\spikes\05-similarity_search\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_05_similarity_search.py`.

### Practica 06

Prerequisito: arrancar `ollama serve` y descargar `nomic-embed-text`.
Compilacion: `python -m compileall spikes\06-chromadb_cheat_sheet`.
Ejecucion: `python .\spikes\06-chromadb_cheat_sheet\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_06_chromadb_cheat_sheet.py`.

### Practica 07

Prerequisito: arrancar `ollama serve` y descargar `nomic-embed-text`.
Compilacion: `python -m compileall spikes\07-employee_similarity`.
Ejecucion: `python .\spikes\07-employee_similarity\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_07_employee_similarity.py`.

### Practica 08

Prerequisito: arrancar `ollama serve` y descargar `nomic-embed-text` y `llama3.2:3b`.
Compilacion: `python -m compileall spikes\08-food_recommendation_rag`.
Ejecucion: `python .\spikes\08-food_recommendation_rag\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_08_food_recommendation_rag_rag.py`.

### Practica 09

Prerequisito: arrancar `ollama serve` y descargar `nomic-embed-text` y `qwen2.5:7b`.
Compilacion: `python -m compileall spikes\09-context_retrieval`.
Ejecucion: `python .\spikes\09-context_retrieval\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_09_context_retrieval.py`.

### Practica 10

Prerequisito: arrancar `ollama serve` y descargar `nomic-embed-text` y `qwen2.5:7b`.
Compilacion: `python -m compileall spikes\10-advanced_retrievers`.
Ejecucion: `python .\spikes\10-advanced_retrievers\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_10_advanced_retrievers.py`.

### Practica 11

Prerequisito: arrancar `ollama serve` y descargar `nomic-embed-text`.
Compilacion: `python -m compileall spikes\11-semantic_similarity`.
Ejecucion: `python .\spikes\11-semantic_similarity\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_11_semantic_similarity.py`.

### Practica 12

Prerequisito: arrancar `ollama serve` y descargar `nomic-embed-text` y `qwen2.5:7b`.
Compilacion: `python -m compileall spikes\12-youtube_rag_faiss`.
Ejecucion: `python .\spikes\12-youtube_rag_faiss\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_12_youtube_rag_faiss.py`.

### Practica 13

Prerequisito: arrancar `ollama serve` y descargar `qwen2.5:7b`.
Compilacion: `python -m compileall spikes\13-story_tts`.
Ejecucion base: `python .\spikes\13-story_tts\main.py`.
Variantes: `python .\spikes\13-story_tts\ollama_mistral_story_tts\main.py` `python .\spikes\13-story_tts\mistral_api_story_tts\main.py` `python .\spikes\13-story_tts\ollama_mistral_edge_tts_story_tts\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_13_story_tts.py tests\unit\test_spike_13_story_tts_real_variants.py`.

### Practica 14

Prerequisito: arrancar `ollama serve` y descargar `qwen2.5vl:3b`.
Compilacion: `python -m compileall spikes\14-vision_multimodal`.
Ejecucion base: `python .\spikes\14-vision_multimodal\main.py`.
Variantes principales: `python .\spikes\14-vision_multimodal\llava_vision_querying\main.py` `python .\spikes\14-vision_multimodal\llama3_2_vision_querying\main.py` `python .\spikes\14-vision_multimodal\qwen2_5vl_vision_querying\main.py`.
Apps extendidas: `python .\spikes\14-vision_multimodal\style_finder_fashion_rag_app\main.py` `python .\spikes\14-vision_multimodal\nutrition_coach_flask_app\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_14_vision_multimodal.py tests\unit\test_spike_14_vision_multimodal_real_variants.py tests\unit\test_spike_14_vision_multimodal_style_finder.py tests\unit\test_spike_14_vision_multimodal_nutrition_coach.py`.

### Practica 15

Prerequisito: arrancar `ollama serve` y descargar `llama3.2:3b`.
Compilacion: `python -m compileall spikes\15-meeting_assistant`.
Ejecucion: `python .\spikes\15-meeting_assistant\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_15_meeting_assistant.py`.

### Practica 16

Prerequisito: exportar `OPENAI_API_KEY` si quieres probar las variantes reales.
Compilacion: `python -m compileall spikes\16-dalle_generation`.
Ejecucion base: `python .\spikes\16-dalle_generation\main.py`.
Variantes: `python .\spikes\16-dalle_generation\dall_e_2_generation\main.py` `python .\spikes\16-dalle_generation\dall_e_3_generation\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_16_dalle_generation.py`.

### Practica 17

Dependencias extra: `pip install -U transformers torch sounddevice pyautogui Send2Trash`.
Dependencia opcional del runner de consola: `pip install -U keyboard`.
Compilacion: `python -m compileall src spikes\17-voice_assistant`.
Ejecucion: `python .\spikes\17-voice_assistant\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_17_voice_assistant.py`.

### Practica 18

Prerequisito: arrancar `ollama serve` y descargar `qwen2.5:7b` o `llama3.2:3b`.
Compilacion: `python -m compileall spikes\18-tool_calling_math`.
Ejecucion: `python .\spikes\18-tool_calling_math\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_18_tool_calling_math.py`.

### Practica 19

Dependencias extra: `pip install -U pandas numpy scikit-learn`.
Prerequisito: arrancar `ollama serve` y descargar `qwen2.5:7b` o `llama3.2:3b`.
Compilacion: `python -m compileall spikes\19-datawizard_analysis`.
Ejecucion: `python .\spikes\19-datawizard_analysis\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_19_datawizard_analysis.py`.

### Practica 20

Prerequisito: arrancar `ollama serve` y descargar `qwen2.5:7b` o `llama3.2:3b`.
Compilacion: `python -m compileall spikes\20-interactive_agents`.
Ejecucion: `python .\spikes\20-interactive_agents\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_20_interactive_agents.py`.

### Practica 21

Dependencias extra: `pip install -U yt-dlp youtube-transcript-api`.
Prerequisito: arrancar `ollama serve` y descargar `qwen2.5:7b` o `llama3.2:3b`.
Compilacion: `python -m compileall spikes\21-youtube_tool_agent`.
Ejecucion: `python .\spikes\21-youtube_tool_agent\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_21_youtube_tool_agent.py`.

### Practica 22

Dependencias extra: `pip install -U langchain-experimental matplotlib seaborn`.
Prerequisito: arrancar `ollama serve` y descargar `qwen2.5:7b` o `llama3.2:3b`.
Compilacion: `python -m compileall spikes\22-nl_data_viz`.
Ejecucion: `python .\spikes\22-nl_data_viz\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_22_nl_data_viz.py`.

### Practica 23

Dependencias extra: `pip install -U langchain-community`.
Prerequisito: arrancar `ollama serve` y descargar `qwen2.5:7b` o `llama3.2:3b`.
Compilacion: `python -m compileall spikes\23-nl_sql`.
Ejecucion: `python .\spikes\23-nl_sql\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_23_nl_sql.py`.

### Practica 24

Dependencias extra: `pip install -U langgraph==0.2.57`.
Prerequisito: arrancar `ollama serve` y descargar `qwen2.5:7b` o `llama3.2:3b`.
Compilacion: `python -m compileall spikes\24-langgraph_stateful_workflows`.
Ejecucion: `python .\spikes\24-langgraph_stateful_workflows\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_24_langgraph_stateful_workflows.py`.

### Practica 25

Dependencias extra: `pip install -U langgraph==0.2.57`.
Dependencia opcional para PNG: `pip install -U pygraphviz==1.14`.
Prerequisito: arrancar `ollama serve` y descargar `qwen2.5:7b` o `llama3.2:3b`.
Compilacion: `python -m compileall spikes\25-reflection_agent`.
Ejecucion: `python .\spikes\25-reflection_agent\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_25_reflection_agent.py`.

### Practica 26

Dependencias extra: `pip install -U langgraph==0.2.57`.
Dependencia opcional para Tavily: `pip install -U tavily-python`.
Prerequisito: arrancar `ollama serve` y descargar `qwen2.5:7b` o `llama3.2:3b`.
Compilacion: `python -m compileall spikes\26-reflection_external_knowledge`.
Ejecucion: `python .\spikes\26-reflection_external_knowledge\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_26_reflection_external_knowledge.py`.

### Practica 27

Dependencias extra: `pip install -U langgraph==0.2.57`.
Dependencia opcional para Tavily: `pip install -U tavily-python`.
Prerequisito: arrancar `ollama serve` y descargar `qwen2.5:7b` o `llama3.2:3b`.
Compilacion: `python -m compileall spikes\27-react_langgraph_agents`.
Ejecucion: `python .\spikes\27-react_langgraph_agents\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_27_react_langgraph_agents.py`.

### Practica 28

Dependencias opcionales: `pip install -U docling python-docx`.
Prerequisito: arrancar `ollama serve` y descargar `qwen2.5:7b` o `llama3.2:3b`.
Compilacion: `python -m compileall spikes\28-docchat_multi_agent_rag`.
CLI demo: `python .\spikes\28-docchat_multi_agent_rag\main.py`.
UI: `python .\spikes\28-docchat_multi_agent_rag\app.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_28_docchat_multi_agent_rag.py`.

### Practica 29

Prerequisito: arrancar `ollama serve` y descargar `qwen2.5:7b` o `llama3.2:3b`.
Compilacion: `python -m compileall spikes\29-langgraph_workflow_patterns`.
Ejecucion: `python .\spikes\29-langgraph_workflow_patterns\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_29_langgraph_workflow_patterns.py`.

### Practica 30

Prerequisito: arrancar `ollama serve` y descargar `qwen2.5:7b` o `llama3.2:3b`.
Compilacion: `python -m compileall spikes\30-langgraph_design_patterns`.
Ejecucion: `python .\spikes\30-langgraph_design_patterns\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_30_langgraph_design_patterns.py`.

### Practica 31

Prerequisito: arrancar `ollama serve` y descargar `qwen2.5:7b` o `llama3.2:3b`.
Dependencias opcionales para CrewAI real: `pip install -U crewai crewai-tools`.
Compilacion: `python -m compileall spikes\31-crewai_multi_agent`.
Ejecucion: `python .\spikes\31-crewai_multi_agent\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_31_crewai_multi_agent.py`.

### Practica 32

Prerequisito: arrancar `ollama serve` y descargar `qwen2.5:7b` o `llama3.2:3b`.
Dependencias opcionales para CrewAI real: `pip install -U crewai crewai-tools`.
Compilacion: `python -m compileall spikes\32-meal_grocery_planner`.
Ejecucion: `python .\spikes\32-meal_grocery_planner\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_32_meal_grocery_planner.py`.

### Practica 33

Prerequisito: arrancar `ollama serve` y descargar `qwen2.5:7b` o `llama3.2:3b`.
Dependencias opcionales para CrewAI real: `pip install -U crewai crewai-tools`.
Compilacion: `python -m compileall spikes\33-crewai_tools_vs_tasks`.
Ejecucion: `python .\spikes\33-crewai_tools_vs_tasks\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_33_crewai_tools_vs_tasks.py`.

### Practica 34

Prerequisito: arrancar `ollama serve` y descargar `qwen2.5:7b` y `qwen2.5vl:3b`.
Modelos alternativos de vision: `llava` o `llama3.2-vision`.
Compilacion: `python -m compileall spikes\34-nutrition_coach_multi_agent`.
Demo CLI: `python .\spikes\34-nutrition_coach_multi_agent\main.py`.
UI `Gradio`: `python .\spikes\34-nutrition_coach_multi_agent\app.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_34_nutrition_coach_multi_agent.py`.

### Practica 35

Dependencias opcionales para BeeAI real: `pip install openai==1.99.9 beeai-framework[wikipedia]==0.1.35 pydantic==2.11.7 pydantic-core==2.33.2`.
Compilacion: `python -m compileall spikes\35-beeai_agentic_systems`.
Ejecucion: `python .\spikes\35-beeai_agentic_systems\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_35_beeai_agentic_systems.py`.

### Practica 36

Dependencias opcionales para AG2 real: `pip install ag2[openai] python-dotenv`.
Compilacion: `python -m compileall spikes\36-ag2_tutorial`.
Ejecucion: `python .\spikes\36-ag2_tutorial\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_36_ag2_tutorial.py`.

### Practica 37

Dependencias opcionales para AutoGen real: `pip install autogen==0.7 openai==1.64.0 python-dotenv==1.1.0`.
Compilacion: `python -m compileall spikes\37-ag2_healthcare_chatbot`.
Ejecucion: `python .\spikes\37-ag2_healthcare_chatbot\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_37_ag2_healthcare_chatbot.py`.

### Practica 38

Dependencias MCP: `pip install fastmcp==2.12.5 mcp==1.16.0`.
Opcional para el Context7 real: instalar Node.js y usar `npx -y @upstash/context7-mcp`.
Compilacion: `python -m compileall spikes\38-mcp_existing_servers`.
Ejecucion: `python .\spikes\38-mcp_existing_servers\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_38_mcp_existing_servers.py`.

### Practica 39

Dependencias MCP: `pip install fastmcp==2.12.5 mcp==1.16.0 langchain-mcp-adapters==0.1.9`.
Compilacion: `python -m compileall spikes\39-mcp_application`.
Ejecucion: `python .\spikes\39-mcp_application\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_39_mcp_application.py`.

### Practica 40

Dependencias MCP: `pip install fastmcp==2.12.5 mcp==1.16.0 langchain-mcp-adapters==0.1.9`.
Compilacion: `python -m compileall spikes\40-mcp_hello_world`.
Ejecucion: `python .\spikes\40-mcp_hello_world\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_40_mcp_hello_world.py`.

### Practica 41

Dependencias MCP: `pip install fastmcp==2.12.5`.
Compilacion: `python -m compileall spikes\41-enhanced_mcp_server`.
Ejecucion: `python .\spikes\41-enhanced_mcp_server\main.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_41_enhanced_mcp_server.py`.

### Practica 42

Dependencias MCP: `pip install fastmcp==2.12.5 mcp==1.16.0`.
Compilacion: `python -m compileall spikes\42-custom_mcp_client`.
Demo programatica: `python .\spikes\42-custom_mcp_client\main.py`.
CLI interactiva: `python .\spikes\42-custom_mcp_client\mcp_client.py .\spikes\42-custom_mcp_client\mcp_server.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_42_custom_mcp_client.py`.

### Practica 43

Dependencias opcionales de UI y LLM: `pip install httpx==0.28.1 gradio==5.49.1 openai==2.6.1`.
Compilacion: `python -m compileall spikes\43-mcp_http_roots_sampling`.
Demo programatica: `python .\spikes\43-mcp_http_roots_sampling\main.py`.
GUI opcional: `python .\spikes\43-mcp_http_roots_sampling\models\advanced_http_client_app.py http://127.0.0.1:8000 .\spikes\43-mcp_http_roots_sampling\workspace`.
Host opcional: `python .\spikes\43-mcp_http_roots_sampling\models\advanced_http_host_app.py http://127.0.0.1:8000 .\spikes\43-mcp_http_roots_sampling\workspace`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_43_mcp_http_roots_sampling.py`.

### Practica 44

Dependencias opcionales de UI y LLM: `pip install gradio==5.49.1 openai==2.6.1`.
Compilacion: `python -m compileall spikes\44-mcp_security_permissions`.
Demo programatica: `python .\spikes\44-mcp_security_permissions\main.py`.
GUI opcional: `python .\spikes\44-mcp_security_permissions\models\permission_client_app.py .\spikes\44-mcp_security_permissions\models\permission_mcp_server.py`.
Host opcional: `python .\spikes\44-mcp_security_permissions\models\permission_host_app.py .\spikes\44-mcp_security_permissions\models\permission_mcp_server.py`.
Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_44_mcp_security_permissions.py`.

## Ruta de Aprendizaje Sugerida

1. Empieza por `01` y `02` si quieres dominar prompts `LCEL` y una interfaz minima.
2. Sigue con `03` `05` y `06` para entender `RAG` embeddings similitud y bases vectoriales.
3. Continua con `07` y `08` para ver casos de uso concretos de retrieval y recomendacion.
4. Pasa a `09` y `10` cuando quieras profundizar en retrievers avanzados.
5. Cierra con `11` `12` `13` `14` `15` `16` `17` `18` `19` `20` `21` `22` `23` `24` `25` `26` `27` `28` `29` `30` `31` `32` `33` `34` `35` `36` `37` `38` `39` `40` `41` `42` `43` y `44` para trabajar `FAISS` contenido multimedia `Text to Speech` vision multimodal captioning visual apps `Gradio` y `Flask` asistentes de reunion generacion de imagenes control local por voz con permisos `tool calling` moderno en `LangChain` analisis tabular con `pandas` y `scikit-learn` el ciclo manual completo de agentes interactivos con tools la integracion multi paso con YouTube real la visualizacion conversacional de datos con `pandas` consultas SQL en lenguaje natural sobre un esquema relacional workflows con estado en `LangGraph` agentes de reflexion auto mejorables revision guiada por conocimiento externo el patron ReAct completo un DocChat multiagente con retrieval hibrido y verificacion patrones de workflow con `LangGraph` patrones de orquestacion y reflexion pipelines estilo `CrewAI` para contenido y grocery planning una comparativa formal entre tools por agente contra tools por tarea una app multimodal multiagente de coaching nutricional nuevas practicas sobre patrones BeeAI y AG2 con agents tools approvals handoffs group chat y colaboracion multiagente en salud y un bloque completo de MCP con servidores existentes hosts multi servidor FastMCP Context prompts resources clientes custom sobre `ClientSession` transporte `Streamable HTTP` roots sampling y controles de seguridad con permisos auditoria y `elicitation`.

## Nota

La mayoria de practicas estan adaptadas para ejecutarse de forma local y reproducible. Cuando un laboratorio original dependia de servicios externos el repositorio prioriza modelos reales locales como `Ollama` si encajan tecnicamente con el caso de uso. Los datos locales y los mocks de test pueden simplificar el aislamiento de pruebas pero no sustituyen el camino ejecutable principal de cada practica.

Cuando una practica de `spikes` puede resolverse bien con `Ollama` se prioriza esa via. Si la practica es multimodal o el caso de uso no encaja con `Ollama` se debe usar el modelo recomendado en el `README` de la propia practica. Si para ese mismo caso existe una alternativa gratuita y accesible en internet se debe priorizar esa opcion gratuita.
