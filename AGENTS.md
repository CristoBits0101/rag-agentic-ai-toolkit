# AGENTS.md

Guia operativa para mantener coherencia tecnica en este monolito FastAPI.

## Objetivo

Estandarizar como se agregan endpoints, services, schemas y prompts para evitar acoplamientos y regresiones.

## Convenciones de arquitectura

- `src/app/api/v1/endpoints`: capa HTTP (`*.py`).
- `src/app/modules/apps`: casos de uso de aplicacion.
- `src/app/modules/capabilities`: capacidades IA reutilizables.
- `src/app/core`: configuracion y utilidades transversales.
- `src/app/infra`: adaptadores a servicios externos.

## Reglas de imports

- Import absoluto desde `app...`.
- Correcto: `from app.modules.apps.chatbot.service import prompt_service`.
- Evitar rutas antiguas tipo `app.service...`.

## Flujo recomendado

1. Definir o ajustar schema en `src/app/modules/**/schemas.py`.
2. Implementar logica en `src/app/modules/**/service.py` o `client.py`.
3. Exponer endpoint en `src/app/api/v1/endpoints/*.py`.
4. Registrar endpoint en `src/app/api/v1/router.py`.
5. Si aplica, agregar o actualizar prompt en `src/app/modules/capabilities/agents/prompts`.
6. Agregar test en `tests/unit` o `tests/integration`.

## Criterios minimos por cambio

- El modulo compila e importa (`python -m compileall src/app`).
- Endpoints nuevos aparecen en `/docs`.
- Si toca rutas existentes, actualizar smoke tests.
- No introducir logica de negocio dentro de endpoints.

## Testing

```bash
python -m pytest -q
```

Si no existen dependencias de test:

```bash
pip install pytest httpx
```
