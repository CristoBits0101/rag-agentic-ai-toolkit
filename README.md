# COMANDOS

## Instalacion de dependencias

```bash
# 1) Crear entorno virtual.
python -m venv .venv

# 2) Activar entorno.
.\.venv\Scripts\Activate.ps1

# 3) Actualizar pip.
python -m pip install --upgrade pip

# 4) Instalar todo desde requirements.txt.
pip install -r requirements.txt
```

## Instalacion paquetes individuales

```bash
# FastAPI: Framework principal para exponer la API.
pip install -U fastapi

# Uvicorn: Servidor ASGI para desarrollo y ejecucion local.
pip install -U "uvicorn[standard]"

# Gunicorn: Gestor de procesos para despliegues en produccion.
pip install -U gunicorn

# Pydantic Settings: Configuracion tipada desde variables de entorno.
pip install -U pydantic-settings

# pypdf: Lectura de documentos PDF.
pip install -U pypdf

# LangChain: Orquestacion de prompts cadenas y agentes.
pip install -U langchain

# LangChain Community: Cargadores de documentos y vector stores.
pip install -U langchain-community

# LangChain Core: Primitivas base e interfaces compartidas.
pip install -U langchain-core

# LangChain Experimental: Agent toolkits avanzados como el DataFrame agent de la practica 22.
pip install -U langchain-experimental

# LangChain Ollama: Integracion con modelos servidos por Ollama.
pip install -U langchain-ollama

# LangGraph: Workflows con estado nodos y aristas condicionales para las practicas 24 y 25.
pip install -U langgraph==0.2.57

# Tavily Python: Cliente opcional para busqueda web externa en la practica 26.
pip install -U tavily-python

# ChromaDB: Base de datos vectorial para retrieval local.
pip install -U chromadb

# FAISS CPU: Indice vectorial para busqueda por similitud.
pip install -U faiss-cpu==1.13.2

# LlamaIndex Core: Componentes base para indices y retrievers.
pip install -U llama-index-core==0.12.49

# LlamaIndex BM25: Retriever lexico para busqueda avanzada.
pip install -U llama-index-retrievers-bm25==0.5.2

# Rank BM25: Implementacion del ranking BM25.
pip install -U rank-bm25==0.2.2

# PyStemmer: Stemming para BM25 sobre texto.
pip install -U PyStemmer==2.2.0.3

# Lark: Parser requerido por SelfQueryRetriever de LangChain.
pip install -U lark==1.1.9

# Python Dotenv: Carga variables de entorno desde archivos .env.
pip install -U python-dotenv

# PyYAML: Lectura y escritura de archivos YAML.
pip install -U PyYAML

# Pandas y NumPy: Analisis tabular y calculo numerico para la practica 19.
pip install -U pandas numpy

# Scikit Learn: Entrenamiento y evaluacion de modelos para la practica 19.
pip install -U scikit-learn

# Matplotlib y Seaborn: Visualizacion para la practica 22.
pip install -U matplotlib seaborn

# Gradio: Interfaces web rapidas para demos y pruebas.
pip install -U gradio

# Flask: Framework web ligero usado por la extension Nutrition Coach de la practica 14.
pip install -U flask

# gTTS: Sintesis de voz opcional para la practica 13.
pip install -U gTTS

# edge-tts: Sintesis de voz gratuita para la variante real de la practica 13.
pip install -U edge-tts

# youtube-transcript-api: Recuperacion de transcriptos reales para la practica 21.
pip install -U youtube-transcript-api

# yt-dlp: Busqueda y metadatos de YouTube para la practica 21.
pip install -U yt-dlp

# OpenAI: Cliente oficial para la practica 16 de generacion de imagenes.
pip install -U openai

# Transformers y Torch: Soporte opcional para Whisper en la practica 15.
pip install -U transformers torch

# sounddevice: Captura de audio desde microfono para la practica 17.
pip install -U sounddevice

# keyboard: Deteccion local de la tecla push to talk en el runner de consola de la practica 17.
pip install -U keyboard

# PyAutoGUI: Automatizacion de teclado para la practica 17.
pip install -U pyautogui

# Send2Trash: Envio seguro a la papelera para la practica 17.
pip install -U Send2Trash

# Torchvision: Soporte opcional para ResNet50 en la extension Style Finder de la practica 14.
pip install -U torchvision

# Hugging Face Hub: Acceso a modelos datasets y artefactos.
pip install -U huggingface_hub
```

## Ollama

```bash
# Instalar Ollama.
irm https://ollama.com/install.ps1 | iex

# Descargar un modelo local de ejemplo.
ollama pull llama3.2:3b

# Descargar embeddings locales para practicas vectoriales.
ollama pull nomic-embed-text

# Descargar un modelo de texto recomendado para retrievers y tool calling.
ollama pull qwen2.5:7b

# Descargar un modelo de vision recomendado para practica 14.
ollama pull qwen2.5vl:3b

# Verificar.
ollama --version
ollama list
```

## Politica de Modelos para Practicas

Para las practicas de `spikes` se prioriza `Ollama` cuando la tarea puede resolverse bien con modelos locales de texto o embeddings compatibles con el repositorio. Si una practica multimodal o cualquier ejercicio de IA no encaja correctamente con `Ollama` se debe usar el modelo recomendado por la propia practica. Si existe una variante gratuita y accesible en internet que cubra ese mismo caso de uso de forma razonable esa opcion gratuita debe priorizarse frente a alternativas privativas o de pago. Los mocks y fakes solo se permiten en tests. El camino ejecutable principal de cada practica debe usar modelos reales locales o gratuitos.

## Ejecutar Gradio

```powershell
# Activar el entorno virtual.
.\venv\Scripts\Activate.ps1

# Ejecutar la practica de Gradio.
python .\spikes\02-gradio_llama_lab\main.py

# Abrir la interfaz en el navegador.
http://127.0.0.1:7860
```

## Ejecutar Practica 04

```powershell
# Activar el entorno virtual.
.\venv\Scripts\Activate.ps1

# Ejecutar la practica de LinkedIn Icebreaker con Ollama.
python .\spikes\04-linkedin_icebreaker_bot_lab\main.py

# Abrir la interfaz en el navegador.
http://127.0.0.1:7861
```

## Ejecutar Practica 05

```powershell
# Activar el entorno virtual.
.\venv\Scripts\Activate.ps1

# Instalar dependencias del laboratorio de similitud.
pip install -U sentence-transformers==4.1.0 scipy torch

# Ejecutar la practica de similitud vectorial.
python .\spikes\05-similarity_search_by_hand_lab\main.py
```

## Ejecutar Practica 06

```powershell
# Activar el entorno virtual.
.\venv\Scripts\Activate.ps1

# Arrancar Ollama y descargar embeddings locales.
ollama serve
ollama pull nomic-embed-text

# Ejecutar la practica de introduccion a ChromaDB.
python .\spikes\06-vector_databases_chromadb_cheat_sheet_lab\main.py
```

## Ejecutar Practica 07

```powershell
# Activar el entorno virtual.
.\venv\Scripts\Activate.ps1

# Arrancar Ollama y descargar embeddings locales.
ollama serve
ollama pull nomic-embed-text

# Ejecutar la practica de similitud sobre empleados y libros con ChromaDB.
python .\spikes\07-employee_similarity_search_chromadb_lab\main.py
```

## Ejecutar Practica 08

```powershell
# Activar el entorno virtual.
.\venv\Scripts\Activate.ps1

# Arrancar Ollama y descargar modelos necesarios.
ollama serve
ollama pull nomic-embed-text
ollama pull llama3.2:3b

# Ejecutar la practica de recomendaciones de comida con ChromaDB y RAG.
python .\spikes\08-food_recommendation_systems_chromadb_rag_lab\main.py
```

## Ejecutar Practica 09

```powershell
# Activar el entorno virtual.
.\venv\Scripts\Activate.ps1

# Arrancar Ollama y descargar modelos necesarios.
ollama serve
ollama pull nomic-embed-text
ollama pull qwen2.5:7b

# Ejecutar la practica de context retrieval con LangChain.
python .\spikes\09-langchain_context_retrieval_lab\main.py
```

## Ejecutar Practica 10

```powershell
# Activar el entorno virtual.
.\venv\Scripts\Activate.ps1

# Arrancar Ollama y descargar modelos necesarios.
ollama serve
ollama pull nomic-embed-text
ollama pull qwen2.5:7b

# Ejecutar la practica de retrievers avanzados con LlamaIndex.
python .\spikes\10-advanced_retrievers_llamaindex_lab\main.py
```

## Ejecutar Practica 11

```powershell
# Activar el entorno virtual.
.\venv\Scripts\Activate.ps1

# Arrancar Ollama y descargar embeddings locales.
ollama serve
ollama pull nomic-embed-text

# Ejecutar la practica de semantic similarity con FAISS.
python .\spikes\11-semantic_similarity_faiss_lab\main.py
```

## Ejecutar Practica 12

