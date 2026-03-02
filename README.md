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
pip install fastapi==0.134.0
pip install "uvicorn[standard]==0.41.0"
pip install gunicorn==25.1.0
pip install pydantic-settings==2.13.1
pip install langchain==0.3.27
pip install langchain-core==0.3.80
pip install langchain-ollama==0.3.10
pip install python-dotenv==1.2.1
pip install PyYAML==6.0.3
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

## Comandos utiles despues de instalar

```bash
# Instalar el proyecto en modo editable.
pip install -e .

# Ejecutar API en desarrollo.
PYTHONPATH=src uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Guardar lock simple de dependencias.
pip freeze > requirements.txt
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

## Glosario de Terminos

| Termino | Descripcion |
| --- | --- |
| Agentes de IA | Sistemas basados en inteligencia artificial que planifican acciones y ejecutan tareas con cierto grado de autonomia. |
| Chain-of-Thought | Tecnica de prompting que fuerza un razonamiento intermedio paso a paso para mejorar respuestas complejas. |
| Chaining | Flujo secuencial Retrieval -> Extraction -> Processing -> Generation para transformar contexto en una salida util. |
| Embeddings | Vectores numericos que representan el significado semantico de palabras frases o documentos. |
| Fine-tuning | Ajuste adicional de un modelo preentrenado con datos de dominio para mejorar su rendimiento en tareas especificas. |
| Hallucination Mitigation | Estrategias para reducir respuestas inventadas o inexactas en modelos de lenguaje. |
| LangChain | Framework de codigo abierto para crear aplicaciones con LLMs y componentes como prompts cadenas agentes y herramientas. |
| LCEL | Lenguaje declarativo de LangChain para componer cadenas de ejecucion centradas en LLM de forma modular. |
| Lematizacion | Proceso de reducir palabras a su forma canonica para normalizar texto y mejorar analisis. |
| LLM | Modelo de lenguaje de gran escala entrenado para comprender y generar texto. |
| Multi-Agent System | Arquitectura donde varios agentes cooperan para resolver objetivos comunes. |
| NLG | Generacion de lenguaje natural a partir de datos o representaciones internas. |
| NLP | Procesamiento de lenguaje natural para analizar y transformar texto humano en estructuras utiles. |
| NLU | Comprension del lenguaje natural para extraer intencion entidades y contexto semantico. |
| Orchestration | Coordinacion del flujo entre agentes herramientas y pasos de ejecucion. |
| Prompting | Diseno de instrucciones y contexto para guiar la salida de un modelo. |
| Prompting Templates | Plantillas reutilizables para estructurar prompts de forma consistente. |
| RAG | Enfoque que combina recuperacion de informacion y generacion para producir respuestas mas precisas y trazables. |
| Retrieval | Proceso de recuperar contexto relevante desde una base de conocimiento antes de generar una respuesta. |
| Tokenizacion | Segmentacion del texto en unidades llamadas tokens para su procesamiento por modelos. |
| Vector Database | Base de datos optimizada para almacenar y consultar vectores por similitud semantica. |

## Tipos de Agentes

| Termino | Descripcion |
| --- | --- |
| Agentes de IA | Integran LLMs con planificacion herramientas y memoria para ejecutar acciones autonomas. |
| IA Generativa | Predice la siguiente secuencia probable y genera texto imagen audio o video segun el modelo. |
| LLMs | No son agentes por si solos y producen texto de salida a partir de texto de entrada sin herramientas externas. |
| Multimodal Generative AI | Procesa y genera varios tipos de datos en una misma interaccion. |
| RAG | Combina recuperacion de informacion y generacion para fundamentar respuestas con contexto externo. |

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
