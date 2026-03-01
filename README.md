# RAG and Agentic AI Toolkit

Monolito FastAPI para experimentar con Prompt Engineering, RAG y agentes de IA.

## Arquitectura

El codigo vive en `src/app` y esta separado por capas:

- API REST: `src/app/api`, `src/app/core`, `src/app/infra`
- Dominio y contratos: `src/app/domain`, `src/app/common`
- Features y componentes IA: `src/app/modules/features`, `src/app/modules/components`

Referencia extendida: `docs/architecture.md`.

## Estructura (resumen)

```text
.
+-- compose.yaml
+-- Dockerfile
+-- pyproject.toml
+-- scripts/
+-- docs/
+-- tests/
+-- src/
    +-- app/
        +-- main.py
        +-- api/v1/endpoints/
        +-- core/
        +-- domain/
        +-- infra/
        +-- modules/components/
        +-- modules/features/
        +-- common/
```

## Requisitos

- Python 3.11+
- Dependencias del proyecto (`pip install -e .`)
- Ollama + modelo local (solo para endpoints de prompts/LLM con ejecucion real)

## Configuracion

Variables base en `.env.example`:

- `APP_AUTHOR`
- `APP_DESCRIPTION`
- `APP_NAME`
- `APP_VERSION`

La app carga `.env` via `pydantic-settings`.

## Ejecutar en desarrollo

```bash
pip install -e .
./scripts/start_dev.sh
```

Alternativa directa:

```bash
PYTHONPATH=src uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Ejecutar en produccion

```bash
./scripts/start_prod.sh
```

## Docker Compose

```bash
docker compose -f compose.yaml up --build
```

## Documentacion OpenAPI

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Endpoints activos

Base:

- `GET /`
- `GET /health`

Versionados (`/api/v1`):

- `GET /api/v1/health/`
- `GET /api/v1/agent/`
- `GET /api/v1/chat/`
- `GET /api/v1/llm/`
- `GET /api/v1/rag/`
- `GET /api/v1/prompt/`
- `POST /api/v1/prompt/exercise-1/completion`
- `POST /api/v1/prompt/exercise-2/task-prompts`
- `POST /api/v1/prompt/exercise-3/step-by-step`
- `POST /api/v1/prompt/exercise-4/lcel`
- `POST /api/v1/prompt/exercise-5/reasoning-reviews`

## Nota operativa de prompts

Si faltan dependencias de LangChain/Ollama o el modelo local no esta disponible,
los endpoints de prompts pueden responder `503 Service Unavailable`.

## Tests

```bash
python -m pytest -q
```

`tests/conftest.py` agrega `src/` al `PYTHONPATH` para importar `app.*`.