```powershell
# Activar el entorno virtual.
.\venv\Scripts\Activate.ps1

# Arrancar Ollama y descargar modelos necesarios.
ollama serve
ollama pull nomic-embed-text
ollama pull qwen2.5:7b

# Ejecutar la practica de resumen y QA sobre YouTube con RAG y FAISS.
python .\spikes\12-youtube_summarizer_rag_faiss_lab\main.py
```

## Ejecutar Practica 13

```powershell
# Activar el entorno virtual.
.\venv\Scripts\Activate.ps1

# Arrancar Ollama y descargar un modelo de texto.
ollama serve
ollama pull qwen2.5:7b

# Instalar sintetizador de voz gratuito.
pip install -U edge-tts

# Ejecutar la practica de generacion de historias y texto a voz.
python .\spikes\13-story_generator_text_to_speech_lab\main.py

# Variante adicional con Ollama y gTTS.
python .\spikes\13-story_generator_text_to_speech_lab\ollama_mistral_story_tts\main.py

# Variante real con Mistral API.
python .\spikes\13-story_generator_text_to_speech_lab\mistral_api_story_tts\main.py

# Variante real con Ollama y edge-tts.
python .\spikes\13-story_generator_text_to_speech_lab\ollama_mistral_edge_tts_story_tts\main.py
```

## Ejecutar Practica 14

```powershell
# Activar el entorno virtual.
.\venv\Scripts\Activate.ps1

# Arrancar Ollama y descargar un modelo de vision.
ollama serve
ollama pull qwen2.5vl:3b

# Ejecutar la practica de vision multimodal basica.
python .\spikes\14-basic_vision_multimodal_lab\main.py

# Variante real con llava.
python .\spikes\14-basic_vision_multimodal_lab\llava_vision_querying\main.py

# Variante real con llama3.2-vision.
python .\spikes\14-basic_vision_multimodal_lab\llama3_2_vision_querying\main.py

# Variante real con qwen2.5vl.
python .\spikes\14-basic_vision_multimodal_lab\qwen2_5vl_vision_querying\main.py

# Extension avanzada Style Finder.
python .\spikes\14-basic_vision_multimodal_lab\style_finder_fashion_rag_app\main.py

# Variante Style Finder con llama3.2-vision.
python .\spikes\14-basic_vision_multimodal_lab\style_finder_llama3_2_vision_app\main.py

# Variante Style Finder con llava.
python .\spikes\14-basic_vision_multimodal_lab\style_finder_llava_app\main.py

# Variante Style Finder con qwen2.5vl.
python .\spikes\14-basic_vision_multimodal_lab\style_finder_qwen2_5vl_app\main.py

# Extension avanzada Nutrition Coach.
python .\spikes\14-basic_vision_multimodal_lab\nutrition_coach_flask_app\main.py

# Variante Nutrition Coach con llama3.2-vision.
python .\spikes\14-basic_vision_multimodal_lab\nutrition_coach_llama3_2_vision_app\main.py

# Variante Nutrition Coach con llava.
python .\spikes\14-basic_vision_multimodal_lab\nutrition_coach_llava_app\main.py

# Variante Nutrition Coach con qwen2.5vl.
python .\spikes\14-basic_vision_multimodal_lab\nutrition_coach_qwen2_5vl_app\main.py

# Tras validar compilacion y tests puedes lanzar la interfaz Flask.
python .\spikes\14-basic_vision_multimodal_lab\nutrition_coach_flask_app\app.py
```

## Ejecutar Practica 15

```powershell
# Activar el entorno virtual.
.\venv\Scripts\Activate.ps1

# Arrancar Ollama y descargar un modelo de texto.
ollama serve
ollama pull llama3.2:3b

# Ejecutar la practica del asistente de reuniones.
python .\spikes\15-ai_meeting_assistant_lab\main.py
```

## Ejecutar Practica 16

```powershell
# Activar el entorno virtual.
.\venv\Scripts\Activate.ps1

# Ejecutar la practica de generacion de imagenes con DALL-E.
python .\spikes\16-dalle_image_generation_lab\main.py

# Variante real con DALL-E 2.
python .\spikes\16-dalle_image_generation_lab\dall_e_2_generation\main.py

# Variante real con DALL-E 3.
python .\spikes\16-dalle_image_generation_lab\dall_e_3_generation\main.py
```

## Ejecutar Practica 17

```powershell
# Activar el entorno virtual.
.\venv\Scripts\Activate.ps1

# Instalar dependencias locales de voz y automatizacion.
pip install -U transformers torch sounddevice pyautogui Send2Trash

# Dependencia opcional para el runner de consola legado.
pip install -U keyboard

# Arrancar Ollama.
ollama serve

# Descargar un modelo recomendado para planificacion.
ollama pull qwen2.5:7b

# Ejecutar la practica de asistente de escritorio por voz con ventana nativa.
# La respuesta hablada usa la voz local de Windows si esta disponible.
# La app puede abrir y cerrar aplicaciones permitidas con confirmacion verifica si el proceso sigue vivo antes de reportar un fallo de cierre y resume el ultimo estado en una sola linea.
python .\spikes\17-voice_desktop_assistant_lab\main.py
```

## Ejecutar Practica 18

```powershell
# Activar el entorno virtual.
.\venv\Scripts\Activate.ps1

# Arrancar Ollama.
ollama serve

# Descargar un modelo recomendado para tool calling.
ollama pull qwen2.5:7b

# Ejecutar la practica de tool calling con LangChain.
# El laboratorio usa tools con @tool y ChatOllama como modelo principal.
python .\spikes\18-langchain_tool_calling_math_assistant_lab\main.py
```

## Ejecutar Practica 19

```powershell
# Activar el entorno virtual.
.\venv\Scripts\Activate.ps1

# Instalar dependencias del laboratorio DataWizard.
pip install -U pandas numpy scikit-learn

# Arrancar Ollama.
ollama serve

# Descargar un modelo recomendado para DataWizard.
ollama pull qwen2.5:7b

# Ejecutar la practica de analisis de datos con tool calling local.
# El laboratorio compara un baseline sin tools con un executor agent.
python .\spikes\19-datawizard_ai_powered_data_analysis_lab\main.py
```

## Ejecutar Practica 20

```powershell
# Activar el entorno virtual.
.\venv\Scripts\Activate.ps1

# Arrancar Ollama.
ollama serve

# Descargar un modelo recomendado para tool calling interactivo.
ollama pull qwen2.5:7b

# Alternativa de menor consumo.
ollama pull llama3.2:3b

# Ejecutar la practica de agentes interactivos con tools de LangChain.
# El laboratorio demuestra bind_tools tool_calls ToolMessage y clases de agente.
python .\spikes\20-interactive_llm_agents_with_tools_lab\main.py
```

## Ejecutar Practica 21

```powershell
# Activar el entorno virtual.
.\venv\Scripts\Activate.ps1

# Instalar dependencias del laboratorio YouTube.
pip install -U yt-dlp youtube-transcript-api

# Arrancar Ollama.
ollama serve

# Descargar un modelo recomendado para tool calling sobre YouTube.
ollama pull qwen2.5:7b

# Alternativa de menor consumo.
ollama pull llama3.2:3b

# Ejecutar la practica de agente con tools reales de YouTube.
# El laboratorio demuestra tool calling manual cadena fija y cadena recursiva.
python .\spikes\21-youtube_tool_calling_agent_lab\main.py
```

## Ejecutar Practica 22

```powershell
# Activar el entorno virtual.
.\venv\Scripts\Activate.ps1

# Instalar dependencias del laboratorio de visualizacion.
pip install -U langchain-experimental matplotlib seaborn

# Arrancar Ollama.
ollama serve

# Descargar un modelo recomendado para el DataFrame agent.
ollama pull qwen2.5:7b

# Alternativa de menor consumo.
ollama pull llama3.2:3b

# Ejecutar la practica de visualizacion conversacional con pandas.
# El laboratorio guarda los charts en artifacts y muestra el codigo generado por el agente.
python .\spikes\22-natural_language_data_visualization_agent_lab\main.py
```

## Ejecutar Practica 23

```powershell
# Activar el entorno virtual.
.\venv\Scripts\Activate.ps1

# Instalar la dependencia del toolkit SQL si hace falta.
pip install -U langchain-community

# Arrancar Ollama.
ollama serve

# Descargar un modelo recomendado para el agente SQL.
ollama pull qwen2.5:7b

# Alternativa de menor consumo.
ollama pull llama3.2:3b

# Ejecutar la practica de consultas SQL en lenguaje natural.
# El laboratorio genera una base Chinook local en SQLite y muestra el SQL usado por el agente.
python .\spikes\23-natural_language_sql_agent_lab\main.py
```

## Ejecutar Practica 24

```powershell
# Activar el entorno virtual.
.\venv\Scripts\Activate.ps1

# Instalar LangGraph si aun no esta disponible.
pip install -U langgraph==0.2.57

# Arrancar Ollama.
ollama serve

# Descargar un modelo recomendado para el workflow QA.
ollama pull qwen2.5:7b

# Alternativa de menor consumo.
ollama pull llama3.2:3b

# Ejecutar la practica de workflows con estado y aristas condicionales.
# El laboratorio incluye autenticacion con reintentos QA contextual y un contador ciclico.
python .\spikes\24-langgraph_101_building_stateful_ai_workflows_lab\main.py
```

