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

# LangChain Ollama: Integracion con modelos servidos por Ollama.
pip install -U langchain-ollama

# ChromaDB: Base de datos vectorial para retrieval local.
pip install -U chromadb

# Python Dotenv: Carga variables de entorno desde archivos .env.
pip install -U python-dotenv

# PyYAML: Lectura y escritura de archivos YAML.
pip install -U PyYAML

# Gradio: Interfaces web rapidas para demos y pruebas.
pip install -U gradio

# Hugging Face Hub: Acceso a modelos datasets y artefactos.
pip install -U huggingface_hub
```

## Ollama

```bash
# Instalar Ollama.
irm https://ollama.com/install.ps1 | iex

# Descargar un modelo local de ejemplo.
ollama pull llama3.2:3b

# Verificar.
ollama --version
ollama list
```

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

# Ejecutar la practica de introduccion a ChromaDB.
python .\spikes\06-vector_databases_chromadb_cheat_sheet_lab\main.py
```

## Ejecutar Practica 07

```powershell
# Activar el entorno virtual.
.\venv\Scripts\Activate.ps1

# Ejecutar la practica de similitud sobre empleados y libros con ChromaDB.
python .\spikes\07-employee_similarity_search_chromadb_lab\main.py
```

## Ejecutar Practica 08

```powershell
# Activar el entorno virtual.
.\venv\Scripts\Activate.ps1

# Ejecutar la practica de recomendaciones de comida con ChromaDB y RAG.
python .\spikes\08-food_recommendation_systems_chromadb_rag_lab\main.py
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
```

## Glosario de Terminos

| Termino | Descripcion |
| --- | --- |
| Agentes de IA | Sistemas basados en inteligencia artificial que planifican acciones y ejecutan tareas con cierto grado de autonomia. |
| ANN | Busqueda aproximada de vecinos mas cercanos para escalar retrieval vectorial con baja latencia. |
| Advanced Retriever | Recuperador con estrategias mas sofisticadas que un top k simple como fusion filtros o reranking. |
| Chain-of-Thought | Tecnica de prompting que fuerza un razonamiento intermedio paso a paso para mejorar respuestas complejas. |
| Chaining | Flujo secuencial Retrieval -> Extraction -> Processing -> Generation para transformar contexto en una salida util. |
| ChromaDB | Base de datos vectorial orientada a embeddings usada para almacenar y recuperar contexto por similitud semantica. |
| Chunk | Trozo de texto dividido de un archivo. |
| Chunking Strategy | Criterio para dividir documentos en fragmentos antes del indexado y la recuperacion. |
| Embeddings | Vectores numericos que representan el significado semantico de palabras frases o documentos. |
| FAISS | Libreria de Meta para busqueda vectorial eficiente y de alto rendimiento orientada a similitud en memoria. |
| Fine-tuning | Ajuste adicional de un modelo preentrenado con datos de dominio para mejorar su rendimiento en tareas especificas. |
| Hallucination Mitigation | Estrategias para reducir respuestas inventadas o inexactas en modelos de lenguaje. |
| HNSW | Indice basado en grafos para recuperar vecinos cercanos aproximados con buena velocidad y precision. |
| LangChain | Framework de codigo abierto para crear aplicaciones con LLMs y componentes como prompts cadenas agentes y herramientas. |
| LCEL | Lenguaje declarativo de LangChain para componer cadenas de ejecucion centradas en LLM de forma modular. |
| Lematizacion | Proceso de reducir palabras a su forma canonica para normalizar texto y mejorar analisis. |
| LlamaIndex | Framework para construir aplicaciones con LLMs orientadas a documentos indices y retrieval en flujos RAG. |
| LLM | Modelo de lenguaje de gran escala entrenado para comprender y generar texto. |
| LSH | Tecnica de hashing sensible a la localidad usada para aproximar similitud en espacios de alta dimension. |
| Milvus | Base de datos vectorial orientada a escalado y despliegues de produccion sobre grandes colecciones. |
| Multi-Agent System | Arquitectura donde varios agentes cooperan para resolver objetivos comunes. |
| NLG | Generacion de lenguaje natural a partir de datos o representaciones internas. |
| NLP | Procesamiento de lenguaje natural para analizar y transformar texto humano en estructuras utiles. |
| NLU | Comprension del lenguaje natural para extraer intencion entidades y contexto semantico. |
| Orchestration | Coordinacion del flujo entre agentes herramientas y pasos de ejecucion. |
| Point | 1 point = 1 chunk como objeto guardado en la vector DB. |
| Prompting | Diseno de instrucciones y contexto para guiar la salida de un modelo. |
| Prompting Templates | Plantillas reutilizables para estructurar prompts de forma consistente. |
| Query Fusion | Estrategia que combina resultados de varias consultas o recuperadores para mejorar cobertura y relevancia. |
| RAG | Enfoque que combina recuperacion de informacion y generacion para producir respuestas mas precisas y trazables. |
| Reranking | Reordenacion posterior de resultados recuperados para mejorar la relevancia final. |
| Retriever | Componente encargado de recuperar contexto relevante desde una base de conocimiento indexada. |
| Retrieval | Proceso de recuperar contexto relevante desde una base de conocimiento antes de generar una respuesta. |
| TF-IDF | Representacion clasica de texto basada en frecuencia de termino y frecuencia inversa de documento. |
| Tokenizacion | Segmentacion del texto en unidades llamadas tokens para su procesamiento por modelos. |
| Vector Database | Base de datos optimizada para almacenar y consultar vectores por similitud semantica. |
| Vector Store Retriever | Recuperador que usa una base vectorial para localizar fragmentos cercanos a una consulta embebida. |

## Tipos de Sistemas de IA

| Termino | Descripcion |
| --- | --- |
| IA Generativa | Predice la siguiente secuencia probable y genera texto imagen audio o video segun el modelo. |
| RAG | Combina recuperacion de informacion y generacion para fundamentar respuestas con contexto externo. |
| Agentes de IA | Integran LLMs con planificacion herramientas y memoria para ejecutar acciones autonomas. |
| IA Generativa Multimodal | Procesa y genera varios tipos de datos en una misma interaccion. |

## IA Generativa para Tareas Especificas

| Termino | Descripcion |
| --- | --- |
| Language Translation | Traduccion automatica de contenido entre idiomas. |
| Sentiment Analysis | Clasificacion de la emocion o postura expresada en un texto. |
| Spam Detection | Identificacion de mensajes no deseados o maliciosos. |
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
