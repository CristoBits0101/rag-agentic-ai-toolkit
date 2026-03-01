# RAG and Agentic AI Toolkit

Toolkit monolitico en FastAPI para experimentar con Prompt Engineering, RAG y orquestacion de agentes.

## Estructura actual

```text
app/
|-- main.py
|-- rest_api/
|   |-- api/
|   |   `-- v1/
|   |       |-- router.py
|   |       |-- agent_router.py
|   |       |-- chat_router.py
|   |       |-- llm_router.py
|   |       |-- rag_router.py
|   |       `-- prompt_router.py
|   |-- core/
|   |-- db/
|   |-- middleware/
|   |-- models/
|   |-- repository/
|   |-- schemas/
|   |-- services/
|   `-- utils/
|-- ai_agents/
|   |-- agents/
|   |-- embeddings/
|   |-- memory/
|   |-- prompts/
|   |-- rag/
|   |-- tools/
|   `-- vector_db/
`-- __pycache__/            # autogenerado por Python
```

## Grupos de carpetas dentro de app

### Grupo 1: API REST

- `app/rest_api/api`: capa HTTP y versionado de endpoints (`v1`).
- `app/rest_api/schemas`: contratos Pydantic de entrada/salida.
- `app/rest_api/services`: casos de uso y logica de negocio de API.
- `app/rest_api/core`: configuracion global, settings y logging transversal.
- `app/rest_api/db`: configuracion de conexion y session de base de datos.
- `app/rest_api/middleware`: middlewares cross-cutting.
- `app/rest_api/models`: modelos de persistencia/ORM.
- `app/rest_api/repository`: acceso a datos (DAO/Repository).
- `app/rest_api/utils`: helpers utilitarios compartidos.

### Grupo 2: Agentes de IA

- `app/ai_agents/agents`: base de agentes, orquestador y especializaciones.
- `app/ai_agents/prompts`: plantillas reutilizables y prompts de sistema.
- `app/ai_agents/rag`: chunking, retrieval y pipeline RAG.
- `app/ai_agents/embeddings`: generacion y normalizacion de embeddings.
- `app/ai_agents/vector_db`: cliente del motor vectorial.
- `app/ai_agents/memory`: memoria conversacional (redis/postgres).
- `app/ai_agents/tools`: herramientas invocables por agentes.

## Capas y responsabilidades (actuales y futuras)

| Capa | Ruta | Responsabilidad actual | Responsabilidad futura |
| --- | --- | --- | --- |
| API | `app/rest_api/api/v1/*_router.py` | Exponer endpoints y validar contrato HTTP basico. | Versionado de API, manejo de errores estandar y auth por router. |
| Schemas | `app/rest_api/schemas/*.py` | Definir modelos de entrada/salida para prompt y base de chat/agent. | Contratos completos por dominio (`agent`, `chat`, `rag`) con validaciones de negocio. |
| Services | `app/rest_api/services/*_service.py` | Ejecutar casos de uso de prompt engineering y wrapper de LLM. | Orquestacion de agentes, politicas de retries/timeouts y trazabilidad por request. |
| Agents | `app/ai_agents/agents/*` | Estructura creada (base/orchestrator/support) aun sin logica productiva. | Router inteligente de tareas, delegacion multi-agente y control de herramientas. |
| Prompts | `app/ai_agents/prompts/*` | Plantillas base y archivos de prompt del sistema. | Versionado de prompts, variantes por canal/idioma y experimentacion A/B. |
| RAG | `app/ai_agents/rag/*` | Estructura de pipeline/retriever/chunking preparada. | Ingestion documental, chunking configurable, retrieval hibrido y reranking. |
| Embeddings | `app/ai_agents/embeddings/*` | Capa placeholder para generacion de embeddings. | Normalizacion de embeddings, caching y soporte multi-modelo. |
| Vector DB | `app/ai_agents/vector_db/*` | Cliente placeholder para motor vectorial. | Integracion real con Qdrant, colecciones, filtros y busqueda semantica. |
| Memory | `app/ai_agents/memory/*` | Estructura placeholder para memoria conversacional. | Memoria corta/larga por sesion con Redis/Postgres y politicas de expiracion. |
| Tools | `app/ai_agents/tools/*` | Carpeta de herramientas definida sin implementacion funcional. | Tool calling seguro (search/db/calc), permisos y auditoria de ejecuciones. |
| Core | `app/rest_api/core/*` | Config base y archivos de settings/logging creados. | Config central por entorno, secretos, observabilidad y logging estructurado. |

## Rutas activas

| Metodo | Ruta |
| --- | --- |
| GET | `/` |
| GET | `/health` |
| GET | `/api/v1/agent/` |
| GET | `/api/v1/chat/` |
| GET | `/api/v1/llm/` |
| GET | `/api/v1/rag/` |
| GET | `/api/v1/prompt/` |
| POST | `/api/v1/prompt/exercise-1/completion` |
| POST | `/api/v1/prompt/exercise-2/task-prompts` |
| POST | `/api/v1/prompt/exercise-3/step-by-step` |
| POST | `/api/v1/prompt/exercise-4/lcel` |
| POST | `/api/v1/prompt/exercise-5/reasoning-reviews` |

Nota: los endpoints de `prompt` devuelven `503` cuando faltan dependencias/modelos LLM en runtime.

## Instalacion

```bash
python -m venv venv
.\\venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
```

## Ejecucion

```bash
uvicorn app.main:app --reload
```

## Tests

Smoke tests en `tests/test_api_smoke.py`.

```bash
python -m pytest -q
```

## Estado de implementacion

Modulos aun en modo placeholder (estructura creada, implementacion pendiente):

- `app/ai_agents/agents/*`
- `app/rest_api/core/settings.py`
- `app/rest_api/core/logging.py`
- `app/rest_api/services/llm_service.py`
- `app/ai_agents/rag/*`
- `app/ai_agents/embeddings/embedding_service.py`
- `app/ai_agents/vector_db/qdrant_client.py`
- `app/ai_agents/memory/*`
- `app/ai_agents/tools/*`
- `app/rest_api/schemas/agent_schema.py`
- `app/rest_api/schemas/chat_schema.py`
- `app/ai_agents/prompts/orchestrator_prompt.txt`
- `app/ai_agents/prompts/support_prompt.txt`

## Docker

Archivos presentes pero vacios:

- `docker/Dockerfile`
- `docker/docker-compose.yml`
- `docker-compose.yml`
