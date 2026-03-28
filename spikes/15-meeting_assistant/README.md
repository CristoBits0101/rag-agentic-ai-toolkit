# Practica 15 AI Meeting Assistant

## Leyenda

1. Speech to text: Convierte audio de reunion en una transcripcion usable.
2. Transcript cleanup: Normaliza terminos financieros y corrige formatos frecuentes.
3. Prompt template and chain: Genera acta de reunion y lista de tareas desde el transcript ajustado.
4. Gradio app: Expone el flujo completo con entrada de audio y descarga del resultado.
5. Adaptacion local: Evita depender de watsonx para la ejecucion normal del repositorio.

## Adaptacion

Esta practica adapta el laboratorio original a una version local y reproducible del repositorio. `Whisper` no se sustituye por `Ollama` porque son componentes de naturaleza distinta. La transcripcion puede ejecutarse con `Whisper` local o apoyarse en el audio de muestra del spike para pruebas controladas. La generacion de actas y tareas usa un modelo real de texto en `Ollama`.

## Roles de Archivos

- `main.py`: Punto de entrada de la practica.
- `config/meeting_assistant_config.py`: Parametros del spike y nombres de archivos.
- `data/meeting_transcript_catalog.py`: Transcript local de muestra para la reunion de ejemplo.
- `models/meeting_assistant_llm_gateway.py`: Acceso al modelo real de `Ollama`.
- `orchestration/meeting_transcription_orchestration.py`: Transcripcion con `Whisper` opcional o catalogo local.
- `orchestration/meeting_cleanup_orchestration.py`: Ajuste del transcript y extraccion del bloque corregido.
- `orchestration/meeting_minutes_orchestration.py`: Prompt template chain y escritura del reporte final.
- `orchestration/meeting_assistant_orchestration.py`: Flujo completo de audio a acta.
- `orchestration/meeting_assistant_lab_runner.py`: Ejecucion guiada del laboratorio.
- `ui/meeting_assistant_ui.py`: Interfaz `Gradio` para ejecutar el asistente.

## Instalacion

1. Activar entorno: `.\venv\Scripts\Activate.ps1`.
2. Dependencias ya cubiertas por el repo: `gradio` `langchain-core` y `langchain-ollama`.
3. Dependencia opcional para `Whisper`: `pip install -U transformers torch`.
4. Arrancar `Ollama`: `ollama serve`.
5. Modelo de texto: `ollama pull llama3.2:3b`.

## Verificacion

1. Compilacion: `python -m compileall spikes\15-meeting_assistant`.
2. Practica: `.\venv\Scripts\python.exe .\spikes\15-meeting_assistant\main.py`.
3. Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_15_meeting_assistant.py`.

## Cobertura

1. `remove_non_ascii`: Limpieza base del transcript.
2. `transcribe_audio_source`: Transcripcion con `Whisper` o con el audio de ejemplo del spike.
3. `product_assistant`: Normalizacion de terminos financieros.
4. `generate_meeting_minutes`: Generacion de acta y tareas.
5. `transcript_audio`: Flujo completo con escritura de archivo descargable.