## Ejecutar Practica 25

```powershell
# Activar el entorno virtual.
.\venv\Scripts\Activate.ps1

# Arrancar Ollama.
ollama serve

# Descargar un modelo recomendado para el agente reflexivo.
ollama pull qwen2.5:7b

# Alternativa de menor consumo.
ollama pull llama3.2:3b

# Dependencia opcional para exportar PNG del grafo.
pip install -U pygraphviz==1.14

# Ejecutar la practica de reflexion con MessageGraph y LinkedIn post generation.
# El laboratorio genera un borrador lo critica y vuelve a generarlo hasta el limite de mensajes.
python .\spikes\25-building_reflection_agent_with_langgraph_lab\main.py
```

## Ejecutar Practica 26

```powershell
# Activar el entorno virtual.
.\venv\Scripts\Activate.ps1

# Arrancar Ollama.
ollama serve

# Descargar un modelo recomendado para el agente reflexivo con evidencia externa.
ollama pull qwen2.5:7b

# Alternativa de menor consumo.
ollama pull llama3.2:3b

# Opcional si quieres usar Tavily en lugar del fallback gratuito de Europe PMC.
pip install -U tavily-python
$env:TAVILY_API_KEY = "tu_api_key"

# Ejecutar la practica de reflexion con herramientas externas y revision guiada por evidencia.
# El laboratorio puede usar Tavily o hacer fallback a Europe PMC si no hay API key.
python .\spikes\26-building_reflection_agent_with_external_knowledge_integration\main.py
```

## Ejecutar Practica 27

```powershell
# Activar el entorno virtual.
.\venv\Scripts\Activate.ps1

# Arrancar Ollama.
ollama serve

# Descargar un modelo recomendado para el agente ReAct.
ollama pull qwen2.5:7b

# Alternativa de menor consumo.
ollama pull llama3.2:3b

# Opcional si quieres usar Tavily para la busqueda general.
pip install -U tavily-python
$env:TAVILY_API_KEY = "tu_api_key"

# Ejecutar la practica de ReAct con herramientas y LangGraph.
# El laboratorio incluye busqueda clima ropa calculadora y resumen de noticias.
python .\spikes\27-react_build_reasoning_and_acting_ai_agents_with_langgraph\main.py
```

## Parar Gradio

```powershell
# Si Gradio corre en primer plano.
Ctrl+C

# Si Gradio sigue usando el puerto 7860.
$pid = (Get-NetTCPConnection -LocalPort 7860 -State Listen).OwningProcess
Stop-Process -Id $pid
```

## Comandos utiles despues de instalar

```bash
# Instalar el proyecto en modo editable.
pip install -e .

# Ejecutar API en desarrollo.
PYTHONPATH=src uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Guardar lock simple de dependencias.
pip freeze > requirements.txt
```

## VS Code

```text
Task: Codex: Generate Commit Message
Uso: Genera un commit message con Codex usando solo cambios staged.
Salida: Imprime el mensaje en la terminal y lo copia al portapapeles cuando es posible.
```

## Rutas de API

| Metodo | Ruta | Descripcion |
| --- | --- | --- |
| GET | `/api/v1/agent/` | Endpoint de prueba del modulo de agentes. |
| GET | `/api/v1/chat/` | Endpoint de prueba del modulo de chat. |
| GET | `/api/v1/health/` | Health check de la API versionada v1. |
| GET | `/api/v1/llm/` | Endpoint de prueba del modulo LLM. |
| GET | `/api/v1/prompt/` | Health check del servicio de prompts. |
| POST | `/api/v1/prompt/exercise-1/completion` | Ejecuta el ejercicio 1 de prompts. |
| POST | `/api/v1/prompt/exercise-2/task-prompts` | Ejecuta el ejercicio 2 de prompts. |
| POST | `/api/v1/prompt/exercise-3/step-by-step` | Ejecuta el ejercicio 3 de prompts. |
| POST | `/api/v1/prompt/exercise-4/lcel` | Ejecuta el ejercicio 4 de prompts. |
| POST | `/api/v1/prompt/exercise-5/reasoning-reviews` | Ejecuta el ejercicio 5 de prompts. |
| GET | `/api/v1/rag/` | Endpoint de prueba del modulo de retrieval RAG. |
| GET | `/health` | Health check general de la aplicacion. |

## Archivos comentados

