# Ollama Mistral Story TTS

Esta variante ejecuta la practica 13 con un `LLM` real servido por `Ollama` usando el modelo `mistral`. La salida de audio intenta usar `gTTS` si esta disponible. Si no lo esta guarda un `WAV` local de demostracion para mantener la ejecucion estable.

## Requisitos

1. Instalar `Ollama`.
2. Ejecutar `ollama serve`.
3. Descargar el modelo: `ollama pull mistral`.
4. Dependencia opcional para `MP3`: `pip install -U gTTS`.

## Ejecucion

```powershell
.\venv\Scripts\python.exe .\spikes\13-story_generator_text_to_speech_lab\ollama_mistral_story_tts\main.py
```
