# Mistral API Story TTS

Esta variante ejecuta la practica 13 con un `LLM` real de `Mistral` por API usando el modelo `mistral-small-latest`. La salida de audio intenta usar `gTTS` si esta disponible. Si no lo esta guarda un `WAV` local de demostracion.

## Requisitos

1. Exportar la variable `MISTRAL_API_KEY`.
2. Tener acceso a la API de `Mistral`.
3. Dependencia opcional para `MP3`: `pip install -U gTTS`.

## Ejecucion

```powershell
$env:MISTRAL_API_KEY = "tu_api_key"
.\venv\Scripts\python.exe .\spikes\13-story_generator_text_to_speech_lab\mistral_api_story_tts\main.py
```
