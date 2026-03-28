# Practica 17 Voice Desktop Assistant

## Leyenda

1. Voice channel toggle: Abre o cierra el canal de voz con un boton corto o con la barra espaciadora y muestra una bombilla roja o verde segun el estado.
2. Speech to text local: Transcribe la orden con `Whisper` en local.
3. Command planner: Interpreta la intencion con `Ollama` usando un plan JSON validado.
4. Desktop actions: Ejecuta una allowlist de acciones de escritorio incluyendo apertura y cierre controlado de apps movimiento de raton click de raton y click visual sobre objetivos permitidos.
5. Confirmation gate: Pide confirmacion antes de enviar rutas a la papelera.

## Justificacion

Esta practica no es una extension menor de la practica 15. La practica 15 trabaja audio subido por archivo y generacion de actas. Esta practica introduce micro en tiempo real canal de voz local permisos de seguridad y automatizacion local del sistema operativo. Por eso queda separada como spike propio.

## Roles de Archivos

- `main.py`: Punto de entrada de la practica.
- `config/voice_desktop_config.py`: Parametros del spike audio modelos y reglas de seguridad.
- `data/voice_command_catalog.py`: Allowlist de acciones aplicaciones urls alias y objetivos de click.
- `models/voice_desktop_entities.py`: Dataclasses para planes y resultados.
- `models/voice_microphone_gateway.py`: Captura de audio local y guardado a WAV.
- `models/voice_transcription_gateway.py`: Transcripcion local con `Whisper`.
- `models/voice_agent_ollama_gateway.py`: Planner principal con `Ollama` y seleccion automatica del mejor modelo local disponible.
- `models/voice_local_tts_gateway.py`: Respuesta hablada local con `System.Speech` de Windows.
- `orchestration/voice_desktop_planning_orchestration.py`: Validacion y normalizacion del plan generado por `Ollama`.
- `orchestration/voice_desktop_execution_orchestration.py`: Ejecutor seguro de acciones locales.
- `models/voice_screen_vision_gateway.py`: Localizacion de objetivos sobre capturas de pantalla con `qwen3-vl`.
- `orchestration/voice_desktop_session_orchestration.py`: Flujo de turnos y confirmaciones por voz.
- `orchestration/voice_desktop_lab_runner.py`: Loop principal del asistente.
- `ui/voice_desktop_ui.py`: Ventana nativa con canal de voz abierto o cerrado bombilla roja o verde respuesta por voz soporte de barra espaciadora como toggle y envio de mensajes escritos.

## Instalacion

1. Activar entorno: `.\venv\Scripts\Activate.ps1`.
2. Dependencias para voz y automatizacion: `pip install -U transformers torch sounddevice pyautogui Send2Trash`.
3. Arrancar `Ollama`: `ollama serve`.
4. Modelo recomendado para control de escritorio: `ollama pull qwen3-vl:30b`.
5. Modelo compatible de menor consumo: `ollama pull qwen3-vl:8b`.
6. Dependencia opcional para el runner de consola legado: `pip install -U keyboard`.
7. La transcripcion local usa `openai/whisper-small` forzada a espanol para mejorar el reconocimiento de comandos de voz del escritorio.
8. La respuesta por voz usa `System.Speech` local de Windows y no necesita red.
9. Conectar un micro funcional antes de ejecutar la practica.
10. `ffmpeg` no es necesario para el flujo normal de esta practica porque el audio `WAV` del micro se carga de forma nativa.
11. Las plantillas visuales son opcionales y se usan como primer intento rapido antes del fallback con vision sobre la pantalla actual.
12. El flujo actual usa `qwen3-vl:30b` como planner por defecto y tambien como modelo de vision para localizar objetivos en pantalla.
13. Las ordenes directas de escritorio mas claras como `dale a jugar en league of legends` se resuelven primero con reglas locales para reducir fallos del planner.

## Funcionamiento

