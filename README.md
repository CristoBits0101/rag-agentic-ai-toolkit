# RAG and Agentic AI Toolkit

Toolkit monolitico en FastAPI para experimentar con Prompt Engineering, RAG y agentes de IA.

## Estructura del proyecto

```text
.
├── pyproject.toml
├── README.md
├── .env.example
├── .gitignore
├── compose.yaml
├── Dockerfile
├── scripts/
│   ├── start_dev.sh
│   └── start_prod.sh
├── docs/
│   └── architecture.md
├── tests/
│   ├── unit/
│   ├── integration/
│   └── conftest.py
└── src/
    └── app/
        ├── __init__.py
        ├── main.py
        ├── api/
        │   ├── __init__.py
        │   └── v1/
        │       ├── __init__.py
        │       ├── router.py
        │       └── endpoints/
        │           ├── __init__.py
        │           ├── health.py
        │           ├── chat.py
        │           ├── agents.py
        │           ├── retrieval.py
        │           ├── llm.py
        │           └── prompts.py
        ├── core/
        │   ├── __init__.py
        │   ├── settings.py
        │   ├── logging.py
        │   ├── errors.py
        │   └── security.py
        ├── infra/
        │   ├── __init__.py
        │   ├── db/
        │   │   ├── __init__.py
        │   │   ├── session.py
        │   │   └── models/
        │   ├── cache/
        │   │   ├── __init__.py
        │   │   └── redis_client.py
        │   └── vector_db/
        │       ├── __init__.py
        │       └── qdrant_client.py
        ├── modules/
        │   ├── __init__.py
        │   ├── capabilities/
        │   │   ├── __init__.py
        │   │   ├── llm/
        │   │   │   ├── __init__.py
        │   │   │   ├── client.py
        │   │   │   └── schemas.py
        │   │   ├── retrieval/
        │   │   │   ├── __init__.py
        │   │   │   ├── chunking.py
        │   │   │   ├── retriever.py
        │   │   │   ├── pipeline.py
        │   │   │   ├── embeddings/
        │   │   │   │   ├── __init__.py
        │   │   │   │   └── embedding_service.py
        │   │   │   └── schemas.py
        │   │   ├── agents/
        │   │   │   ├── __init__.py
        │   │   │   ├── orchestrators/
        │   │   │   │   ├── __init__.py
        │   │   │   │   └── orchestrator.py
        │   │   │   ├── agents/
        │   │   │   │   ├── __init__.py
        │   │   │   │   ├── base_agent.py
        │   │   │   │   └── support_agent.py
        │   │   │   ├── tools/
        │   │   │   │   ├── __init__.py
        │   │   │   │   ├── calculator_tool.py
        │   │   │   │   ├── database_tool.py
        │   │   │   │   └── search_tool.py
        │   │   │   ├── memory/
        │   │   │   │   ├── __init__.py
        │   │   │   │   ├── postgres_memory.py
        │   │   │   │   └── redis_memory.py
        │   │   │   ├── prompts/
        │   │   │   │   ├── __init__.py
        │   │   │   │   ├── templates.py
        │   │   │   │   ├── orchestrator_prompt.txt
        │   │   │   │   └── support_prompt.txt
        │   │   │   └── schemas.py
        │   │   └── vision/
        │   │       ├── __init__.py
        │   │       ├── pipelines.py
        │   │       └── schemas.py
        │   └── apps/
        │       ├── __init__.py
        │       ├── chatbot/
        │       │   ├── __init__.py
        │       │   ├── service.py
        │       │   └── schemas.py
        │       ├── doc_qa/
        │       │   ├── __init__.py
        │       │   ├── service.py
        │       │   └── schemas.py
        │       └── agent_runner/
        │           ├── __init__.py
        │           ├── service.py
        │           └── schemas.py
        └── common/
            ├── __init__.py
            ├── types.py
            └── utils/
                ├── __init__.py
                └── strings.py
```

## Ejecutar en desarrollo

```bash
pip install -e .
./scripts/start_dev.sh
```

## Ejecutar con Docker Compose

```bash
docker compose -f compose.yaml up --build
```

## Tests

```bash
python -m pytest -q
```

Nota: `tests/conftest.py` agrega `src/` al `PYTHONPATH` para importar `app.*`.
