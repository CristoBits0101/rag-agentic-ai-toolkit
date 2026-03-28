# Qwen2.5VL Vision Querying

Esta variante ejecuta la practica 14 con un modelo de vision real en `Ollama` usando `qwen2.5vl:3b`. Usa una imagen local de una etiqueta nutricional y hace una consulta orientada a OCR ligero para leer el sodio visible.

## Requisitos

1. Instalar `Ollama`.
2. Ejecutar `ollama serve`.
3. Descargar el modelo: `ollama pull qwen2.5vl:3b`.

## Ejecucion

```powershell
.\venv\Scripts\python.exe .\spikes\14-vision_multimodal\qwen2_5vl_vision_querying\main.py
```
