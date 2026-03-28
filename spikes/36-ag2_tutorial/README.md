# Practica 36 AG2 101 Complete Tutorial

## Leyenda

1. Tutorial guiado: La practica recorre agentes conversacionales herramientas group chat HITL y salidas estructuradas.
2. Capa AG2 compatible: Replica `ConversableAgent`, `AssistantAgent`, `UserProxyAgent`, `GroupChat` y `GroupChatManager` en local.
3. Sin claves externas: La ejecucion por defecto no necesita `OpenAI` para enseÃ±ar la orquestacion.
4. Enfoque reproducible: Los ejemplos se convierten en funciones testeables y un runner unico.
5. Adaptacion segura: El ejemplo de codigo genera un `SVG` local en lugar de depender de `matplotlib` y de un notebook.

## Adaptacion

El laboratorio original dependia de `AG2` real, de modelos GPT remotos y de celdas interactivas. Esta adaptacion conserva los conceptos y los patrones de colaboracion entre agentes pero los convierte en una practica local y ejecutable desde terminal. El objetivo del spike es aprender la arquitectura y no bloquearse por credenciales o por dependencias de notebook.

## Roles de Archivos

- `main.py`: Runner principal del tutorial.
- `config/ag2_tutorial_config.py`: Configuracion demo tickets y ejemplos.
- `models/ag2_compat.py`: Capa local compatible con AG2.
- `models/ag2_entities.py`: Modelo estructurado de soporte.
- `orchestration/ag2_tutorial_workflow.py`: Implementacion de todos los ejemplos del tutorial.

## Instalacion

1. Activar entorno: `.\venv\Scripts\Activate.ps1`.
2. Instalar dependencias base del repo: `pip install -r requirements.txt`.
3. Opcional para contrastar con AG2 real fuera del camino principal: `pip install ag2[openai] python-dotenv`.

## Verificacion

1. Compilacion: `python -m compileall spikes\36-ag2_tutorial`.
2. Practica: `venv\Scripts\python.exe .\spikes\36-ag2_tutorial\main.py`.
3. Tests: `venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_36_ag2_tutorial.py`.

## Cobertura

1. `conversational_agent_demo`: Chat basico entre estudiante y tutor.
2. `build_specialized_agents`: Agentes tecnico creativo y de negocio.
3. `built_in_agent_demo`: Patron `AssistantAgent` y `UserProxyAgent` con ejecucion local de codigo.
4. `human_in_the_loop_demo`: Bug triage con revision humana simulada.
5. `group_chat_lesson_planning_demo`: `GroupChat` y `GroupChatManager` para planificacion de clase.
6. `tools_and_extensions_demo`: Registro de funciones como tools.
7. `structured_outputs_demo`: Salidas estructuradas con `Pydantic`.