# Architecture

## Layout rationale

- `src/app/api`: HTTP layer (versioned routers and endpoints).
- `src/app/core`: settings, logging, and cross-cutting concerns.
- `src/app/infra`: technical adapters (db/cache/vector-store).
- `src/app/modules/components`: reusable AI capabilities (llm, retrieval, agents).
- `src/app/modules/use_cases`: application-level use cases.
- `src/app/common`: shared utility types/functions.

## Current active API routes

- `GET /`
- `GET /health`
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
