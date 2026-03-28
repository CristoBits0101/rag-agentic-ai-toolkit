# Practica 33 Agents with Tools versus Tasks with Tools in CrewAI

## Leyenda

1. Comparacion explicita: La practica ejecuta el mismo chatbot con asignacion de tools al agente y con asignacion de tools a cada tarea.
2. Base local reproducible: El conocimiento del restaurante vive en una FAQ local y en snippets suplementarios de tipo web.
3. CrewAI compatible: El spike conserva `Agent` `Task` `Crew` y `Process.sequential` mediante una capa ligera local.
4. Herramientas custom: Incluye una extension con tools de suma y multiplicacion para mostrar como registrar funciones propias.
5. Enfoque operacional: El output deja visible que tools se usaron para que la diferencia sea medible y no solo conceptual.

## Adaptacion

El laboratorio original dependia de `PDFSearchTool` `SerperDevTool` y de un modelo remoto. En esta adaptacion la FAQ del PDF se normaliza a una base local reproducible y la busqueda web se sustituye por snippets locales que representan informacion suplementaria como parking y transporte. El modelo principal usa `ChatOllama` y los tests inyectan un modelo fake para validar el flujo sin red.

## Roles de Archivos

- `main.py`: Punto de entrada del spike.
- `config/daily_dish_chatbot_config.py`: FAQ base snippets suplementarios y prompts demo.
- `models/crewai_compat.py`: Compatibilidad local de CrewAI con override de tools por tarea.
- `models/daily_dish_entities.py`: Modelos tipados para el resumen comparativo y la demo de custom tools.
- `models/daily_dish_llm_gateway.py`: Seleccion del modelo local en `Ollama`.
- `models/daily_dish_tools.py`: Herramientas FAQ web y tools custom de aritmetica.
- `orchestration/daily_dish_chatbot_workflow.py`: Construccion de crews ejecucion comparativa y demo final.

## Instalacion

1. Activar entorno: `.\venv\Scripts\Activate.ps1`.
2. Instalar dependencias base del repo: `pip install -r requirements.txt`.
3. Arrancar `Ollama`: `ollama serve`.
4. Descargar un modelo recomendado: `ollama pull qwen2.5:7b`.
5. Alternativa de menor consumo: `ollama pull llama3.2:3b`.
6. Opcional para usar CrewAI real: `pip install -U crewai crewai-tools`.

## Verificacion

1. Compilacion: `python -m compileall spikes\33-crewai_tools_vs_tasks`.
2. Practica: `venv\Scripts\python.exe .\spikes\33-crewai_tools_vs_tasks\main.py`.
3. Tests: `venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_33_crewai_tools_vs_tasks.py`.

## Cobertura

1. `build_agent_centric_crew`: Da al agente una caja de herramientas completa.
2. `build_task_centric_crew`: Expone cada tool solo en la tarea que la necesita.
3. `compare_tool_assignment`: Ejecuta ambos enfoques y resume tools usadas y respuestas.
4. `build_calculator_crew`: Demuestra tools custom registradas desde funciones Python.
5. `run_daily_dish_demo`: Imprime ejemplos con una consulta FAQ simple y otra con informacion suplementaria.