# FastAPI

## Leyenda

1. LangChain: Prompts, Memory, Chains, Agents, Tools, RAG, LLMs
2. LangChain Core: PromptTemplate, Runnable/LCEL, ChatModel/LLM, OutputParser
3. LangChain Ollama: llama3.1:latest, mistral:latest, phi3.5:latest

## Instalacion

1. Ollama: `irm https://ollama.com/install.ps1 | iex`
2. LLM llama3.2:3b: `ollama pull llama3.2:3b`
3. LangChain*: `pip install -U langchain langchain-core langchain-ollama`
4. LangChain Ollama: `pip install -U langchain-ollama`

## Verificacion

1. Ollama: `ollama --version`
2. Ollama Servidor: `ollama serve`
3. LangChain: `pip show langchain`
4. Ollama Modelos: `ollama list`

## Dependencias (Prompt)

1. `OllamaLLM`: Para interactuar con modelos Ollama desde LangChain.
2. `PromptTemplate`: Para crear plantillas de prompts con variables dinamicas.

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
| `main` | `app/main.py` | Bootstrap FastAPI: instancia app, metadata y registro de routers. | `app.include_router(api_v1_router)` |
| `api` | `app/api/v1/...` | Capa HTTP: rutas, métodos, contratos y manejo de estado HTTP. | `app/api/v1/prompt/router.py` |
| `service` | `app/service/...` | Capa de negocio: ejecuta casos de uso y orquesta integraciones. | `app/service/prompt_service.py` |
| `schemas` | `app/schemas/...` | Contratos Pydantic: validación y tipado de request/response. | `app/schemas/prompt_schemas.py` |
| `core` | `app/core/...` | Núcleo compartido: settings, constantes y utilidades transversales. | `app/core/config.py` |
| `templates` | `app/prompts/templates.py` | Repositorio de prompts base reutilizables desacoplados de HTTP. | `DEFAULT_REVIEW_TEMPLATE` |
| `requirements` | `requirements.txt` | Manifiesto de dependencias y versiones runtime del proyecto. | `fastapi`, `langchain`, `uvicorn` |

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
                           app/prompts/templates.py
                           (plantillas base de prompts)
                                      |
                                      v
                           LangChain/Ollama (ejecución LLM)
                                      |
                                      v
                              Respuesta JSON al cliente
```




