# Nutrition Coach with llama3.2 vision

Esta variante ejecuta la extension `Nutrition Coach` con `llama3.2-vision` en `Ollama`.

## Ejecucion

1. Activar entorno: `.\venv\Scripts\Activate.ps1`.
2. Arrancar `Ollama`: `ollama serve`.
3. Descargar modelo: `ollama pull llama3.2-vision`.
4. Ejecutar runner: `.\venv\Scripts\python.exe .\spikes\14-vision_multimodal\nutrition_coach_llama3_2_vision_app\main.py`.
5. Para lanzar la interfaz Flask tras validar tests y compilacion: `.\venv\Scripts\python.exe .\spikes\14-vision_multimodal\nutrition_coach_flask_app\app.py`.
