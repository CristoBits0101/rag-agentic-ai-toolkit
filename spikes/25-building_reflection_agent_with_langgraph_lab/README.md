# Practica 25 Building a Reflection Agent with LangGraph

## Leyenda

1. `MessageGraph`: La practica usa un grafo centrado en mensajes para conservar el contexto completo entre iteraciones.
2. Reflexion iterativa: El agente genera un borrador recibe una critica y vuelve a generar una version refinada.
3. LinkedIn post generator: El caso de uso principal es una publicacion corta para anunciar un nuevo puesto.
4. `HumanMessage` como feedback: La critica vuelve al flujo como si fuera una instruccion humana para guiar la siguiente revision.
5. Modelo real: El camino principal usa `ChatOllama` y evita depender de `watsonx.ai`.

## Adaptacion

Esta practica adapta el lab original de Reflection Agents con `LangGraph` a la estructura del repositorio y al stack local basado en `Ollama`. En lugar de `ChatWatsonx` usa `ChatOllama`, mantiene el enfoque de mensajes acumulados y resuelve la visualizacion del grafo con Mermaid integrada en LangGraph en vez de exigir `pygraphviz` como dependencia obligatoria. El resultado es un spike reproducible desde terminal y facil de validar con tests unitarios.

## Roles de Archivos

- `main.py`: Punto de entrada de la practica.
- `config/reflection_agent_config.py`: Prompts del generador y del critico limites de iteracion y request de ejemplo.
- `models/reflection_agent_entities.py`: Resultado tipado de una ejecucion del agente reflexivo.
- `models/reflection_agent_ollama_gateway.py`: Seleccion de modelo y construccion de `ChatOllama`.
- `orchestration/reflection_agent_workflow.py`: Prompts chains nodos router compilacion e invocacion del workflow.
- `orchestration/reflection_agent_lab_runner.py`: Runner guiado que muestra primer borrador primera critica resultado final y diagrama Mermaid.

## Instalacion

1. Activar entorno: `\.venv\Scripts\Activate.ps1`.
2. Instalar dependencias base del repo: `pip install -r requirements.txt`.
3. Arrancar `Ollama`: `ollama serve`.
4. Descargar un modelo recomendado: `ollama pull qwen2.5:7b`.
5. Modelo compatible de menor consumo: `ollama pull llama3.2:3b`.
6. Dependencia opcional para PNG externos: `pip install -U pygraphviz==1.14`.

## Contenido del Lab

1. Prompt de generacion:
   Crea un borrador de publicacion de LinkedIn y acepta feedback acumulado en el historial de mensajes.
2. Prompt de reflexion:
   Critica el post generado y produce recomendaciones practicas para la siguiente revision.
3. Nodo `generate`:
   Ejecuta la cadena de generacion y devuelve un `AIMessage`.
4. Nodo `reflect`:
   Ejecuta la cadena de reflexion y devuelve un `HumanMessage` para simular feedback humano.
5. Router condicional:
   Corta el ciclo cuando el numero total de mensajes alcanza el limite configurado.

## Verificacion

1. Compilacion: `python -m compileall spikes\25-building_reflection_agent_with_langgraph_lab`.
2. Practica: `.\venv\Scripts\python.exe .\spikes\25-building_reflection_agent_with_langgraph_lab\main.py`.
3. Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_25_building_reflection_agent_with_langgraph.py`.

## Cobertura

1. `build_generation_prompt`: Crea el prompt principal del LinkedIn post generator.
2. `build_reflection_prompt`: Crea el prompt del critico.
3. `generation_node`: Genera un nuevo borrador como `AIMessage`.
4. `reflection_node`: Convierte la critica en `HumanMessage`.
5. `should_continue`: Decide si el workflow termina o vuelve a reflexionar.
6. `invoke_reflection_agent`: Ejecuta el workflow y resume borradores criticas resultado final y Mermaid.

## Relacion con la Practica 24

1. La practica 24 introduce `StateGraph` y ciclos explicitos.
2. La practica 25 usa esa base para dar el siguiente paso natural: un agente que mejora su propia salida.
3. El foco pedagogico deja de ser el estado tipado general y pasa al historial de mensajes y a la reflexion iterativa.