```text
src/
  app/
    api/
      v1/
        endpoints/
          prompts.py
        router.py
    infra/
      llm/
        ollama_client.py
        openai_client.py
    main.py
    modules/
      components/
        agents/
          prompts/
            templates.py
      features/
        chatbot/
          schemas.py
          service.py
spikes/
  01-prompting_lcel_lab/
    README.md
    main.py
    config/
      prompting_runtime_config.py
    models/
      prompting_model_gateway.py
    orchestration/
      prompting_orchestration_basic.py
      prompting_orchestration_lcel.py
      prompting_orchestration_reasoning.py
  02-gradio_llama_lab/
    README.md
    main.py
    config/
      gradio_llama_runtime_config.py
    models/
      gradio_llama_model_gateway.py
    orchestration/
      gradio_llama_orchestration_steps.py
    state/
      gradio_llama_runtime_state.py
    ui/
      gradio_llama_ui_builder.py
  03-rag_pdf_qa_bot_lab/
    README.md
    main.py
    bootstrap/
      rag_bootstrap.py
    config/
      rag_config.py
    models/
      rag_models.py
    orchestration/
      rag_orchestration_qa.py
      rag_orchestration_retrieval.py
    pipeline/
      rag_document_pipeline.py
    state/
      rag_state.py
    ui/
      rag_ui.py
  04-linkedin_icebreaker_bot_lab/
    README.md
    main.py
    config/
      icebreaker_config.py
    data/
      ana_martinez.json
      diego_santos.json
    models/
      icebreaker_models.py
    orchestration/
      icebreaker_orchestration_profile.py
      icebreaker_orchestration_qa.py
      icebreaker_orchestration_retrieval.py
    pipeline/
      icebreaker_profile_pipeline.py
    state/
      icebreaker_state.py
    ui/
      icebreaker_ui.py
  05-similarity_search_by_hand_lab/
    README.md
    main.py
    config/
      similarity_runtime_config.py
    data/
      similarity_documents.py
    models/
      similarity_embedding_gateway.py
    orchestration/
      similarity_lab_runner.py
      similarity_metrics_orchestration.py
      similarity_search_orchestration.py
    state/
      similarity_runtime_state.py
  06-vector_databases_chromadb_cheat_sheet_lab/
    README.md
    main.py
    config/
      chromadb_cheat_sheet_config.py
    data/
      chromadb_demo_dataset.py
    models/
      chromadb_keyword_embedding_gateway.py
    orchestration/
      chromadb_cheat_sheet_runner.py
      chromadb_collection_orchestration.py
      chromadb_query_orchestration.py
    state/
      chromadb_runtime_state.py
  07-employee_similarity_search_chromadb_lab/
    README.md
    main.py
    config/
      employee_similarity_config.py
    data/
      book_records.py
      employee_records.py
    models/
      employee_book_embedding_gateway.py
    orchestration/
      book_collection_orchestration.py
      book_search_orchestration.py
      employee_collection_orchestration.py
      employee_search_orchestration.py
      employee_similarity_lab_runner.py
    state/
      employee_similarity_state.py
  08-food_recommendation_systems_chromadb_rag_lab/
    README.md
    main.py
    config/
      food_recommendation_config.py
    data/
      food_dataset.json
    models/
      food_embedding_gateway.py
      food_ollama_gateway.py
    orchestration/
      food_collection_orchestration.py
      food_rag_orchestration.py
      food_recommendation_lab_runner.py
      food_search_orchestration.py
    pipeline/
      food_data_pipeline.py
    state/
      food_recommendation_state.py
  09-langchain_context_retrieval_lab/
    README.md
    main.py
    config/
      context_retrieval_config.py
    data/
      company_policies.txt
      context_retrieval_movie_dataset.py
      langchain_retrieval_notes.txt
    models/
      context_retrieval_demo_llm.py
      context_retrieval_ollama_gateway.py
      context_retrieval_embedding_gateway.py
    orchestration/
      context_retrieval_collection_orchestration.py
      context_retrieval_lab_runner.py
      context_retrieval_parent_orchestration.py
      context_retrieval_search_orchestration.py
      context_retrieval_self_query_orchestration.py
  10-advanced_retrievers_llamaindex_lab/
    README.md
    main.py
    config/
      advanced_retrievers_config.py
    data/
      advanced_retrievers_documents.py
    models/
      advanced_retrievers_ollama_gateway.py
      advanced_retrievers_demo_llm.py
      llamaindex_demo_embedding_gateway.py
    orchestration/
      advanced_retrievers_context_orchestration.py
      advanced_retrievers_core_orchestration.py
      advanced_retrievers_fusion_orchestration.py
      advanced_retrievers_index_orchestration.py
      advanced_retrievers_lab_runner.py
  11-semantic_similarity_faiss_lab/
    README.md
    main.py
    config/
      faiss_similarity_config.py
    data/
      faiss_forum_posts.py
    models/
      faiss_semantic_embedding_gateway.py
    orchestration/
      faiss_index_orchestration.py
      faiss_preprocessing_orchestration.py
      faiss_search_orchestration.py
      faiss_similarity_lab_runner.py
  12-youtube_summarizer_rag_faiss_lab/
    README.md
    main.py
    config/
      youtube_rag_config.py
    data/
      youtube_transcript_catalog.py
    models/
      youtube_rag_demo_llm.py
      youtube_rag_ollama_gateway.py
      youtube_rag_embedding_gateway.py
    orchestration/
      youtube_rag_lab_runner.py
      youtube_rag_orchestration.py
      youtube_transcript_orchestration.py
  13-story_generator_text_to_speech_lab/
    README.md
    main.py
    config/
      story_real_provider_config.py
      story_tts_config.py
    mistral_api_story_tts/
      README.md
      main.py
    models/
      story_audio_gateway.py
      story_demo_model.py
      story_edge_tts_gateway.py
      story_mistral_api_gateway.py
      story_ollama_mistral_gateway.py
    ollama_mistral_edge_tts_story_tts/
      README.md
      main.py
    ollama_mistral_story_tts/
      README.md
      main.py
    orchestration/
      story_audio_orchestration.py
      story_generation_orchestration.py
      story_real_variants_orchestration.py
      story_tts_lab_runner.py
  14-basic_vision_multimodal_lab/
    README.md
    main.py
    assets/
      city_scene_real.png
      nutrition_label_real.png
    config/
      nutrition_coach_config.py
      style_finder_fashion_config.py
      vision_real_provider_config.py
      vision_multimodal_config.py
    data/
      nutrition_coach_dataset.py
      style_finder_fashion_dataset.py
      vision_sample_dataset.py
    llama3_2_vision_querying/
      README.md
      main.py
    llava_vision_querying/
      README.md
      main.py
    nutrition_coach_flask_app/
      README.md
      app.py
      main.py
      static/
        style.css
      templates/
        index.html
    nutrition_coach_llama3_2_vision_app/
      README.md
      main.py
    nutrition_coach_llava_app/
      README.md
      main.py
    nutrition_coach_qwen2_5vl_app/
      README.md
      main.py
    models/
      nutrition_coach_image_processor.py
      nutrition_coach_llm_service.py
      style_finder_image_processor.py
      style_finder_llm_service.py
      vision_demo_model.py
      vision_ollama_gateway.py
    orchestration/
      nutrition_coach_app_orchestration.py
      nutrition_coach_asset_orchestration.py
      nutrition_coach_dataset_orchestration.py
      nutrition_coach_helpers.py
      nutrition_coach_lab_runner.py
      style_finder_app_orchestration.py
      style_finder_asset_orchestration.py
      style_finder_dataset_orchestration.py
      style_finder_helpers.py
      style_finder_lab_runner.py
      vision_image_orchestration.py
      vision_lab_runner.py
      vision_query_orchestration.py
      vision_real_variants_orchestration.py
      vision_similarity_orchestration.py
    qwen2_5vl_vision_querying/
      README.md
      main.py
    style_finder_fashion_rag_app/
      README.md
      main.py
    style_finder_llama3_2_vision_app/
      README.md
      main.py
    style_finder_llava_app/
      README.md
      main.py
    style_finder_qwen2_5vl_app/
      README.md
      main.py
    ui/
      style_finder_ui.py
  15-ai_meeting_assistant_lab/
    README.md
    main.py
    config/
      meeting_assistant_config.py
    data/
      meeting_transcript_catalog.py
    models/
      meeting_assistant_demo_llm.py
      meeting_assistant_llm_gateway.py
    orchestration/
      meeting_assistant_lab_runner.py
      meeting_assistant_orchestration.py
      meeting_cleanup_orchestration.py
      meeting_minutes_orchestration.py
      meeting_transcription_orchestration.py
    ui/
      meeting_assistant_ui.py
  16-dalle_image_generation_lab/
    README.md
    main.py
    config/
      dalle_image_generation_config.py
    dall_e_2_generation/
      README.md
      main.py
    dall_e_3_generation/
      README.md
      main.py
    data/
      dalle_prompt_catalog.py
    models/
      dalle_openai_gateway.py
    orchestration/
      dalle_generation_orchestration.py
      dalle_lab_runner.py
  17-voice_desktop_assistant_lab/
    README.md
    main.py
    config/
      voice_desktop_config.py
    data/
      voice_command_catalog.py
    models/
      voice_agent_demo_planner.py
      voice_agent_ollama_gateway.py
      voice_desktop_entities.py
      voice_local_tts_gateway.py
      voice_microphone_gateway.py
      voice_transcription_gateway.py
    orchestration/
      voice_desktop_execution_orchestration.py
      voice_desktop_lab_runner.py
      voice_desktop_planning_orchestration.py
      voice_desktop_session_orchestration.py
    ui/
      voice_desktop_ui.py
  18-langchain_tool_calling_math_assistant_lab/
    README.md
    main.py
    config/
      tool_calling_math_config.py
    data/
      tool_calling_fact_catalog.py
    models/
      tool_calling_ollama_gateway.py
      tool_calling_demo_chat_model.py
      tool_calling_math_entities.py
    orchestration/
      tool_calling_agent_orchestration.py
      tool_calling_lab_runner.py
      tool_calling_tools_orchestration.py
  19-datawizard_ai_powered_data_analysis_lab/
    README.md
    main.py
    config/
      datawizard_config.py
    data/
      classification-dataset.csv
      regression-dataset.csv
    models/
      datawizard_baseline_chat.py
      datawizard_demo_chat_model.py
      datawizard_ollama_gateway.py
      datawizard_entities.py
    orchestration/
      datawizard_agent_orchestration.py
      datawizard_lab_runner.py
      datawizard_tools_orchestration.py
```

## Glosario de Terminos

