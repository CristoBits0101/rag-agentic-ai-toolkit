# FastAPI

## Comandos de configuración y ejecución

```bash
# Configuración de Git para evitar problemas de saltos de línea.
git config --global core.autocrlf input
```

```bash
# Crear entorno virtual.
python3 -m venv venv
```

```bash
# Activar entorno en Windows PowerShell.
.\venv\Scripts\Activate.ps1
```

```bash
# Instalar dependencias.
pip install fastapi uvicorn[standard] gunicorn pydantic-settings
```

```bash
# Generar requirements.txt.
pip freeze > requirements.txt
```

```bash
# Ejecutar servidor en desarrollo.
uvicorn main:app --reload
```

## Formateo de código

> Black Formatter

