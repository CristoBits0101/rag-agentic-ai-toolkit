# Practica 21 YouTube Tool Calling Agent

## Leyenda

1. Tools de YouTube: La practica usa herramientas reales para buscar videos leer transcriptos extraer metadatos y recuperar thumbnails.
2. Manual tool calling: Primero se ejecuta el flujo paso a paso para entender `tool_calls` y `ToolMessage`.
3. Cadena fija: Despues se automatiza el caso de resumen con una secuencia predecible de pasos.
4. Cadena recursiva: Finalmente se construye un agente que puede iterar hasta completar las herramientas necesarias.
5. Modelo real: El camino principal usa `ChatOllama` y no depende de `OpenAI`.

## Adaptacion

Esta practica adapta el lab original sin `OpenAI` y sin notebooks. En lugar de `gpt-4o-mini` usa `ChatOllama` y mantiene integraciones reales y gratuitas con YouTube mediante `yt-dlp` y `youtube-transcript-api`. La separacion con la practica 12 es tecnica y pedagogica: la `12` trabaja `RAG` con transcriptos locales y `FAISS`, mientras que la `21` se centra en `tool calling` manual automatizado y recursivo sobre sistemas externos reales. La separacion con la `20` tambien es clara: la `20` explica el ciclo generico con herramientas simples y esta `21` lo lleva a un caso multi paso sobre YouTube.

## Roles de Archivos

- `main.py`: Punto de entrada de la practica.
- `config/youtube_tool_calling_agent_config.py`: Prompts limites y consultas demo.
- `models/youtube_tool_calling_entities.py`: Dataclasses del flujo y de los pasos ejecutados.
- `models/youtube_tool_calling_ollama_gateway.py`: Seleccion de modelo y construccion del `ChatOllama` principal.
- `orchestration/youtube_tool_calling_tools_orchestration.py`: Tools reales de YouTube y mapeo de herramientas.
- `orchestration/youtube_tool_calling_agent_orchestration.py`: Flujo manual cadena fija cadena recursiva y clase de agente.
- `orchestration/youtube_tool_calling_lab_runner.py`: Runner guiado del laboratorio.

## Instalacion

1. Activar entorno: `.\venv\Scripts\Activate.ps1`.
2. Instalar dependencias base del repo: `pip install -r requirements.txt`.
3. Instalar dependencias del laboratorio: `pip install -U yt-dlp youtube-transcript-api`.
4. Arrancar `Ollama`: `ollama serve`.
5. Descargar un modelo recomendado: `ollama pull qwen2.5:7b`.
6. Modelo compatible de menor consumo: `ollama pull llama3.2:3b`.
7. La practica requiere acceso a internet para consultar YouTube.

## Funcionamiento

1. La practica define tools con `@tool` para extraer el `video_id` recuperar transcriptos buscar videos y leer metadatos y thumbnails.
2. El modelo recibe esas tools mediante `bind_tools`.
3. El flujo manual muestra como leer `tool_calls` ejecutar cada herramienta y devolver el resultado con `ToolMessage`.
4. La cadena fija automatiza el resumen de un video a partir de URL y transcripto.
5. La cadena recursiva procesa un numero variable de llamadas hasta que el modelo entrega la respuesta final.
6. La clase `YouTubeToolCallingAgent` envuelve la cadena recursiva para consultas mas flexibles.

## Verificacion

1. Compilacion: `python -m compileall spikes\21-youtube_tool_agent`.
2. Practica: `.\venv\Scripts\python.exe .\spikes\21-youtube_tool_agent\main.py`.
3. Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_21_youtube_tool_agent.py`.

## Cobertura

1. `extract_video_id`: Extrae el identificador de un enlace de YouTube.
2. `fetch_transcript`: Recupera y normaliza el transcripto de un video.
3. `search_youtube`: Busca videos con `yt-dlp`.
4. `get_full_metadata`: Extrae metadatos ricos del video.
5. `get_thumbnails`: Recupera thumbnails y resoluciones.
6. `execute_manual_youtube_summary_flow`: Ejecuta el flujo manual del resumen.
7. `build_fixed_summarization_chain`: Automatiza un caso de resumen con secuencia fija.
8. `build_universal_recursive_chain`: Construye la cadena recursiva para consultas de varias herramientas.
9. `YouTubeToolCallingAgent`: Expone la version reutilizable del agente.
