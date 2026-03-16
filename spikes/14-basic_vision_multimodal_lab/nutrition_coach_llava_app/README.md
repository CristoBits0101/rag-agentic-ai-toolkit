# Nutrition Coach with llava

Esta variante ejecuta la extension `Nutrition Coach` con `llava` en `Ollama`.

## Ejecucion

1. Activar entorno: `.\venv\Scripts\Activate.ps1`.
2. Arrancar `Ollama`: `ollama serve`.
3. Descargar modelo: `ollama pull llava`.
4. Ejecutar runner: `.\venv\Scripts\python.exe .\spikes\14-basic_vision_multimodal_lab\nutrition_coach_llava_app\main.py`.
5. Para lanzar la interfaz Flask tras validar tests y compilacion: `.\venv\Scripts\python.exe .\spikes\14-basic_vision_multimodal_lab\nutrition_coach_flask_app\app.py`.
