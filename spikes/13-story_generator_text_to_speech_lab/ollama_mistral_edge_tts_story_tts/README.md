# Ollama Mistral Edge TTS Story TTS

Esta variante ejecuta la practica 13 con un `LLM` real en `Ollama` usando `mistral` y sintetiza la voz con `edge-tts`. `edge-tts` es una opcion gratuita y real para `Text to Speech` accesible desde internet sin depender de `watsonx`.

## Requisitos

1. Instalar `Ollama`.
2. Ejecutar `ollama serve`.
3. Descargar el modelo: `ollama pull mistral`.
4. Instalar `edge-tts`: `pip install -U edge-tts`.

## Ejecucion

```powershell
.\venv\Scripts\python.exe .\spikes\13-story_generator_text_to_speech_lab\ollama_mistral_edge_tts_story_tts\main.py
```
