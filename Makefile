# ==============================
# FastAPI RAG Agent Toolkit
# ==============================

APP=app.main:app
HOST=0.0.0.0
PORT=8000

# Instalar dependencias
install:
	pip install -r requirements.txt

# Ejecutar en desarrollo
run:
	uvicorn $(APP) --reload --host $(HOST) --port $(PORT)

# Ejecutar en modo producción (Linux recomendado)
prod:
	gunicorn $(APP) -k uvicorn.workers.UvicornWorker -b $(HOST):$(PORT)

# Formatear código (si instalas black)
format:
	black .

# Ejecutar tests (si usas pytest)
test:
	pytest

# Limpiar cache
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +