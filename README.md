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
