# COMANDOS

## Instalacion de dependencias

```bash
# 1) Crear entorno virtual.
python -m venv .venv

# 2) Activar entorno.
.\.venv\Scripts\Activate.ps1

# 3) Actualizar pip.
python -m pip install --upgrade pip

# 4) Instalar todo desde requirements.txt.
pip install -r requirements.txt
```

## Instalacion paquetes individuales

```bash
pip install fastapi==0.134.0
pip install "uvicorn[standard]==0.41.0"
pip install gunicorn==25.1.0
pip install pydantic-settings==2.13.1
pip install langchain==0.3.27
pip install langchain-core==0.3.80
pip install langchain-ollama==0.3.10
pip install python-dotenv==1.2.1
pip install PyYAML==6.0.3
```

## Ollama

```bash
# Instalar Ollama.
irm https://ollama.com/install.ps1 | iex

# Descargar un modelo local de ejemplo.
ollama pull llama3.2:3b

# Verificar.
ollama --version
ollama list
```

## Comandos utiles despues de instalar

```bash
# Instalar el proyecto en modo editable.
pip install -e .

# Ejecutar API en desarrollo.
PYTHONPATH=src uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Guardar lock simple de dependencias.
pip freeze > requirements.txt
```

## Rutas de API

| Metodo | Ruta | Descripcion |
| --- | --- | --- |
| GET | `/api/v1/agent/` | Endpoint de prueba del modulo de agentes. |
| GET | `/api/v1/chat/` | Endpoint de prueba del modulo de chat. |
| GET | `/api/v1/health/` | Health check de la API versionada v1. |
| GET | `/api/v1/llm/` | Endpoint de prueba del modulo LLM. |
| GET | `/api/v1/prompt/` | Health check del servicio de prompts. |
| POST | `/api/v1/prompt/exercise-1/completion` | Ejecuta el ejercicio 1 de prompts. |
| POST | `/api/v1/prompt/exercise-2/task-prompts` | Ejecuta el ejercicio 2 de prompts. |
| POST | `/api/v1/prompt/exercise-3/step-by-step` | Ejecuta el ejercicio 3 de prompts. |
| POST | `/api/v1/prompt/exercise-4/lcel` | Ejecuta el ejercicio 4 de prompts. |
| POST | `/api/v1/prompt/exercise-5/reasoning-reviews` | Ejecuta el ejercicio 5 de prompts. |
| GET | `/api/v1/rag/` | Endpoint de prueba del modulo de retrieval RAG. |
| GET | `/health` | Health check general de la aplicacion. |
