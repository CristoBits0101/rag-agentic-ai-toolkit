# Practica 17 Voice Desktop Assistant

## Leyenda

1. Push to talk: Captura audio desde el micro mientras mantienes un boton o la barra espaciadora con foco local.
2. Speech to text local: Transcribe la orden con `Whisper` en local.
3. Command planner: Interpreta la intencion con `Ollama` usando un plan JSON validado.
4. Desktop actions: Ejecuta una allowlist de acciones de escritorio incluyendo apertura y cierre controlado de apps.
5. Confirmation gate: Pide confirmacion antes de enviar rutas a la papelera.

## Justificacion

Esta practica no es una extension menor de la practica 15. La practica 15 trabaja audio subido por archivo y generacion de actas. Esta practica introduce micro en tiempo real push to talk permisos de seguridad y automatizacion local del sistema operativo. Por eso queda separada como spike propio.

## Roles de Archivos

- `main.py`: Punto de entrada de la practica.
- `config/voice_desktop_config.py`: Parametros del spike audio modelos y reglas de seguridad.
- `data/voice_command_catalog.py`: Allowlist de acciones aplicaciones urls y alias.
- `models/voice_desktop_entities.py`: Dataclasses para planes y resultados.
- `models/voice_microphone_gateway.py`: Captura de audio con push to talk manual y guardado a WAV.
- `models/voice_transcription_gateway.py`: Transcripcion local con `Whisper`.
- `models/voice_agent_ollama_gateway.py`: Planner principal con `Ollama` y seleccion automatica del mejor modelo local disponible.
- `models/voice_local_tts_gateway.py`: Respuesta hablada local con `System.Speech` de Windows.
- `orchestration/voice_desktop_planning_orchestration.py`: Validacion y normalizacion del plan generado por `Ollama`.
- `orchestration/voice_desktop_execution_orchestration.py`: Ejecutor seguro de acciones locales.
- `orchestration/voice_desktop_session_orchestration.py`: Flujo de turnos y confirmaciones por voz.
- `orchestration/voice_desktop_lab_runner.py`: Loop principal del asistente.
- `ui/voice_desktop_ui.py`: Ventana nativa con boton push to talk respuesta por voz y soporte de barra espaciadora con foco local.

## Instalacion

1. Activar entorno: `.\venv\Scripts\Activate.ps1`.
2. Dependencias para voz y automatizacion: `pip install -U transformers torch sounddevice pyautogui Send2Trash`.
3. Arrancar `Ollama`: `ollama serve`.
4. Modelo recomendado de texto: `ollama pull qwen2.5:7b`.
5. Modelo compatible de menor consumo: `ollama pull llama3.2:3b`.
6. Dependencia opcional para el runner de consola legado: `pip install -U keyboard`.
7. La respuesta por voz usa `System.Speech` local de Windows y no necesita red.
8. Conectar un micro funcional antes de ejecutar la practica.
9. `ffmpeg` no es necesario para el flujo normal de esta practica porque el audio `WAV` del micro se carga de forma nativa.

## Funcionamiento

1. La practica abre una ventana nativa de escritorio sin navegador.
2. Mantienes pulsado el boton principal o la barra espaciadora con la ventana enfocada para hablar.
3. `Whisper` transcribe la orden.
4. `Ollama` intenta planificar una accion segura.
5. Si `Ollama` no responde o devuelve una accion no valida el flujo se detiene con un error explicito.
6. Las acciones permitidas son abrir apps cerrar apps permitidas abrir urls escribir texto pulsar atajos y enviar rutas a la papelera.
7. `close_application` y `trash_path` siempre piden confirmacion.
8. `trash_path` bloquea rutas del repo y rutas sensibles del sistema.
9. La ventana incluye botones de `Confirmar` y `Cancelar` para resolver acciones sensibles sin depender de una segunda orden de voz.
10. La ventana puede responder por voz y detiene la locucion activa cuando vuelves a hablar.
11. Si `taskkill` devuelve ruido por procesos secundarios pero la app objetivo ya no sigue viva el asistente da el cierre por correcto.
12. Si la app fue abierta con mas privilegios que el asistente el cierre puede fallar con acceso denegado y la interfaz lo indicara de forma explicita.
13. El bloque de estado muestra solo un resumen en una linea de la ultima accion mientras que el historial conserva el detalle completo.

## Verificacion

1. Compilacion: `python -m compileall src spikes\17-voice_desktop_assistant_lab`.
2. Practica: `.\venv\Scripts\python.exe .\spikes\17-voice_desktop_assistant_lab\main.py`.
3. Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_17_voice_desktop_assistant.py`.

## Cobertura

1. `select_best_available_ollama_model`: Elige el mejor modelo de texto ya instalado en `Ollama`.
2. `process_voice_transcript`: Maneja confirmaciones por voz.
4. `trash_path`: Mueve rutas a la papelera y rechaza rutas protegidas.
5. `write_pcm_frames_to_wav`: Genera el artefacto WAV desde frames PCM.
6. `LocalVoiceSpeaker`: Reproduce voz local y corta la respuesta previa antes de iniciar una nueva.
7. `close_application`: Cierra aplicaciones permitidas mediante `taskkill` tras confirmacion explicita.
