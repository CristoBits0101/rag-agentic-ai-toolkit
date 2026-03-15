# Practica 13 Story Generator And Text To Speech

## Leyenda

1. Story generation: Prompt guiado para crear una historia educativa para principiantes.
2. Demo model local: Generacion determinista que reemplaza la llamada remota a watsonx.
3. Text to speech: Sintesis de audio con una salida local estable y soporte opcional para `gTTS`.
4. Audio export: Guardado del artefacto de audio para inspeccion o reproduccion posterior.

## Adaptacion

Esta practica toma el laboratorio de generacion de historias y texto a voz y lo adapta al repositorio sin depender de watsonx.ai ni de servicios remotos para la ejecucion normal. La historia se genera con un modelo de demostracion local y el audio usa una salida `WAV` determinista para mantener la practica estable. Si el usuario instala `gTTS` y lo habilita de forma explicita la practica tambien puede producir un `MP3`.

## Roles de Archivos

- `main.py`: Punto de entrada de la practica.
- `config/story_tts_config.py`: Temas por defecto y parametros del audio.
- `models/story_demo_model.py`: Generador local de historias educativas.
- `models/story_audio_gateway.py`: Sintesis de audio con fallback local y guardado de archivos.
- `orchestration/story_generation_orchestration.py`: Construccion del prompt y generacion de la historia.
- `orchestration/story_audio_orchestration.py`: Creacion del artefacto de audio y exportacion.
- `orchestration/story_tts_lab_runner.py`: Ejecucion guiada del laboratorio.

## Instalacion

1. Activar entorno: `.\venv\Scripts\Activate.ps1`.
2. Dependencias obligatorias: Ninguna adicional a Python estandar.
3. Dependencia opcional para `MP3`: `pip install -U gTTS`.

## Verificacion

1. Compilacion: `python -m compileall spikes\13-story_generator_text_to_speech_lab`.
2. Practica: `.\venv\Scripts\python.exe .\spikes\13-story_generator_text_to_speech_lab\main.py`.
3. Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_13_story_generator_text_to_speech.py`.

## Cobertura

1. `create_story_prompt`: Construccion del prompt educativo.
2. `generate_story`: Generacion de una historia para un tema dado.
3. `synthesize_story_audio`: Creacion del audio del relato.
4. `save_generated_story_audio`: Exportacion del audio a un archivo local.
5. Ejercicio incluido: Nuevo tema con `the life cycle of a human`.
