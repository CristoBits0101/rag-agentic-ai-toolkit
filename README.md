# FastAPI

## Comandos

```bash
# Configuración de Git para evitar problemas de saltos de línea.
git config --global core.autocrlf input

# Crear entorno virtual.
python3 -m venv venv

# Activar entorno en Windows PowerShell.
.\venv\Scripts\Activate.ps1

# Instalar dependencias.
pip install fastapi uvicorn[standard] gunicorn pydantic-settings

# Generar requirements.txt.
pip freeze > requirements.txt

# Ejecutar servidor en desarrollo.
uvicorn main:app --reload
