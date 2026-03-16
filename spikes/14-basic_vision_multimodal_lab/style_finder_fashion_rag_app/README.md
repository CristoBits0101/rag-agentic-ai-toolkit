# Style Finder Fashion RAG App

Esta extension avanzada de la practica 14 monta una app completa de analisis de moda con `Gradio`.
Combina codificacion de imagen retrieval por similitud sobre un dataset estructurado y respuesta generada por un modelo real de vision en `Ollama`.

## Modelos Soportados

1. `llama3.2-vision`.
2. `llava`.
3. `qwen2.5vl:3b`.

## Flujo

1. Se generan ejemplos locales de outfits.
2. La imagen se convierte a `Base64` y vector visual.
3. Se recupera el look mas cercano en un dataset local.
4. Se obtienen items relacionados y alternativas por categoria.
5. Un modelo de vision genera un analisis de estilo con contexto aumentado.

## Ejecucion

1. Activar entorno: `.\venv\Scripts\Activate.ps1`.
2. Arrancar `Ollama`: `ollama serve`.
3. Descargar un modelo: `ollama pull llama3.2-vision`.
4. Ejecutar runner: `.\venv\Scripts\python.exe .\spikes\14-basic_vision_multimodal_lab\style_finder_fashion_rag_app\main.py`.

## Dependencias

1. Backend visual por defecto: `pillow` y `numpy`.
2. Backend opcional mas cercano al laboratorio original: `pip install torch torchvision`.
3. UI incluida: `gradio`.

## Interfaz

La extension incluye una UI en `ui/style_finder_ui.py`.
No se arranca automaticamente desde `main.py` para respetar la politica del repositorio de validar antes de lanzar servidores.
