# Nutrition Coach with qwen2.5vl

Esta variante ejecuta la extension `Nutrition Coach` con `qwen2.5vl:3b` en `Ollama`.

## Ejecucion

1. Activar entorno: `.\venv\Scripts\Activate.ps1`.
2. Arrancar `Ollama`: `ollama serve`.
3. Descargar modelo: `ollama pull qwen2.5vl:3b`.
4. Ejecutar runner: `.\venv\Scripts\python.exe .\spikes\14-basic_vision_multimodal_lab\nutrition_coach_qwen2_5vl_app\main.py`.
5. Para lanzar la interfaz Flask tras validar tests y compilacion: `.\venv\Scripts\python.exe .\spikes\14-basic_vision_multimodal_lab\nutrition_coach_flask_app\app.py`.