| Termino | Descripcion |
| --- | --- |
| ACP | Agent Communication Protocol para intercambio estructurado de mensajes entre agentes autonomos. |
| Agentic AI | Enfoque donde varios agentes especializados colaboran con memoria coordinacion y reparto dinamico de tareas para alcanzar un objetivo mayor. |
| Agentes de IA | Sistemas basados en inteligencia artificial que planifican acciones y ejecutan tareas con cierto grado de autonomia. |
| ANN | Busqueda aproximada de vecinos mas cercanos para escalar retrieval vectorial con baja latencia. |
| Advanced Retriever | Recuperador con estrategias mas sofisticadas que un top k simple como fusion filtros o reranking. |
| BM25 | Algoritmo de ranking lexico que mejora TF IDF con saturacion de frecuencia y normalizacion por longitud de documento. |
| b64_json | Formato de respuesta donde una imagen generada via API se devuelve como Base64 embebido en JSON en lugar de una URL temporal. |
| Chain-of-Thought | Tecnica de prompting que fuerza un razonamiento intermedio paso a paso para mejorar respuestas complejas. |
| Chaining | Flujo secuencial Retrieval -> Extraction -> Processing -> Generation para transformar contexto en una salida util. |
| ChromaDB | Base de datos vectorial orientada a embeddings usada para almacenar y recuperar contexto por similitud semantica. |
| Chunk | Trozo de texto dividido de un archivo. |
| Chunking Strategy | Criterio para dividir documentos en fragmentos antes del indexado y la recuperacion. |
| Computer Vision | Disciplina de IA que permite interpretar imagenes y video para detectar objetos escenas texto y relaciones visuales. |
| Cross-Modal Alignment | Alineacion entre modalidades para que texto imagen audio o video representen el mismo significado dentro del sistema. |
| Cross-Modal Understanding | Capacidad de relacionar informacion entre modalidades para responder o generar contenido con contexto compartido. |
| DALL-E | Modelo generativo orientado a crear imagenes a partir de instrucciones en lenguaje natural. |
| DALL-E Edits | Capacidad de editar una imagen existente con una mascara y un prompt para reemplazar regiones concretas. |
| DALL-E Variations | Capacidad de generar variantes visuales de una imagen base manteniendo rasgos de estilo o composicion. |
| Deepfake | Contenido sintetico de imagen audio o video que imita personas o eventos con alto realismo. |
| Diffusion Model | Familia de modelos generativos que crea contenido refinando ruido paso a paso hasta obtener una salida coherente. |
| Durable Execution | Capacidad de un workflow para pausar reanudar o recuperarse de fallos sin perder el estado compartido. |
| Edge Computing | Ejecucion de modelos cerca de la fuente de datos para reducir latencia dependencia de red y coste de transferencia. |
| edge-tts | Proveedor de sintesis de voz accesible desde Python que permite generar audio de forma gratuita mediante internet. |
| Embeddings | Vectores numericos que representan el significado semantico de palabras frases o documentos. |
| Explainable AI | Enfoque para hacer mas comprensibles las decisiones y salidas producidas por sistemas de IA. |
| FAISS | Libreria de Meta para busqueda vectorial de alto rendimiento en una sola maquina con CPU o GPU. Ofrece control fino del indice con opciones como Flat IVF LSH y HNSW pero no incluye metadatos ni escalado distribuido de forma nativa. |
| Fine-tuning | Ajuste adicional de un modelo preentrenado con datos de dominio para mejorar su rendimiento en tareas especificas. |
| Flask | Framework web ligero de Python usado para exponer aplicaciones y APIs de IA. |
| Grounding | Uso de contexto recuperado para anclar la respuesta del modelo a evidencia concreta. |
| Hallucination Mitigation | Estrategias para reducir respuestas inventadas o inexactas en modelos de lenguaje. |
| HNSW | Indice ANN basado en grafos jerarquicos de tipo small world. Usa capas superiores dispersas para hacer saltos largos y capas inferiores densas para refinar la busqueda con alta velocidad y buena precision sobre colecciones grandes. |
| Hugging Face | Ecosistema de modelos datasets y librerias para entrenamiento inferencia y despliegue de sistemas de IA. |
| Human-in-the-Loop | Patron donde una persona revisa aprueba o corrige pasos concretos del workflow antes de continuar. |
| IA Multimodal | Capacidad de un sistema para comprender combinar o generar informacion en texto imagen audio y video. |
| Image Captioning | Tarea de vision y lenguaje que genera descripciones textuales a partir de imagenes. |
| Image Validation and Encoding | Paso previo que verifica formato tamano y consistencia de una imagen y la convierte a una representacion apta para el modelo como Base64. |
| Image-to-Video | Generacion o animacion de video a partir de una imagen fija mediante prediccion de movimiento y consistencia temporal. |
| Inpainting | Tecnica de edicion generativa donde se rellenan o sustituyen regiones de una imagen segun una mascara y un prompt. |
| Input Processing | Etapa donde se preparan entradas como texto imagen audio o video antes de invocar el modelo. |
| LangChain | Framework de codigo abierto para crear aplicaciones con LLMs y componentes como prompts cadenas agentes y herramientas. |
| LangGraph | Framework orientado a workflows agenticos con estado nodos aristas memoria compartida y control de flujo explicito. |
| LCEL | Lenguaje declarativo de LangChain para componer cadenas de ejecucion centradas en LLM de forma modular. |
| Lematizacion | Proceso de reducir palabras a su forma canonica para normalizar texto y mejorar analisis. |
| Llama 4 | Familia de modelos multimodales de Meta orientada a razonamiento y generacion sobre varias modalidades. |
| LLaVA | Familia de modelos de vision y lenguaje orientada a consultas sobre imagenes mediante instrucciones en texto. |
| LlamaIndex | Framework para construir aplicaciones con LLMs orientadas a documentos indices y retrieval en flujos RAG. |
| LLM | Modelo de lenguaje de gran escala entrenado para comprender y generar texto. |
| LSH | Tecnica de hashing sensible a la localidad usada para aproximar similitud en espacios de alta dimension. |
| MessageGraph | Tipo de grafo de LangGraph centrado en un historial de mensajes que se va ampliando durante la ejecucion. |
| Milvus | Base de datos vectorial orientada a escalado y despliegues de produccion sobre grandes colecciones. |
| MM-RAG | Variante multimodal de RAG que recupera y combina contexto desde texto imagen audio o video antes de generar una respuesta. |
| Mistral | Familia de modelos de lenguaje y proveedor de inferencia usados para generacion de texto y tareas instruct. |
| Model Context Protocol | Protocolo abierto para conectar modelos con herramientas y fuentes de contexto mediante interfaces estructuradas. |
| Multi-Agent System | Arquitectura donde varios agentes cooperan para resolver objetivos comunes. |
| Multimodal Fusion | Integracion de varias modalidades dentro del modelo o pipeline para producir una interpretacion o salida unificada. |
| Multimodal Message | Estructura de solicitud que combina texto e imagen en un mismo payload para modelos de vision y lenguaje. |
| NLG | Generacion de lenguaje natural a partir de datos o representaciones internas. |
| NLP | Procesamiento de lenguaje natural para analizar y transformar texto humano en estructuras utiles. |
| NLU | Comprension del lenguaje natural para extraer intencion entidades y contexto semantico. |
| Orchestration | Coordinacion del flujo entre agentes herramientas y pasos de ejecucion. |
| OpenAI | Proveedor de modelos y APIs usado en este repositorio para practicas especificas como generacion de imagenes. |
| Point | 1 point = 1 chunk como objeto guardado en la vector DB. |
| Prompting | Diseno de instrucciones y contexto para guiar la salida de un modelo. |
| Prompt Engineering Visual | Diseno de prompts para imagen o video especificando sujeto estilo composicion iluminacion movimiento y contexto. |
| Prompting Templates | Plantillas reutilizables para estructurar prompts de forma consistente. |
| Query Fusion | Estrategia que combina resultados de varias consultas o recuperadores para mejorar cobertura y relevancia. |
| Qwen2.5VL | Modelo multimodal de vision y lenguaje de la familia Qwen orientado a descripcion visual y OCR ligero. |
| RAG | Enfoque que combina recuperacion de informacion y generacion para producir respuestas mas precisas y trazables. |
| ReAct | Patron donde el modelo alterna razonamiento y uso de herramientas dentro de un mismo ciclo de decision. |
| Reflection Agent | Agente que genera una respuesta y despues la critica para mejorar claridad cobertura o calidad sin buscar datos externos. |
| Reflexion Agent | Variante de auto mejora que combina critica interna con herramientas o busqueda externa para revisar la respuesta con evidencia. |
| Reranking | Reordenacion posterior de resultados recuperados para mejorar la relevancia final. |
| Retriever | Componente encargado de recuperar contexto relevante desde una base de conocimiento indexada. |
| Retrieval | Proceso de recuperar contexto relevante desde una base de conocimiento antes de generar una respuesta. |
| Self-Supervised Learning | Aprendizaje que usa patrones internos de los datos para entrenar modelos sin depender por completo de etiquetas manuales. |
| Semantic Search | Busqueda que compara significado y contexto en lugar de depender solo de coincidencias exactas de palabras. |
| StateGraph | Estructura principal de LangGraph donde el estado compartido fluye entre nodos conectados por aristas normales o condicionales. |
| Storyboard | Secuencia visual planificada de escenas o tomas usada para dirigir la generacion o edicion de video. |
| Speech Recognition | Reconocimiento automatico del habla para convertir audio en texto o en unidades linguisticamente utiles. |
| Speech Processing | Conjunto de tecnicas para reconocer entender analizar o generar voz humana en sistemas de IA. |
| Speech to Text | Conversion automatica de audio o voz a texto para transcripcion y analisis. |
| TF-IDF | Representacion clasica de texto basada en frecuencia de termino y frecuencia inversa de documento. |
| Temporal Consistency | Propiedad de video y audio generados o analizados donde la transicion entre pasos mantiene coherencia visual o sonora. |
| Text Processing | Tecnicas para limpiar clasificar resumir extraer y generar informacion a partir de texto. |
| Text to Image | Generacion de imagenes a partir de una descripcion textual. |
| Text to Speech | Sintesis de voz a partir de texto escrito. |
| Text to Video | Generacion de video a partir de instrucciones textuales o guiones. |
| Tokenizacion | Segmentacion del texto en unidades llamadas tokens para su procesamiento por modelos. |
| Transcription | Proceso de transformar una fuente de audio o voz en texto legible y reutilizable. |
| Transparency | Capacidad de documentar fuentes decisiones limites y comportamiento de un sistema para hacerlo auditable y confiable. |
| VAE | Autoencoder variacional usado para aprender representaciones latentes y generar muestras nuevas de forma controlada. |
| Vector Database | Base de datos optimizada para almacenar y consultar vectores por similitud semantica. |
| Vector Store Retriever | Recuperador que usa una base vectorial para localizar fragmentos cercanos a una consulta embebida. |
| Vision-Language Model | Modelo multimodal capaz de procesar conjuntamente imagenes y texto para describir analizar o responder preguntas sobre contenido visual. |
| Visual Encoder | Componente que transforma una imagen en representaciones numericas que luego se alinean con el lenguaje. |
| Visual Generation Workflow | Flujo que pasa de prompt a generacion de imagen y despues a visualizacion guardado o postproceso del resultado. |
| Visual Question Answering | Tarea multimodal donde un modelo responde preguntas en lenguaje natural sobre el contenido de una imagen. |
| Visual Search | Busqueda basada en similitud visual o en contenido de imagenes para localizar elementos relacionados. |
| Whisper | Modelo de reconocimiento automatico de voz usado para transcripcion y traduccion de audio. |
| Zero-Shot Learning | Capacidad de resolver tareas o reconocer conceptos no vistos explicitamente durante el ajuste de un modelo. |

## Tipos de Sistemas de IA

