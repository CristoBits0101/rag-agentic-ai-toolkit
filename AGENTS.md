# AGENTS.md

Guia operativa para mantener coherencia tecnica en este monolito FastAPI.

## Objetivo

Estandarizar como se agregan routers, services, schemas y prompts para evitar acoplamientos y regresiones.

## Convenciones de arquitectura

- `app/api/v1`: capa HTTP (`*_router.py`).
- `app/services`: casos de uso y orquestacion.
- `app/schemas`: contratos Pydantic request/response.
- `app/prompts`: plantillas y prompts reutilizables.
- `app/core`: configuracion y utilidades transversales.

## Convenciones de nombres

- Routers: `*_router.py`.
- Services: `*_service.py`.
- Schemas: `*_schema.py` o `<dominio>_schemas.py`.
- Prompts: `templates.py` y `*_prompt.txt`.

## Reglas de imports

- Import absoluto desde `app...`.
- Correcto: `from app.services.prompt_service import prompt_service`.
- Evitar rutas antiguas tipo `app.service...`.

## Flujo recomendado

1. Definir o ajustar schema en `app/schemas`.
2. Implementar logica en `app/services`.
3. Exponer endpoint en `app/api/v1/*_router.py`.
4. Registrar router en `app/api/v1/router.py`.
5. Si aplica, agregar o actualizar prompt en `app/prompts`.
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
- No mover prompts reutilizables a `api/`; deben permanecer en `app/prompts`.
