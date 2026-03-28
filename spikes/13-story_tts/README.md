# Practica 13 Story Generator And Text To Speech

## Leyenda

1. Story generation: Prompt guiado para crear una historia educativa para principiantes.
2. Story generation con Ollama: Generacion de historia con un `LLM` real local.
3. Text to speech: Sintesis de audio gratuita con `edge-tts` y soporte adicional para `gTTS`.
4. Audio export: Guardado del artefacto de audio para inspeccion o reproduccion posterior.
5. Variantes reales: Ejemplos adicionales con `Ollama` `Mistral API` y `edge-tts`.

## Adaptacion

Esta practica toma el laboratorio de generacion de historias y texto a voz y lo adapta al repositorio sin depender de watsonx.ai. La ejecucion principal usa un `LLM` real en `Ollama` y sintetiza audio con `edge-tts` para mantener el objetivo tecnico del laboratorio con servicios locales o gratuitos.

Ademas incluye variantes extra para el mismo flujo. `Mistral API` queda como proveedor alternativo y `gTTS` como opcion adicional de audio cuando interese comparar otro servicio.

## Roles de Archivos

- `main.py`: Punto de entrada de la practica.
- `config/story_tts_config.py`: Temas por defecto y parametros del audio.
- `models/story_ollama_mistral_gateway.py`: Acceso al modelo configurado en `Ollama` para generar la historia.
- `models/story_mistral_api_gateway.py`: Acceso directo a `Mistral API`.
- `models/story_edge_tts_gateway.py`: Sintesis de audio con `edge-tts`.
- `models/story_audio_gateway.py`: Guardado de artefactos de audio y soporte adicional para `gTTS`.
- `orchestration/story_generation_orchestration.py`: Construccion del prompt y generacion de la historia.
- `orchestration/story_audio_orchestration.py`: Creacion del artefacto de audio y exportacion.
- `orchestration/story_real_variants_orchestration.py`: Flujo compartido para las variantes reales.
- `orchestration/story_tts_lab_runner.py`: Ejecucion guiada del laboratorio.
- `ollama_mistral_story_tts`: Variante real con `Ollama` y `mistral`.
- `mistral_api_story_tts`: Variante real con `Mistral API`.
- `ollama_mistral_edge_tts_story_tts`: Variante real con `Ollama` y `edge-tts`.

## Instalacion

1. Activar entorno: `.\venv\Scripts\Activate.ps1`.
2. LangChain Ollama: `pip install -U langchain-ollama`.
3. Arrancar `Ollama`: `ollama serve`.
4. Modelo de texto recomendado: `ollama pull qwen2.5:7b`.
5. Voz gratuita: `pip install -U edge-tts`.
6. Opcion adicional de audio: `pip install -U gTTS`.
7. Variante real con `Mistral API`: exportar `MISTRAL_API_KEY`.

## Verificacion

1. Compilacion: `python -m compileall spikes\13-story_tts`.
2. Practica: `.\venv\Scripts\python.exe .\spikes\13-story_tts\main.py`.
3. Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_13_story_tts.py`.
4. Variante `Ollama` con audio por `gTTS`: `.\venv\Scripts\python.exe .\spikes\13-story_tts\ollama_mistral_story_tts\main.py`.
5. Variante `Mistral API`: `.\venv\Scripts\python.exe .\spikes\13-story_tts\mistral_api_story_tts\main.py`.
6. Variante `edge-tts`: `.\venv\Scripts\python.exe .\spikes\13-story_tts\ollama_mistral_edge_tts_story_tts\main.py`.

## Cobertura

1. `create_story_prompt`: Construccion del prompt educativo.
2. `generate_story`: Generacion de una historia para un tema dado.
3. `synthesize_story_audio`: Creacion del audio del relato.
4. `save_generated_story_audio`: Exportacion del audio a un archivo local.
5. Ejercicio incluido: Nuevo tema con `the life cycle of a human`.
6. Variante real `Ollama`: Historia con el modelo configurado en `Ollama`.
7. Variante real `Mistral API`: Historia con `mistral-small-latest`.
8. Variante real `edge-tts`: Voz sintetizada gratuita para la historia generada.
