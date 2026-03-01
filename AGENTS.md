# AGENTS.md

Guia operativa para mantener coherencia tecnica en este monolito FastAPI.

## Objetivo

Estandarizar como se agregan routers, services, schemas y prompts para evitar acoplamientos y regresiones.

## Convenciones de arquitectura

- `app/rest_api/api/v1`: capa HTTP (`*_router.py`).
- `app/rest_api/services`: casos de uso y orquestacion.
- `app/rest_api/schemas`: contratos Pydantic request/response.
- `app/ai_agents/prompts`: plantillas y prompts reutilizables.
- `app/rest_api/core`: configuracion y utilidades transversales.

## Convenciones de nombres

- Routers: `*_router.py`.
- Services: `*_service.py`.
- Schemas: `*_schema.py` o `<dominio>_schemas.py`.
- Prompts: `templates.py` y `*_prompt.txt`.

## Reglas de imports

- Import absoluto desde `app...`.
- Correcto: `from app.rest_api.services.prompt_service import prompt_service`.
- Evitar rutas antiguas tipo `app.service...`.

## Flujo recomendado

1. Definir o ajustar schema en `app/rest_api/schemas`.
2. Implementar logica en `app/rest_api/services`.
3. Exponer endpoint en `app/rest_api/api/v1/*_router.py`.
4. Registrar router en `app/rest_api/api/v1/router.py`.
5. Si aplica, agregar o actualizar prompt en `app/ai_agents/prompts`.
6. Agregar test smoke o regresion en `tests/`.

## Criterios minimos por cambio

- El modulo compila e importa (`python -m compileall app`).
- Endpoints nuevos aparecen en `/docs`.
- Si toca rutas existentes, actualizar test smoke.
- No introducir logica de negocio dentro de routers.

## Testing

Comando base:

```bash
python -m pytest -q
```

Si no existen dependencias de test en el entorno:

```bash
pip install pytest httpx
```

## Notas operativas

- Endpoints de prompt deben responder `503` cuando falten dependencias o modelos LLM.
- Mantener `README.md` sincronizado con estructura real y rutas activas.
- No mover prompts reutilizables a `api/`; deben permanecer en `app/ai_agents/prompts`.
