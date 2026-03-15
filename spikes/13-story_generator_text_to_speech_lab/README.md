# Practica 13 Story Generator And Text To Speech

## Leyenda

1. Story generation: Prompt guiado para crear una historia educativa para principiantes.
2. Demo model local: Generacion determinista que reemplaza la llamada remota a watsonx.
3. Text to speech: Sintesis de audio con una salida local estable y soporte opcional para `gTTS`.
4. Audio export: Guardado del artefacto de audio para inspeccion o reproduccion posterior.
5. Variantes reales: Ejemplos adicionales con `Ollama` `Mistral API` y `edge-tts`.

## Adaptacion

Esta practica toma el laboratorio de generacion de historias y texto a voz y lo adapta al repositorio sin depender de watsonx.ai ni de servicios remotos para la ejecucion normal. La historia se genera con un modelo de demostracion local y el audio usa una salida `WAV` determinista para mantener la practica estable. Si el usuario instala `gTTS` y lo habilita de forma explicita la practica tambien puede producir un `MP3`.

La practica base se mantiene local para estabilidad y tests. Ademas incluye tres variantes reales pensadas para ejecutar la misma idea con un `LLM` real sin `watsonx`: `ollama_mistral_story_tts` `mistral_api_story_tts` y `ollama_mistral_edge_tts_story_tts`.

## Roles de Archivos

- `main.py`: Punto de entrada de la practica.
- `config/story_tts_config.py`: Temas por defecto y parametros del audio.
- `models/story_demo_model.py`: Generador local de historias educativas.
- `models/story_ollama_mistral_gateway.py`: Acceso al modelo `mistral` servido por `Ollama`.
- `models/story_mistral_api_gateway.py`: Acceso directo a `Mistral API`.
- `models/story_edge_tts_gateway.py`: Sintesis de audio con `edge-tts`.
- `models/story_audio_gateway.py`: Sintesis de audio con fallback local y guardado de archivos.
- `orchestration/story_generation_orchestration.py`: Construccion del prompt y generacion de la historia.
- `orchestration/story_audio_orchestration.py`: Creacion del artefacto de audio y exportacion.
- `orchestration/story_real_variants_orchestration.py`: Flujo compartido para las variantes reales.
- `orchestration/story_tts_lab_runner.py`: Ejecucion guiada del laboratorio.
- `ollama_mistral_story_tts`: Variante real con `Ollama` y `mistral`.
- `mistral_api_story_tts`: Variante real con `Mistral API`.
- `ollama_mistral_edge_tts_story_tts`: Variante real con `Ollama` y `edge-tts`.

## Instalacion

1. Activar entorno: `.\venv\Scripts\Activate.ps1`.
2. Dependencias obligatorias: Ninguna adicional a Python estandar.
3. Dependencia opcional para `MP3`: `pip install -U gTTS`.
4. Variante real con `Ollama`: `ollama serve` y `ollama pull mistral`.
5. Variante real con `Mistral API`: exportar `MISTRAL_API_KEY`.
6. Variante real gratuita para `Text to Speech`: `pip install -U edge-tts`.

## Verificacion

1. Compilacion: `python -m compileall spikes\13-story_generator_text_to_speech_lab`.
2. Practica: `.\venv\Scripts\python.exe .\spikes\13-story_generator_text_to_speech_lab\main.py`.
3. Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_13_story_generator_text_to_speech.py`.
4. Variante `Ollama`: `.\venv\Scripts\python.exe .\spikes\13-story_generator_text_to_speech_lab\ollama_mistral_story_tts\main.py`.
5. Variante `Mistral API`: `.\venv\Scripts\python.exe .\spikes\13-story_generator_text_to_speech_lab\mistral_api_story_tts\main.py`.
6. Variante `edge-tts`: `.\venv\Scripts\python.exe .\spikes\13-story_generator_text_to_speech_lab\ollama_mistral_edge_tts_story_tts\main.py`.

## Cobertura

1. `create_story_prompt`: Construccion del prompt educativo.
2. `generate_story`: Generacion de una historia para un tema dado.
3. `synthesize_story_audio`: Creacion del audio del relato.
4. `save_generated_story_audio`: Exportacion del audio a un archivo local.
5. Ejercicio incluido: Nuevo tema con `the life cycle of a human`.
6. Variante real `Ollama`: Historia con `mistral` local.
7. Variante real `Mistral API`: Historia con `mistral-small-latest`.
8. Variante real `edge-tts`: Voz sintetizada gratuita para la historia generada.
