# Practica 18 LangChain Tool Calling Math Assistant

## Leyenda

1. `@tool`: Convierte funciones Python en herramientas compatibles con `LangChain`.
2. Tool calling: El modelo propone una llamada con argumentos y la aplicacion decide si ejecuta la herramienta.
3. Modelo real: El spike usa `ChatOllama` como implementacion principal y conserva un modelo demo solo para tests.
4. Bucle controlado: La orquestacion ejecuta herramientas paso a paso hasta recibir una respuesta final.
5. Catalogo factual local: El ejemplo factual reemplaza `Wikipedia` por un dataset local para mantener reproducibilidad.

## Adaptacion

Esta practica adapta el lab de Skills Network sobre asistentes matematicos con `LangChain` usando un modelo real servido por `Ollama` como camino principal. El spike evita `initialize_agent`, mantiene tools modernas con `@tool` y usa un bucle controlado de ejecucion para conservar trazabilidad. El modelo demo solo se conserva como variante complementaria para tests y comparacion reproducible.

## Roles de Archivos

- `main.py`: Punto de entrada de la practica.
- `config/tool_calling_math_config.py`: Introduccion y consultas demo del laboratorio.
- `data/tool_calling_fact_catalog.py`: Catalogo factual local para consultas de referencia.
- `models/tool_calling_math_entities.py`: Dataclasses para pasos y resultados del bucle.
- `models/tool_calling_ollama_gateway.py`: Seleccion de modelo y construccion del `ChatOllama` principal.
- `models/tool_calling_demo_chat_model.py`: Modelo demo con `bind_tools` y generacion determinista de tool calls.
- `orchestration/tool_calling_tools_orchestration.py`: Definicion de tools y parsing numerico.
- `orchestration/tool_calling_agent_orchestration.py`: Bucle de tool calling que ejecuta herramientas y conserva mensajes.
- `orchestration/tool_calling_lab_runner.py`: Runner guiado con introspeccion de schemas y consultas de ejemplo.

## Instalacion

1. Activar entorno: `.\venv\Scripts\Activate.ps1`.
2. Instalar dependencias base del repo: `pip install -r requirements.txt`.
3. Arrancar `Ollama`: `ollama serve`.
4. Descargar un modelo recomendado: `ollama pull qwen2.5:7b`.
5. Modelo compatible de menor consumo: `ollama pull llama3.2:3b`.
6. No hacen falta claves de `OpenAI` ni de `IBM`.
7. No hace falta `langgraph` porque la practica demuestra el ciclo de `tool calling` con `LangChain Core` y un bucle local.

## Funcionamiento

1. La practica define varias tools matematicas con `@tool`.
2. Cada tool expone nombre descripcion y esquema de argumentos.
3. `ChatOllama` decide que herramienta llamar segun la consulta del usuario.
4. La orquestacion ejecuta la tool seleccionada y anade el resultado al historial.
5. Si la tarea requiere varios pasos el modelo propone una segunda llamada.
6. Cuando ya no hacen falta tools devuelve una respuesta final en lenguaje natural.

## Verificacion

1. Compilacion: `python -m compileall spikes\18-tool_calling_math`.
2. Practica: `.\venv\Scripts\python.exe .\spikes\18-tool_calling_math\main.py`.
3. Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_18_tool_calling_math.py`.

## Cobertura

1. `describe_tool_schemas`: Inspecciona nombre descripcion y argumentos de cada tool.
2. `add_numbers`: Suma numeros y palabras numericas simples.
3. `divide_numbers`: Controla division por cero con un error legible.
4. `calculate_power`: Calcula exponentes desde texto.
5. `execute_tool_calling_query`: Ejecuta tool calls secuenciales y conserva el historial.
6. `search_local_reference_fact`: Resuelve consultas factuales locales y las combina con calculo.
7. `build_tool_calling_math_ollama_chat_model`: Construye el modelo real principal con `Ollama`.
