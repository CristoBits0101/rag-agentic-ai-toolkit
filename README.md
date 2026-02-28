# RAG and Agentic AI Toolkit

Toolkit monolitico en FastAPI para experimentar con Prompt Engineering, RAG y orquestacion de agentes.

## Estructura actual

```text
app/
|-- main.py
|-- api/
|   `-- v1/
|       |-- router.py
|       |-- agent_router.py
|       |-- chat_router.py
|       |-- llm_router.py
|       |-- rag_router.py
|       `-- prompt_router.py
|-- agents/
|-- core/
|-- db/
|-- embeddings/
|-- memory/
|-- middleware/
|-- models/
|-- prompts/
|-- rag/
|-- repository/
|-- schemas/
|-- services/
|-- tools/
|-- utils/
|-- vector_db/
`-- __pycache__/            # autogenerado por Python
```
## Carpetas en app (completo)

| Carpeta | Estado actual | Responsabilidad actual/futura |
| --- | --- | --- |
| `app/api` | Activa | Capa HTTP y versionado de endpoints (`v1`). |
| `app/agents` | Placeholder | Base de agentes, orquestador y especializaciones. |
| `app/core` | Parcial | Configuracion global, settings y logging transversal. |
| `app/db` | Placeholder | Configuracion de conexion y session de base de datos. |
| `app/embeddings` | Placeholder | Generacion/normalizacion de embeddings. |
| `app/memory` | Placeholder | Memoria conversacional (redis/postgres). |
| `app/middleware` | Placeholder | Middlewares cross-cutting (logs, trace, auth, rate-limit). |
| `app/models` | Placeholder | Modelos de persistencia/ORM. |
| `app/prompts` | Activa | Plantillas reutilizables y prompts de sistema. |
| `app/rag` | Placeholder | Chunking, retrieval y pipeline RAG. |
| `app/repository` | Placeholder | Acceso a datos (DAO/Repository pattern). |
| `app/schemas` | Parcial | Contratos Pydantic de entrada/salida. |
| `app/services` | Parcial | Casos de uso y orquestacion de negocio. |
| `app/tools` | Placeholder | Herramientas invocables por agentes. |
| `app/utils` | Placeholder | Helpers utilitarios compartidos. |
| `app/vector_db` | Placeholder | Cliente del motor vectorial (Qdrant u otro). |
| `app/__pycache__` | Autogenerado | Cache de bytecode Python; no es capa funcional. |

## Capas y responsabilidades (actuales y futuras)

| Capa | Ruta | Responsabilidad actual | Responsabilidad futura |
| --- | --- | --- | --- |
| API | `app/api/v1/*_router.py` | Exponer endpoints y validar contrato HTTP basico. | Versionado de API, manejo de errores estandar y auth por router. |
| Schemas | `app/schemas/*.py` | Definir modelos de entrada/salida para prompt y base de chat/agent. | Contratos completos por dominio (`agent`, `chat`, `rag`) con validaciones de negocio. |
| Services | `app/services/*_service.py` | Ejecutar casos de uso de prompt engineering y wrapper de LLM. | Orquestacion de agentes, politicas de retries/timeouts y trazabilidad por request. |
| Agents | `app/agents/*` | Estructura creada (base/orchestrator/support) aun sin logica productiva. | Router inteligente de tareas, delegacion multi-agente y control de herramientas. |
| Prompts | `app/prompts/*` | Plantillas base y archivos de prompt del sistema. | Versionado de prompts, variantes por canal/idioma y experimentacion A/B. |
| RAG | `app/rag/*` | Estructura de pipeline/retriever/chunking preparada. | Ingestion documental, chunking configurable, retrieval hibrido y reranking. |
| Embeddings | `app/embeddings/*` | Capa placeholder para generacion de embeddings. | Normalizacion de embeddings, caching y soporte multi-modelo. |
| Vector DB | `app/vector_db/*` | Cliente placeholder para motor vectorial. | Integracion real con Qdrant, colecciones, filtros y busqueda semantica. |
| Memory | `app/memory/*` | Estructura placeholder para memoria conversacional. | Memoria corta/larga por sesion con Redis/Postgres y politicas de expiracion. |
| Tools | `app/tools/*` | Carpeta de herramientas definida sin implementacion funcional. | Tool calling seguro (search/db/calc), permisos y auditoria de ejecuciones. |
| Core | `app/core/*` | Config base y archivos de settings/logging creados. | Config central por entorno, secretos, observabilidad y logging estructurado. |
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

- `app/agents/*`
- `app/core/settings.py`
- `app/core/logging.py`
- `app/services/llm_service.py`
- `app/rag/*`
- `app/embeddings/embedding_service.py`
- `app/vector_db/qdrant_client.py`
- `app/memory/*`
- `app/tools/*`
- `app/schemas/agent_schema.py`
- `app/schemas/chat_schema.py`
- `app/prompts/orchestrator_prompt.txt`
- `app/prompts/support_prompt.txt`

## Docker

Archivos presentes pero vacios:

- `docker/Dockerfile`
- `docker/docker-compose.yml`
- `docker-compose.yml`


