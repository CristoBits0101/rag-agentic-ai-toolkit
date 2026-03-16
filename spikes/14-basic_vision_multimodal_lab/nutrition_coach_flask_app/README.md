# Nutrition Coach Flask App

Esta extension de la practica 14 adapta el laboratorio de nutricion visual a una app `Flask`.
Combina una imagen de comida subida por el usuario con retrieval local sobre un mini catalogo nutricional y un modelo real de vision en `Ollama`.

## Modelos Soportados

1. `llama3.2-vision`.
2. `llava`.
3. `qwen2.5vl:3b`.

## Flujo

1. Se generan ejemplos locales de platos.
2. La imagen subida se codifica a `Base64` y embedding visual.
3. Se recupera la comida mas cercana en un dataset estructurado.
4. El contexto nutricional recuperado se pasa a un modelo de vision en `Ollama`.
5. Si el modelo no responde la app usa un fallback determinista con el catalogo local.

## Ejecucion

1. Activar entorno: `.\venv\Scripts\Activate.ps1`.
2. Instalar dependencias del caso de uso: `pip install -U flask pillow numpy`.
3. Arrancar `Ollama`: `ollama serve`.
4. Descargar un modelo: `ollama pull llama3.2-vision`.
5. Ejecutar runner de consola: `.\venv\Scripts\python.exe .\spikes\14-basic_vision_multimodal_lab\nutrition_coach_flask_app\main.py`.
6. Tras validar compilacion y tests puedes lanzar la app web: `.\venv\Scripts\python.exe .\spikes\14-basic_vision_multimodal_lab\nutrition_coach_flask_app\app.py`.

## Dependencias

1. Base del flujo: `flask` `pillow` y `numpy`.
2. Backend visual opcional mas cercano al laboratorio original: `pip install torch torchvision`.
3. Modelos reales de vision: `llama3.2-vision` `llava` o `qwen2.5vl:3b` en `Ollama`.

## Interfaz

La app usa `templates/index.html` y `static/style.css`.
Los ejemplos visuales se crean automaticamente en `static/examples`.
