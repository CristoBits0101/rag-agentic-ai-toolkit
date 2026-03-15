# Practica 15 AI Meeting Assistant

## Leyenda

1. Speech to text: Convierte audio de reunion en una transcripcion usable.
2. Transcript cleanup: Normaliza terminos financieros y corrige formatos frecuentes.
3. Prompt template and chain: Genera acta de reunion y lista de tareas desde el transcript ajustado.
4. Gradio app: Expone el flujo completo con entrada de audio y descarga del resultado.
5. Adaptacion local: Evita depender de watsonx para la ejecucion normal del repositorio.

## Adaptacion

Esta practica adapta el laboratorio original a una version local y reproducible del repositorio. `Whisper` no se sustituye por `Ollama` porque son componentes de naturaleza distinta. Para transcripcion el spike intenta usar `Whisper` mediante `transformers` si esa dependencia esta instalada. Si no lo esta usa un transcript local de demostracion para mantener estabilidad en tests. Para la generacion de actas y tareas el flujo usa un `DemoLLM` local y deja `Ollama` como opcion gratuita y compatible para quien quiera probar un modelo real de texto.

## Roles de Archivos

- `main.py`: Punto de entrada de la practica.
- `config/meeting_assistant_config.py`: Parametros del spike y nombres de archivos.
- `data/meeting_transcript_catalog.py`: Transcript local de muestra para la reunion demo.
- `models/meeting_assistant_demo_llm.py`: Modelo local para limpieza financiera y actas.
- `models/meeting_assistant_llm_gateway.py`: Seleccion entre `Ollama` y `DemoLLM`.
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

## Verificacion

1. Compilacion: `python -m compileall spikes\15-ai_meeting_assistant_lab`.
2. Practica: `.\venv\Scripts\python.exe .\spikes\15-ai_meeting_assistant_lab\main.py`.
3. Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_15_ai_meeting_assistant.py`.

## Cobertura

1. `remove_non_ascii`: Limpieza base del transcript.
2. `transcribe_audio_source`: Transcripcion por catalogo local o `Whisper` opcional.
3. `product_assistant`: Normalizacion de terminos financieros.
4. `generate_meeting_minutes`: Generacion de acta y tareas.
5. `transcript_audio`: Flujo completo con escritura de archivo descargable.
