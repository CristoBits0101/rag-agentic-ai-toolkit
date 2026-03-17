# Practica 18 LangChain Tool Calling Math Assistant

## Leyenda

1. `@tool`: Convierte funciones Python en herramientas compatibles con `LangChain`.
2. Tool calling: El modelo propone una llamada con argumentos y la aplicacion decide si ejecuta la herramienta.
3. Modelo demo: El spike usa un modelo determinista con `bind_tools` para simular un flujo de herramientas sin APIs externas.
4. Bucle controlado: La orquestacion ejecuta herramientas paso a paso hasta recibir una respuesta final.
5. Catalogo factual local: El ejemplo factual reemplaza `Wikipedia` por un dataset local para mantener reproducibilidad.

## Adaptacion

Esta practica adapta el lab de Skills Network sobre asistentes matematicos con `LangChain` pero elimina dependencias remotas y APIs legacy. En vez de `initialize_agent` o proveedores externos el spike usa tools modernas con `@tool`, un modelo demo con `bind_tools` y un bucle de ejecucion controlado. Con esto la practica sigue mostrando `tool calling`, composicion de herramientas y consultas multi paso de forma estable y testeable.

## Roles de Archivos

- `main.py`: Punto de entrada de la practica.
- `config/tool_calling_math_config.py`: Introduccion y consultas demo del laboratorio.
- `data/tool_calling_fact_catalog.py`: Catalogo factual local para consultas de referencia.
- `models/tool_calling_math_entities.py`: Dataclasses para pasos y resultados del bucle.
- `models/tool_calling_demo_chat_model.py`: Modelo demo con `bind_tools` y generacion determinista de tool calls.
- `orchestration/tool_calling_tools_orchestration.py`: Definicion de tools y parsing numerico.
- `orchestration/tool_calling_agent_orchestration.py`: Bucle de tool calling que ejecuta herramientas y conserva mensajes.
- `orchestration/tool_calling_lab_runner.py`: Runner guiado con introspeccion de schemas y consultas de ejemplo.

## Instalacion

1. Activar entorno: `.\venv\Scripts\Activate.ps1`.
2. Instalar dependencias base del repo: `pip install -r requirements.txt`.
3. No hacen falta claves de `OpenAI` ni de `IBM`.
4. No hace falta `langgraph` porque la practica demuestra el ciclo de `tool calling` con `LangChain Core` y un bucle local.

## Funcionamiento

1. La practica define varias tools matematicas con `@tool`.
2. Cada tool expone nombre descripcion y esquema de argumentos.
3. El modelo demo decide que herramienta llamar segun la consulta del usuario.
4. La orquestacion ejecuta la tool seleccionada y anade el resultado al historial.
5. Si la tarea requiere varios pasos el modelo propone una segunda llamada.
6. Cuando ya no hacen falta tools devuelve una respuesta final en lenguaje natural.

## Verificacion

1. Compilacion: `python -m compileall spikes\18-langchain_tool_calling_math_assistant_lab`.
2. Practica: `.\venv\Scripts\python.exe .\spikes\18-langchain_tool_calling_math_assistant_lab\main.py`.
3. Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_18_langchain_tool_calling_math_assistant.py`.

## Cobertura

1. `describe_tool_schemas`: Inspecciona nombre descripcion y argumentos de cada tool.
2. `add_numbers`: Suma numeros y palabras numericas simples.
3. `divide_numbers`: Controla division por cero con un error legible.
4. `calculate_power`: Calcula exponentes desde texto.
5. `execute_tool_calling_query`: Ejecuta tool calls secuenciales y conserva el historial.
6. `search_local_reference_fact`: Resuelve consultas factuales locales y las combina con calculo.
