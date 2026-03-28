# Practica 20 Interactive LLM Agents with Tools

## Leyenda

1. Manual tool calling: El modelo propone una herramienta y la aplicacion valida y ejecuta esa llamada.
2. `bind_tools`: `LangChain` expone las tools al modelo con su esquema y descripcion.
3. `ToolMessage`: El resultado de la tool vuelve al historial para que el modelo cierre la respuesta.
4. Agente interactivo: La practica encapsula el flujo en clases reutilizables.
5. Modelo real: El camino principal usa `ChatOllama` y no depende de modelos demo.

## Adaptacion

Esta practica adapta el lab de Skills Network sobre agentes interactivos con tools pero lo ajusta al stack real del repositorio. En lugar de `OpenAI` usa `ChatOllama` como implementacion principal y convierte el notebook en una practica reproducible desde terminal. El foco pedagogico es distinto al de la practica 18: aqui la prioridad es entender el ciclo manual de `tool calling`, el uso de `tool_map`, `ToolMessage` y la construccion de clases `ToolCallingAgent` y `TipAgent`.

## Roles de Archivos

- `main.py`: Punto de entrada de la practica.
- `config/interactive_agents_config.py`: Prompts limites y consultas demo.
- `models/interactive_agents_entities.py`: Dataclasses del flujo de tool calling.
- `models/interactive_agents_ollama_gateway.py`: Seleccion de modelo y construccion del `ChatOllama` principal.
- `orchestration/interactive_agents_tools_orchestration.py`: Tools aritmeticas y de calculo de propina.
- `orchestration/interactive_agents_manual_tool_calling_orchestration.py`: Flujo manual de parseo ejecucion y cierre con `ToolMessage`.
- `orchestration/interactive_agents_agent_orchestration.py`: Clases `ToolCallingAgent` y `TipAgent`.
- `orchestration/interactive_agents_lab_runner.py`: Runner guiado del laboratorio.

## Instalacion

1. Activar entorno: `.\venv\Scripts\Activate.ps1`.
2. Instalar dependencias base del repo: `pip install -r requirements.txt`.
3. Arrancar `Ollama`: `ollama serve`.
4. Descargar un modelo recomendado: `ollama pull qwen2.5:7b`.
5. Modelo compatible de menor consumo: `ollama pull llama3.2:3b`.
6. No hacen falta claves de `OpenAI` ni de `IBM`.

## Funcionamiento

1. La practica define tools con `@tool` para suma resta multiplicacion y propina.
2. El modelo recibe esas tools mediante `bind_tools`.
3. La orquestacion inspecciona `AIMessage.tool_calls` y extrae nombre argumentos e identificador.
4. La aplicacion ejecuta la tool correcta con `tool_map`.
5. El resultado vuelve al historial como `ToolMessage`.
6. El modelo genera la respuesta final usando ese contexto.
7. Las clases `ToolCallingAgent` y `TipAgent` encapsulan el proceso completo.

## Verificacion

1. Compilacion: `python -m compileall spikes\20-interactive_agents`.
2. Practica: `.\venv\Scripts\python.exe .\spikes\20-interactive_agents\main.py`.
3. Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_20_interactive_agents.py`.

## Cobertura

1. `add`: Suma dos enteros usando el contrato basico de una tool.
2. `subtract`: Resta dos enteros.
3. `multiply`: Multiplica dos enteros.
4. `calculate_tip`: Calcula la propina y el total final.
5. `extract_tool_calls_from_ai_message`: Lee la propuesta estructurada del modelo.
6. `execute_manual_tool_calling_query`: Ejecuta el ciclo manual completo con `ToolMessage`.
7. `ToolCallingAgent`: Envuelve el flujo para consultas aritmeticas.
8. `TipAgent`: Resuelve consultas de propina con la misma arquitectura.
