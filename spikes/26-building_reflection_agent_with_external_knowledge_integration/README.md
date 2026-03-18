# Practica 26 Building a Reflection Agent with External Knowledge Integration

## Leyenda

1. `MessageGraph`: La practica usa un grafo centrado en mensajes para coordinar respuesta busqueda externa y revision.
2. Reflexion con herramientas: El agente responde se critica busca evidencia adicional y revisa su salida.
3. Conocimiento externo real: La practica usa Tavily si hay API key y si no hace fallback a Europe PMC sin credenciales.
4. Salida estructurada: El agente usa modelos `Pydantic` para forzar answer critique queries y referencias.
5. Modelo real: El camino principal usa `ChatOllama` y mantiene el stack local del repositorio.

## Adaptacion

Esta practica adapta el lab original de external knowledge reflection al stack del repositorio. En lugar de `ChatOpenAI` usa `ChatOllama` como LLM principal. El componente de investigacion externa mantiene compatibilidad con `Tavily` cuando existe `TAVILY_API_KEY`, pero agrega un fallback gratuito con Europe PMC para que el laboratorio pueda ejecutarse sin depender de claves externas. Tambien se corrige el enfoque del prompt hacia nutricion basada en evidencia y no hacia una persona polemica concreta, ya que el objetivo pedagogico es construir el flujo reflexivo y no fijar una doctrina nutricional sesgada.

## Roles de Archivos

- `main.py`: Punto de entrada de la practica.
- `config/external_reflection_agent_config.py`: Prompts limites y pregunta de ejemplo.
- `models/external_reflection_agent_entities.py`: Resultado tipado de una ejecucion completa.
- `models/external_reflection_ollama_gateway.py`: Seleccion de modelo y construccion de `ChatOllama`.
- `models/external_knowledge_gateway.py`: Integracion de Tavily opcional y fallback a Europe PMC.
- `orchestration/external_reflection_agent_workflow.py`: Modelos `Pydantic` nodos loops compilacion e invocacion del workflow.
- `orchestration/external_reflection_agent_lab_runner.py`: Runner guiado con impresion de respuesta inicial final queries referencias y Mermaid.

## Instalacion

1. Activar entorno: `\.venv\Scripts\Activate.ps1`.
2. Instalar dependencias base del repo: `pip install -r requirements.txt`.
3. Arrancar `Ollama`: `ollama serve`.
4. Descargar un modelo recomendado: `ollama pull qwen2.5:7b`.
5. Modelo compatible de menor consumo: `ollama pull llama3.2:3b`.
6. Opcional para Tavily: exportar `TAVILY_API_KEY` e instalar `pip install -U tavily-python`.

## Contenido del Lab

1. Responder:
   Genera una primera respuesta estructurada con answer reflection y search queries.
2. Tool Executor:
   Ejecuta busquedas externas para cada query propuesta por el modelo.
3. Revisor:
   Reescribe la respuesta con evidencia adicional y agrega referencias.
4. Event loop:
   Repite el ciclo hasta agotar el numero maximo de iteraciones basado en `ToolMessage`.

## Verificacion

1. Compilacion: `python -m compileall spikes\26-building_reflection_agent_with_external_knowledge_integration`.
2. Practica: `.\venv\Scripts\python.exe .\spikes\26-building_reflection_agent_with_external_knowledge_integration\main.py`.
3. Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_26_building_reflection_agent_with_external_knowledge_integration.py`.

## Cobertura

1. `build_responder_chain`: Fuerza respuesta estructurada con `AnswerQuestion`.
2. `execute_tools`: Convierte queries en `ToolMessage` con evidencia serializada.
3. `build_revisor_chain`: Fuerza revision estructurada con `ReviseAnswer`.
4. `event_loop`: Controla el numero de iteraciones.
5. `invoke_external_reflection_agent`: Resume respuesta inicial revisiones final referencias y Mermaid.

## Relacion con las Practicas 24 y 25

1. La practica 24 introduce `StateGraph` y ciclos de control.
2. La practica 25 introduce reflexion sobre mensajes.
3. La practica 26 agrega herramientas de conocimiento externo y una revision guiada por evidencia.