| Termino | Descripcion |
| --- | --- |
| Agentic AI | Coordina varios agentes especializados para resolver objetivos complejos con memoria y orquestacion. |
| Agentes de IA | Integran LLMs con planificacion herramientas y memoria para ejecutar acciones autonomas. |
| IA Generativa | Predice la siguiente secuencia probable y genera texto imagen audio o video segun el modelo. |
| IA Generativa Multimodal | Procesa y genera varios tipos de datos en una misma interaccion. |
| MM-RAG | Combina retrieval y generacion sobre varias modalidades para fundamentar respuestas con contexto mixto. |
| RAG | Combina recuperacion de informacion y generacion para fundamentar respuestas con contexto externo. |

## IA Generativa vs IA Agentica

`IA Generativa` se centra en producir una salida como texto imagen audio o video a partir de una instruccion. Normalmente responde en uno o pocos pasos y su exito depende sobre todo de la calidad del prompt del contexto recuperado y del modelo elegido.

`IA Agentica` va un paso mas alla. No solo genera contenido sino que persigue un objetivo usando planificacion memoria herramientas iteracion y toma de decisiones sobre el siguiente paso. Puede dividir una tarea grande en subtareas revisar resultados pedir mas contexto y coordinar uno o varios agentes especializados.

| Aspecto | IA Generativa | IA Agentica |
| --- | --- | --- |
| Objetivo principal | Generar una salida util a partir de una instruccion. | Alcanzar un objetivo mediante decisiones y acciones encadenadas. |
| Autonomia | Baja o media segun el flujo. | Media o alta con supervision y limites claros. |
| Memoria | Suele depender del contexto inmediato o de un historial simple. | Puede usar memoria compartida persistente y estado entre pasos. |
| Herramientas | Puede vivir sin tools en casos simples. | Suele apoyarse en tools APIs retrieval y validaciones externas. |
| Flujo | Normalmente lineal o de una sola vuelta. | Iterativo con ramas reintentos y posibles pausas humanas. |
| Ejemplos tipicos | Resumir traducir redactar clasificar generar imagenes. | Resolver tareas multi paso investigar enrutar consultas orquestar `RAG` y coordinar agentes. |

## Flujos Multimodales

La IA multimodal combina varias modalidades dentro del mismo flujo de aplicacion. En la practica esto aparece en tareas como `Speech to Text` `Text to Speech` `Image Captioning` `Text to Image` `Text to Video` y `MM-RAG`. Frameworks como `Flask` `Gradio` `LangChain` y `Hugging Face` ayudan a prototipar interfaces orquestar pipelines y conectar modelos especializados de voz imagen y video.

## Capacidades y Retos de IA Multimodal

Entre las capacidades mas importantes de la IA multimodal estan `Computer Vision` para interpretar imagenes y video `Text Processing` para comprender lenguaje `Speech Processing` para trabajar con voz `Visual Question Answering` para responder sobre contenido visual e integraciones como `Text to Video` e `Image-to-Video`. En paralelo los retos mas relevantes siguen siendo `Cross-Modal Alignment` `Multimodal Fusion` `Hallucination Mitigation` sesgo privacidad coste computacional y `Transparency` para explicar como decide el sistema.

## Integracion Visual y de Video

En vision multimodal suele repetirse un patron comun. Primero ocurre `Input Processing` donde se prepara el prompt y se valida la imagen. Despues llega `Image Validation and Encoding` para convertir el archivo a una forma transportable como `Base64` o un `Multimodal Message`. Por ultimo un `Vision-Language Model` combina la salida del `Visual Encoder` con el contexto textual para tareas como `Image Captioning` `Visual Question Answering` u OCR ligero.

En generacion visual tambien conviene separar capacidades por proveedor y modelo. `DALL-E 2` destaca por `DALL-E Edits` `DALL-E Variations` multiples imagenes por request y formatos de salida como `b64_json`. `DALL-E 3` se orienta mas a calidad y composicion con menos opciones operativas. En video el vocabulario cambia hacia `Prompt Engineering Visual` `Storyboard` consistencia temporal y operaciones de iteracion sobre escenas.

Dentro de este repositorio la hoja de trucos de integracion visual y de video queda absorbida por dos practicas ya existentes. La practica `14` cubre mensajes multimodales codificacion de imagen `Image Captioning` `Visual Question Answering` object detection por pregunta y analisis visual. La practica `16` cubre generacion con `DALL-E` exportacion local `b64_json` y comparacion entre `dall-e-2` y `dall-e-3` sin necesidad de un spike adicional.

Tras la extension de ambas practicas la `14` tambien cubre captioning en lote sobre varias imagenes y la `16` ya incluye requests configurables para tamano calidad y generacion multiple con `dall-e-2`. Con esto la hoja de trucos queda representada de forma ejecutable sin duplicar contenido en un laboratorio nuevo.

## IA Generativa para Tareas Especificas

| Termino | Descripcion |
| --- | --- |
| Image Captioning | Generacion de subtitulos o descripciones textuales a partir de imagenes. |
| Image-to-Video | Animacion o generacion de video a partir de una imagen de entrada. |
| Language Translation | Traduccion automatica de contenido entre idiomas. |
| Sentiment Analysis | Clasificacion de la emocion o postura expresada en un texto. |
| Speech to Text | Transcripcion automatica de audio o voz a texto utilizable por otros sistemas. |
| Spam Detection | Identificacion de mensajes no deseados o maliciosos. |
| Text to Image | Generacion de imagenes a partir de instrucciones en lenguaje natural. |
| Text to Speech | Generacion de voz sintetica a partir de texto. |
| Text to Video | Generacion de video a partir de un prompt o una descripcion textual. |
| Visual Question Answering | Respuesta a preguntas sobre una imagen o escena usando lenguaje natural. |
| Visual Search | Recuperacion de elementos visualmente similares o semanticamente relacionados a partir de una imagen. |
| Virtual Assistant Chatbot | Asistente conversacional que simula dialogo humano para soporte y automatizacion. |

## Componentes de LangChain

| Termino | Descripcion |
| --- | --- |
| Agents | Entidades que deciden acciones y coordinan herramientas para resolver tareas. |
| Chains | Secuencias de pasos que conectan componentes de LangChain para ejecutar un flujo. |
| Chat Message | Estructura de mensaje usada para conservar contexto en conversaciones. |
| Chat Models | Modelos optimizados para interacciones conversacionales. |
| Documents | Unidades estructuradas de texto o datos listas para procesamiento. |
| Language Model | Modelo que genera o transforma texto segun una entrada. |
| Output Parsers | Componentes que transforman la salida del modelo en formatos estructurados. |
| Prompt Templates | Plantillas predefinidas para construir prompts de forma reutilizable y consistente. |

## Mapa de Herramientas de LangChain en el Repositorio

Esta guia no intenta cubrir todo el catalogo de `LangChain`. Sirve para conectar los tipos de herramientas integradas con las practicas ya presentes en el repo y para detectar huecos naturales de expansion. La disponibilidad la autenticacion y el coste de cada integracion pueden cambiar segun proveedor asi que conviene revisar siempre la documentacion oficial antes de adoptarla.

| Area | Herramientas o toolkits | Estado en el repo | Uso sugerido |
| --- | --- | --- | --- |
| Retrieval documental | `Document Loaders` `VectorStoreQA` `SelfQueryRetriever` `ParentDocumentRetriever` | Cubierto. | Practicas `03` `09` y `12`. |
| Busqueda vectorial | `Chroma` `FAISS` `BM25` `Query Fusion` | Cubierto. | Practicas `06` `07` `08` `10` y `11`. |
| Busqueda externa | `Wikipedia` `Tavily Search` `ArXiv` | Parcial. | Extension natural de `09` o `12`. |
| Analisis y calculo | `Python REPL` `Pandas DataFrame` `LLMMathChain` | Cubierto. | Practicas `18` `19` y `22`. |
| Datos estructurados | `SQL Database Toolkit` `JSON Toolkit` | Cubierto en SQL y parcial en JSON. | Practica `23` para SQL y buen candidato futuro para JSON. |
| Web y APIs | `Requests Toolkit` `Playwright Browser` | No cubierto todavia. | Buen candidato para agentes con navegacion y automatizacion web. |
| Productividad | `GitHub Toolkit` `Slack Toolkit` `Gmail Toolkit` | No cubierto todavia. | Interesante para workflows agenticos orientados a negocio. |

## Cuando Usar LLMs Flujos o Agentes

No toda tarea con IA necesita un agente. Para tareas basicas y bien definidas suele bastar con un `LLM` y un prompt claro. Cuando el proceso es predecible y conviene controlar coste latencia y trazabilidad suele resultar mejor un workflow fijo. Los agentes quedan reservados para escenarios con mas ambiguedad donde hace falta decidir pasos usar herramientas distintas o adaptarse sobre la marcha.

Una forma practica de decidirlo es revisar cuatro factores: ambiguedad de la tarea flexibilidad de los pasos variedad de herramientas necesarias e impacto del fallo. Si la tarea es simple repetible o de alto riesgo operativo conviene evitar agentes y preferir pipelines deterministas con validaciones explicitas.

Los agentes actuales todavia presentan limites de fiabilidad coste y supervision. Por eso deben desplegarse con limites claros registros observabilidad control de resultados y un humano en el bucle cuando el impacto del error sea relevante.

