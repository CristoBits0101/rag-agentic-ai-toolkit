# RAG and Agentic AI Toolkit

## Estado actual

- Base FastAPI creada en `app/main.py`.
- Router versionado activo en `app/api/v1/router.py`.
- Endpoints base activos para `genai`, `gradio`, `llm`, `rag` y `prompt`.
- Flujo de Prompt Engineering modelado con `schemas`, `services` y `prompts/templates.py`.
- Varias capas ya fueron creadas como esqueleto, pero aun estan vacias.

## Arquitectura (actual)

```text
app/
  main.py
  api/
    v1/
      router.py
      genai/router.py
      gradio/router.py
      llm/router.py
      rag/router.py
      prompt/router.py
  schemas/
    prompt_schemas.py
    chat_schema.py           # vacio
    agent_schema.py          # vacio
  services/
    prompt_service.py
    llm_service.py           # vacio
  prompts/
    templates.py
    support_prompt.txt       # vacio
    orchestrator_prompt.txt  # vacio
  core/
    config.py
    settings.py              # vacio
    logging.py               # vacio
  agents/                    # vacio
  rag/                       # vacio
  embeddings/                # vacio
  vector_db/                 # vacio
  memory/                    # vacio
  tools/                     # vacio
```

## Componentes

| Componente | Ubicacion | Responsabilidad |
| --- | --- | --- |
| `main` | `app/main.py` | Bootstrap de FastAPI y registro de rutas globales. |
| `api` | `app/api/v1/...` | Capa HTTP: endpoints, metodos, codigos y validacion de entrada/salida. |
| `schemas` | `app/schemas/...` | Contratos Pydantic para requests/responses. |
| `services` | `app/services/...` | Casos de uso y orquestacion de logica de negocio. |
| `prompts` | `app/prompts/templates.py` | Plantillas reutilizables para prompts del LLM. |
| `core` | `app/core/...` | Configuracion y piezas transversales de infraestructura. |

## Endpoints documentados

| Metodo | Ruta | Estado |
| --- | --- | --- |
| GET | `/` | Activo |
| GET | `/health` | Activo |
| GET | `/api/v1/genai/` | Activo |
| GET | `/api/v1/gradio/` | Activo |
| GET | `/api/v1/llm/` | Activo |
| GET | `/api/v1/rag/` | Activo |
| GET | `/api/v1/prompt/` | Activo |
| POST | `/api/v1/prompt/exercise-1/completion` | Definido |
| POST | `/api/v1/prompt/exercise-2/task-prompts` | Definido |
| POST | `/api/v1/prompt/exercise-3/step-by-step` | Definido |
| POST | `/api/v1/prompt/exercise-4/lcel` | Definido |
| POST | `/api/v1/prompt/exercise-5/reasoning-reviews` | Definido |

## Lo que falta

### 1) Implementar archivos placeholder (vacios)

- `app/core/settings.py`
- `app/core/logging.py`
- `app/services/llm_service.py`
- `app/schemas/chat_schema.py`
- `app/schemas/agent_schema.py`
- `app/agents/base_agent.py`
- `app/agents/support_agent.py`
- `app/agents/orchestrator.py`
- `app/rag/retriever.py`
- `app/rag/chunking.py`
- `app/rag/pipeline.py`
- `app/embeddings/embedding_service.py`
- `app/vector_db/qdrant_client.py`
- `app/memory/redis_memory.py`
- `app/memory/postgres_memory.py`
- `app/tools/search_tool.py`
- `app/tools/calculator_tool.py`
- `app/tools/database_tool.py`
- `app/prompts/support_prompt.txt`
- `app/prompts/orchestrator_prompt.txt`

### 2) Corregir acoplamientos de rutas

- `app/api/v1/prompt/router.py` importa `app.service.prompt_service`.
- La ruta actual del servicio es `app/services/prompt_service.py`.
- Se debe actualizar el import para evitar `ModuleNotFoundError`.

### 3) Completar artefactos Docker

- `docker/Dockerfile` esta vacio.
- `docker/docker-compose.yml` esta vacio.
- `docker-compose.yml` en raiz tambien esta vacio.

## Instalacion

```bash
# Entorno virtual
python -m venv venv

# Activar en PowerShell
.\\venv\\Scripts\\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt
```

## Ejecucion

```bash
# Desde la raiz del repo
uvicorn app.main:app --reload
```

## Verificacion

```bash
# Salud
curl http://127.0.0.1:8000/health

# Docs OpenAPI
http://127.0.0.1:8000/docs
```

## Dependencias clave de Prompt

- `langchain`
- `langchain-core`
- `langchain-ollama`
- `OllamaLLM`
- `PromptTemplate`
