# FastAPI

## Comandos de configuración y ejecución

```bash
# Configuración de Git para evitar problemas de saltos de línea
git config --global core.autocrlf input

# Crear entorno virtual
python3 -m venv venv

# Activar entorno en Windows PowerShell
.\venv\Scripts\Activate.ps1

# Instalar dependencias
pip install fastapi uvicorn[standard] gunicorn pydantic-settings

# Generar requirements.txt
pip freeze > requirements.txt

# Ejecutar servidor en desarrollo
# main:app hace referencia a la variable 'app' dentro de main.py
uvicorn main:app --reload

# /app/main.py:app
uvicorn app.main:app --reload
```

## Formateo de código

```bash
# Instalar Black (si no está instalado)
pip install black

# Formatear el proyecto
black .
```

## Rutas de la API

| Método | Ruta | Descripción |
| --- | --- | --- |
| GET | `http://127.0.0.1:8000/` | Información general del servicio. |
| GET | `http://127.0.0.1:8000/health` | Estado de salud (`{"status": "ok"}`). |
| GET | `http://127.0.0.1:8000/api/v1/genai/` | Mensaje de éxito de GenAI. |
| GET | `http://127.0.0.1:8000/api/v1/gradio/` | Mensaje de éxito de Gradio. |
| GET | `http://127.0.0.1:8000/api/v1/llm/` | Mensaje de éxito de LLM. |
| GET | `http://127.0.0.1:8000/api/v1/prompt/` | Mensaje de éxito para generación de prompts. |
| GET | `http://127.0.0.1:8000/api/v1/rag/` | Mensaje de éxito de RAG. |

## Componentes del proyecto

| Componente | Ubicación | ¿Para qué sirve? | Ejemplo |
| --- | --- | --- | --- |
| `main` | `app/main.py` | Punto de entrada de FastAPI. Crea la app, configura metadata y registra rutas globales (`/`, `/health`, `/api/v1`). | `app.include_router(api_v1_router)` |
| `api` | `app/api/v1/...` | Capa HTTP. Define endpoints, métodos, validación de entrada/salida y códigos de respuesta. No debería contener lógica pesada de negocio. | `app/api/v1/prompt/router.py` |
| `service` | `app/service/...` | Lógica de negocio y orquestación de casos de uso. Recibe datos ya validados desde `api` y ejecuta el flujo principal. | `app/service/prompt_service.py` |
| `schemas` | `app/schemas/...` | Modelos Pydantic para requests/responses. Garantiza contrato de datos entre cliente y API. | `app/schemas/prompt_schemas.py` |
| `core` | `app/core/...` | Configuración compartida y utilidades base de infraestructura (settings, constantes globales, etc.). | `app/core/config.py` |
| `templates` | `app/api/v1/prompt/prompt_engineering_templates.py` | Plantillas y textos base reutilizables de prompts (sin acoplarse a HTTP). | `DEFAULT_REVIEW_TEMPLATE` |
| `requirements` | `requirements.txt` | Dependencias necesarias para ejecutar la aplicación. | `fastapi`, `langchain`, `uvicorn` |

## Flujo y orden de llamadas

```text
Cliente (Postman/Frontend/curl)
        |
        v
app/main.py
  FastAPI app + include_router(api_v1_router)
        |
        v
app/api/v1/router.py
  Router principal /api/v1
        |
        +-------------------> /genai  -> app/api/v1/genai/router.py
        +-------------------> /llm    -> app/api/v1/llm/router.py
        +-------------------> /gradio -> app/api/v1/gradio/router.py
        +-------------------> /rag    -> app/api/v1/rag/router.py
        |
        +-------------------> /prompt -> app/api/v1/prompt/router.py
                                      |
                                      v
                           app/schemas/prompt_schemas.py
                           (valida request/response)
                                      |
                                      v
                           app/service/prompt_service.py
                           (lógica de negocio)
                                      |
                                      v
                           app/api/v1/prompt/prompt_engineering_templates.py
                           (plantillas base de prompts)
                                      |
                                      v
                           LangChain/Ollama (ejecución LLM)
                                      |
                                      v
                              Respuesta JSON al cliente
```