## Tool Calling y Arquitectura de Agentes

El `tool calling` amplia a los `LLM` al conectarlos con datos y acciones externas en tiempo real. En lugar de depender solo del conocimiento del modelo permite consultar APIs bases de datos buscadores sistemas corporativos y utilidades multimodales para trabajar con texto imagen audio o video. Aunque el nombre sugiere ejecucion directa el modelo no ejecuta la herramienta por si solo. Lo que hace es proponer una llamada estructurada con el nombre de la herramienta y sus argumentos para que la aplicacion decida si la ejecuta o no.

Cuando las herramientas se integran desde un framework como `LangChain` se reduce fragilidad frente a implementaciones ad hoc en cliente y mejora la trazabilidad del flujo. Esto ayuda a bajar alucinaciones porque el modelo deja de inventar ciertos datos y pasa a recuperarlos desde fuentes externas o a ejecutar acciones acotadas mediante interfaces definidas. Tambien encaja bien con patrones `RAG` cuando el agente necesita apoyarse en bases de conocimiento propias o especializadas. En `LangChain` la jerarquia base parte de `BaseTool` y para herramientas basadas en funciones suele ser preferible usar `@tool` o `StructuredTool` antes que enfoques mas antiguos o menos estructurados.

Una arquitectura de agente eficaz suele separar memoria uso de herramientas planificacion y razonamiento en componentes modulares. Ese enfoque facilita auditar decisiones controlar riesgos y sustituir piezas concretas sin redisenar todo el sistema. Patrones como `Zero-Shot ReAct` pueden servir como punto de partida cuando el problema esta acotado y el agente solo necesita razonamiento sencillo con seleccion de herramientas.

## Ciclo de Tool Calling

En un flujo normal de `tool calling` la aplicacion registra primero las herramientas disponibles junto con su esquema de entrada. Despues el modelo recibe la consulta del usuario y decide si necesita llamar una herramienta. Si la necesita devuelve una solicitud estructurada con nombre y argumentos. La aplicacion valida esa solicitud ejecuta la herramienta si procede y devuelve el resultado al modelo para que redacte la respuesta final con ese dato ya incorporado al contexto.

## Manual Tool Calling y Control de Ejecucion

En `tool calling` el modelo no ejecuta herramientas por si solo. El modelo devuelve una propuesta de llamada con nombre y argumentos y la aplicacion decide si esa llamada se ejecuta o no. Este enfoque permite aplicar validaciones reglas de negocio listas de herramientas permitidas y control de errores antes de tocar sistemas externos.

El ciclo habitual es simple: el modelo devuelve un `AIMessage` con `tool_calls` la aplicacion ejecuta la herramienta valida el resultado y responde con un `ToolMessage` asociado al mismo `tool_call_id`. Solo despues el modelo genera la respuesta final usando ese resultado como contexto. Este patron es especialmente util cuando importan seguridad auditabilidad y control de costes.

## Structured Outputs

Cuando una salida va a terminar en una base de datos una API o un flujo automatizado conviene pedir una respuesta estructurada en lugar de texto libre. En `LangChain` esto puede resolverse con esquemas `Pydantic` `TypedDict` `dataclasses` o `JSON Schema` para asegurar consistencia y validacion.

En la API moderna `LangChain` puede usar salida estructurada nativa del proveedor cuando el modelo la soporta o caer a una estrategia basada en `tool calling` cuando no existe soporte nativo. Esto reduce parsing fragil y hace mas fiables los flujos donde la salida debe cumplir un contrato fijo.

## Criterio de Orquestacion

No todas las tareas necesitan un agente. Si solo hace falta una respuesta de texto basta una llamada directa al modelo. Si el flujo es lineal y predecible conviene usar `LCEL`. Si el sistema necesita decidir herramientas encadenar acciones o iterar hasta llegar a una respuesta entonces tiene sentido usar un agente.

Como regla practica:
- Llamada directa: Para una sola generacion.
- `LCEL`: Para pipelines lineales con prompts modelos parsers retrieval o transformaciones.
- Agente: Para decisiones dinamicas uso de herramientas y bucles de razonamiento controlados.

## LCEL y Runnables

`LCEL` ofrece una forma simple de encadenar pasos con el operador `|` cuando el flujo es claro y determinista. Su base comun son los `Runnables` que permiten componer prompts modelos parsers y transformaciones bajo una interfaz consistente. Eso facilita reutilizar operaciones como `invoke` `batch` `ainvoke` o `stream` sin redisenar cada pipeline desde cero.

En este repositorio `LCEL` encaja mejor en escenarios donde la secuencia de pasos ya esta decidida y conviene priorizar legibilidad trazabilidad y coste estable. Esa idea aparece de forma temprana en la [practica 01](C:/Workspace/rag-agentic-ai-toolkit/spikes/01-prompting_lcel_lab/README.md) y sirve como contrapunto a los casos donde un agente con herramientas necesita mas autonomia.

## LangChain vs LangGraph

`LangChain` encaja mejor cuando el flujo es secuencial y predecible. `LangGraph` entra cuando hace falta mantener estado compartido ramificar por condiciones iterar con reintentos o pausar para una revision humana. Su modelo mental se apoya en `StateGraph` para definir la estructura fija del workflow y en un estado explicito que viaja por nodos y aristas hasta completar la tarea.

En terminos practicos `LangChain` resuelve bien prompts pipelines `RAG` clasico y `tool calling` lineal. `LangGraph` se vuelve util cuando quieres bucles aristas condicionales memoria persistente `human-in-the-loop` o ejecucion durable. Tambien facilita visualizar el flujo con Mermaid para depurar rutas antes de desplegar.

Dentro de este repositorio las practicas [01](C:/Workspace/rag-agentic-ai-toolkit/spikes/01-prompting_lcel_lab/README.md) [18](C:/Workspace/rag-agentic-ai-toolkit/spikes/18-langchain_tool_calling_math_assistant_lab/README.md) [20](C:/Workspace/rag-agentic-ai-toolkit/spikes/20-interactive_llm_agents_with_tools_lab/README.md) [21](C:/Workspace/rag-agentic-ai-toolkit/spikes/21-youtube_tool_calling_agent_lab/README.md) [22](C:/Workspace/rag-agentic-ai-toolkit/spikes/22-natural_language_data_visualization_agent_lab/README.md) [23](C:/Workspace/rag-agentic-ai-toolkit/spikes/23-natural_language_sql_agent_lab/README.md) [24](C:/Workspace/rag-agentic-ai-toolkit/spikes/24-langgraph_101_building_stateful_ai_workflows_lab/README.md) [25](C:/Workspace/rag-agentic-ai-toolkit/spikes/25-building_reflection_agent_with_langgraph_lab/README.md) [26](C:/Workspace/rag-agentic-ai-toolkit/spikes/26-building_reflection_agent_with_external_knowledge_integration/README.md) y [27](C:/Workspace/rag-agentic-ai-toolkit/spikes/27-react_build_reasoning_and_acting_ai_agents_with_langgraph/README.md) cubren el puente entre `LCEL` `tool calling` workflows con estado agentes reflexivos revision con conocimiento externo y el patron ReAct completo.

## Patrones de Agentes Auto-Mejorables

Tres patrones merecen atencion porque aparecen una y otra vez en sistemas agenticos modernos:

| Patron | Idea central | Cuando aporta mas |
| --- | --- | --- |
| `Reflection` | El modelo genera una respuesta y luego la critica para revisarla. | Cuando buscas mas claridad cobertura o calidad de redaccion sin depender de datos externos. |
| `Reflexion` | La revision se apoya en herramientas o busqueda externa para corregir con evidencia. | Cuando la precision factual importa y conviene fundamentar o citar. |
| `ReAct` | El modelo alterna razonamiento y accion en un bucle de herramientas y observaciones. | Cuando la tarea exige planificacion ligera y llamadas reales a tools o APIs. |

Estos patrones se entienden mejor si los conectas con dos ideas ya presentes en el repo. La primera es `tool calling` con control manual de ejecucion. La segunda es la salida estructurada con `Pydantic` `TypedDict` o `JSON Schema` para que el agente distinga con claridad respuesta critica consulta y resultado de herramienta.

## Multiagente y Agentic RAG

Un sistema multiagente reparte el trabajo entre roles especializados en lugar de pedirle todo a un solo modelo. Los patrones mas comunes son `pipeline` secuencial `hub-and-spoke` con un coordinador central y ejecucion en paralelo con agregacion posterior. El beneficio real no es tener mas agentes sino separar responsabilidades para reducir sobrecarga de contexto mejorar depuracion y facilitar validaciones.

`Agentic RAG` anade una capa de decision sobre el `RAG` clasico. En vez de recuperar siempre desde una sola fuente un agente puede decidir que base consultar cuando reformular una consulta cuando pedir verificacion adicional y cuando escalar a otro agente o a un humano. Esto suele mejorar robustez en dominios con varias fuentes o con consultas ambiguas.