1. La practica abre una ventana nativa de escritorio sin navegador.
2. Abres o cierras el canal de voz con el boton principal o con la barra espaciadora.
3. Cuando el canal esta abierto la bombilla circular se muestra en verde y cuando esta cerrado se muestra en rojo.
4. Mientras el canal esta abierto la app escucha de forma continua y procesa cada orden detectada sin tener que volver a cerrarlo para cada frase.
5. Debajo de `Estado` puedes escribir un mensaje y enviarlo sin usar el micro.
6. `Whisper` transcribe cada orden capturada.
7. `Ollama` intenta planificar una accion segura.
8. Si `Ollama` no responde o devuelve una accion no valida el flujo se detiene con un error explicito.
9. Las acciones permitidas son abrir apps abrir urls escribir texto mover el raton hacer click con el raton pulsar atajos hacer click en objetivos visuales permitidos cerrar apps permitidas y enviar rutas a la papelera.
10. `close_application` y `trash_path` siempre piden confirmacion.
11. `trash_path` bloquea rutas del repo y rutas sensibles del sistema.
12. La ventana incluye botones de `Confirmar` y `Cancelar` para resolver acciones sensibles sin depender de una segunda orden de voz.
13. La ventana puede responder por voz y detiene la locucion activa cuando vuelves a hablar.
14. Si `taskkill` devuelve ruido por procesos secundarios pero la app objetivo ya no sigue viva el asistente da el cierre por correcto.
15. Si la app fue abierta con mas privilegios que el asistente el cierre puede fallar con acceso denegado y la interfaz lo indicara de forma explicita.
16. El bloque de estado muestra solo un resumen en una linea de la ultima accion mientras que el historial conserva el detalle completo.
17. Si dices `abre league of legends` el asistente abre `Riot Client` y primero intenta pulsar `riot_play_button` si ya esta en la pagina de LoL y si no prueba `riot_lol_icon` y despues `riot_play_button`.
18. Si dices `cierra el lol` el asistente acepta tanto procesos del cliente de League como procesos activos de `Riot Client` cuando League esta abierto desde ese lanzador.
19. Si dices `dale a jugar al lol` el asistente intenta primero el boton amarillo `riot_play_button` y si no esta visible cae al boton azul `league_play_button`.
20. Si dices `dale a jugar en league of legends` o una variante cercana como `dale a jugar a leaguea of legends` el asistente intentara pulsar `league_play_button`.
21. Si dices `clasificatoria solo duo` el asistente intentara pulsar `league_ranked_solo_duo_option`.
22. Si dices `pulsa confirmar` el asistente intentara pulsar `league_confirm_button`.
23. Si dices `encontrar partida` el asistente intentara pulsar `league_find_match_button`.
24. El parser local tolera algunas transcripciones defectuosas frecuentes de `League of Legends` como `log` o `diage of legends`.

## Acciones Permitidas

1. `open_application`: `calculator` `chrome` `explorer` `league_of_legends` `notepad` `paint` `riot_client`.
2. `close_application`: `calculator` `chrome` `league_of_legends` `notepad` `paint` `riot_client`.
3. `open_url`: Solo urls conocidas o urls expresas detectadas en la orden.
4. `type_text`: Escribe el texto dictado en la ventana activa.
5. `move_mouse`: Mueve el raton a coordenadas explicitas.
6. `click_mouse`: Hace click izquierdo derecho o medio en la posicion actual o en coordenadas explicitas.
7. `press_hotkey`: Ejecuta atajos compatibles con `alt` `ctrl` `delete` `enter` `esc` `shift` `tab` `win` y teclas alfanumericas simples.
8. `click_target`: `riot_lol_icon` `riot_play_button` `league_play_any_button` `league_play_button` `league_ranked_solo_duo_option` `league_confirm_button` `league_find_match_button`.
9. `trash_path`: Solo envia a la papelera rutas existentes no protegidas.

## Limitaciones

1. `click_target` no usa coordenadas libres ni clicks arbitrarios.
2. El click visual depende de que la ventana correcta este visible y de que el objetivo se vea con claridad en la captura.
3. Las plantillas opcionales pueden mejorar precision pero ya no son obligatorias para los objetivos de `League of Legends`.
4. `close_application` usa `taskkill` sobre procesos permitidos y puede fallar si Windows devuelve acceso denegado o si la app se ejecuto con mas privilegios.
5. El fallback con vision depende de que `qwen3-vl:30b` o `qwen3-vl:8b` este disponible en `Ollama`.

## Verificacion

1. Compilacion: `python -m compileall src spikes\17-voice_assistant`.
2. Practica: `.\venv\Scripts\python.exe .\spikes\17-voice_assistant\main.py`.
3. Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_17_voice_assistant.py`.

## Cobertura

1. `select_best_available_ollama_model`: Elige el mejor modelo de texto ya instalado en `Ollama`.
2. `process_voice_transcript`: Maneja confirmaciones por voz.
3. `click_target`: Busca un objetivo visual permitido primero con plantilla opcional y despues con vision sobre la pantalla actual.
4. `trash_path`: Mueve rutas a la papelera y rechaza rutas protegidas.
5. `write_pcm_frames_to_wav`: Genera el artefacto WAV desde frames PCM.
6. `LocalVoiceSpeaker`: Reproduce voz local y corta la respuesta previa antes de iniciar una nueva.
7. `close_application`: Cierra aplicaciones permitidas mediante `taskkill` tras confirmacion explicita.