En este repositorio la base tecnica de `Agentic RAG` ya aparece repartida entre la [practica 03](C:/Workspace/rag-agentic-ai-toolkit/spikes/03-rag_pdf_qa_bot_lab/README.md) la [09](C:/Workspace/rag-agentic-ai-toolkit/spikes/09-langchain_context_retrieval_lab/README.md) la [10](C:/Workspace/rag-agentic-ai-toolkit/spikes/10-advanced_retrievers_llamaindex_lab/README.md) la [12](C:/Workspace/rag-agentic-ai-toolkit/spikes/12-youtube_summarizer_rag_faiss_lab/README.md) la [21](C:/Workspace/rag-agentic-ai-toolkit/spikes/21-youtube_tool_calling_agent_lab/README.md) la [23](C:/Workspace/rag-agentic-ai-toolkit/spikes/23-natural_language_sql_agent_lab/README.md) la [24](C:/Workspace/rag-agentic-ai-toolkit/spikes/24-langgraph_101_building_stateful_ai_workflows_lab/README.md) la [25](C:/Workspace/rag-agentic-ai-toolkit/spikes/25-building_reflection_agent_with_langgraph_lab/README.md) la [26](C:/Workspace/rag-agentic-ai-toolkit/spikes/26-building_reflection_agent_with_external_knowledge_integration/README.md) y la [27](C:/Workspace/rag-agentic-ai-toolkit/spikes/27-react_build_reasoning_and_acting_ai_agents_with_langgraph/README.md). La practica 24 introduce el flujo con estado la 25 la reflexion iterativa la 26 suma conocimiento externo y la 27 formaliza el bucle razonar actuar observar con herramientas heterogeneas.

## Ruta de Aprendizaje Agentica en este Repo

1. Empieza por [01](C:/Workspace/rag-agentic-ai-toolkit/spikes/01-prompting_lcel_lab/README.md) para fijar prompts plantillas y `LCEL`.
2. Continua con [18](C:/Workspace/rag-agentic-ai-toolkit/spikes/18-langchain_tool_calling_math_assistant_lab/README.md) y [20](C:/Workspace/rag-agentic-ai-toolkit/spikes/20-interactive_llm_agents_with_tools_lab/README.md) para dominar `tool calling` contratos y control de ejecucion.
3. Pasa por [03](C:/Workspace/rag-agentic-ai-toolkit/spikes/03-rag_pdf_qa_bot_lab/README.md) [09](C:/Workspace/rag-agentic-ai-toolkit/spikes/09-langchain_context_retrieval_lab/README.md) [10](C:/Workspace/rag-agentic-ai-toolkit/spikes/10-advanced_retrievers_llamaindex_lab/README.md) y [12](C:/Workspace/rag-agentic-ai-toolkit/spikes/12-youtube_summarizer_rag_faiss_lab/README.md) para construir la base de `RAG` y retrieval avanzado.
4. Cierra con [21](C:/Workspace/rag-agentic-ai-toolkit/spikes/21-youtube_tool_calling_agent_lab/README.md) [22](C:/Workspace/rag-agentic-ai-toolkit/spikes/22-natural_language_data_visualization_agent_lab/README.md) [23](C:/Workspace/rag-agentic-ai-toolkit/spikes/23-natural_language_sql_agent_lab/README.md) [24](C:/Workspace/rag-agentic-ai-toolkit/spikes/24-langgraph_101_building_stateful_ai_workflows_lab/README.md) [25](C:/Workspace/rag-agentic-ai-toolkit/spikes/25-building_reflection_agent_with_langgraph_lab/README.md) [26](C:/Workspace/rag-agentic-ai-toolkit/spikes/26-building_reflection_agent_with_external_knowledge_integration/README.md) y [27](C:/Workspace/rag-agentic-ai-toolkit/spikes/27-react_build_reasoning_and_acting_ai_agents_with_langgraph/README.md) para ver agentes contra herramientas datos relacionales workflows con estado reflexion iterativa revision con evidencia externa y ReAct.
5. El siguiente salto natural sobre el material actual es extender la practica 27 hacia un caso sencillo de `agentic RAG` con recuperacion verificacion y memoria.

## Resumen de ChromaDB

Las bases de datos vectoriales simplifican el almacenamiento la organizacion y la recuperacion de datos complejos como imagenes gustos sonidos texto patrones mapas informacion genomica y otros tipos de datos de alta dimensionalidad. En lugar de guardar solo registros tradicionales almacenan objetos matematicos definidos por magnitud y direccion. Un vector es una matriz de valores numericos que representa atributos o caracteristicas de los datos originales.

Estas bases se usan en tareas de analisis que agrupan clasifican y sugieren relaciones entre elementos. Tambien aceleran sistemas de recomendacion analisis de redes sociales grafos de conocimiento analisis de grafos busqueda semantica y procesamiento de imagenes y videos. En escenarios geoespaciales ayudan en GPS gestion de flotas y sugerencias de trafico en tiempo real. En marketing y productos sociales facilitan el manejo de perfiles de usuario tendencias y optimizacion de recursos.

Las bases de datos vectoriales son una pieza importante en aprendizaje automatico porque ofrecen alto rendimiento y escalabilidad para dominios muy distintos. Para responder rapido sobre grandes colecciones suelen apoyarse en computacion distribuida indexacion procesamiento paralelo y algoritmos de vecinos mas cercanos aproximados. Entre las tecnicas mas habituales estan los indices invertidos la cuantificacion de productos y el hashing sensible a la localidad.

Existen varias familias de bases de datos vectoriales como las bases en memoria en disco distribuidas graficas y temporales. Tambien hay motores tradicionales o marcos de procesamiento que soportan busqueda vectorial guardando datos como BLOB matrices o tipos definidos por el usuario. Entre proveedores conocidos de bases vectoriales aparecen `FAISS` `Annoy` y `Milvus`. Entre sistemas con soporte de busqueda vectorial aparecen `SingleStore` `Elasticsearch` `PostgreSQL` `MySQL` `RedisAI` `MongoDB` y `Apache Cassandra`.

`ChromaDB` es una base de datos vectorial centrada en tareas de recuperacion para aplicaciones de IA. Soporta busqueda vectorial busqueda de texto completo filtrado por metadatos y escenarios multimodales. Puede ejecutarse en modo autonomo o en arquitectura cliente servidor y se integra bien con frameworks populares del ecosistema de LLMs. Su enfoque de vecinos mas cercanos aproximados permite encontrar rapidamente los fragmentos mas cercanos a una consulta dentro de una coleccion.

En este repositorio `ChromaDB` se usa como una opcion simple para flujos RAG locales. Encaja bien en practicas como la [03](C:/Workspace/rag-agentic-ai-toolkit/spikes/03-rag_pdf_qa_bot_lab/README.md) cuando hay que indexar trozos de documentos y recuperar contexto antes de responder con un modelo.

## Busqueda de Similitud

La forma manual de hacer busqueda por similitud consiste en generar embeddings normalizar vectores y comparar una consulta contra una coleccion usando distancia euclidiana producto punto o similitud coseno. Esa idea esta resumida en la [practica 05](C:/Workspace/rag-agentic-ai-toolkit/spikes/05-similarity_search_by_hand_lab/README.md) donde se implementan los calculos a mano y se comparan contra operaciones matriciales y librerias externas.

Con `ChromaDB` el flujo se simplifica: primero se crean embeddings de los documentos luego se almacenan junto con sus metadatos y finalmente se ejecutan consultas por similitud para recuperar los fragmentos mas cercanos. Esto permite construir buscadores semanticos chatbots basados en IA recuperacion de documentos y sistemas de recomendacion con menos trabajo operativo sobre indices y almacenamiento.

## Conceptos Avanzados de Retrieval

Los `retrievers` son la pieza que convierte una base de conocimiento en contexto util para un flujo `RAG`. Un `vector store retriever` usa embeddings y una base vectorial para encontrar fragmentos cercanos a una consulta. Un `advanced retriever` anade tecnicas como filtros por metadatos fusion de consultas o `reranking` para mejorar precision y cobertura.

En cursos y proyectos mas avanzados tambien aparecen estrategias como `Query Fusion` para mezclar resultados de varias formulaciones de una misma pregunta y enfoques hibridos que comparan metodos semanticos con metodos lexicos como `TF-IDF`. Estas tecnicas son relevantes cuando el top k basico no es suficiente o cuando se necesita mayor robustez frente a ambiguedad terminologica.

## FAISS vs ChromaDB vs Milvus

`FAISS` destaca cuando se necesita busqueda vectorial muy eficiente y control fino del indice en memoria. `ChromaDB` simplifica el desarrollo de aplicaciones `RAG` porque combina colecciones metadatos filtros y retrieval en una experiencia mas directa para prototipos y proyectos locales. `Milvus` entra mejor en escenarios de mayor escala y despliegue distribuido donde el volumen de vectores y los requisitos operativos son mas altos.

En este repositorio `ChromaDB` es la opcion principal porque reduce complejidad para aprendizaje y pruebas. `FAISS` y `Milvus` conviene entenderlos como alternativas importantes para retrieval avanzado y escalado de produccion.
