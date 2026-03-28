# Practica 27 ReAct Build Reasoning and Acting AI Agents with LangGraph

## Leyenda

1. `StateGraph`: La practica usa estado tipado con `add_messages` para automatizar el ciclo ReAct.
2. ReAct: El agente razona pide herramientas observa sus resultados y vuelve a decidir.
3. Herramientas reales: La practica incluye busqueda externa recomendaciones de ropa calculadora segura y resumen de noticias.
4. Ejercicios resueltos: `calculator_tool` y `news_summarizer_tool` ya quedan integrados en el agente.
5. Modelo real: El camino principal usa `ChatOllama` y evita depender de `OpenAI`.

## Adaptacion

Esta practica adapta el lab original de ReAct a la estructura del repositorio y al stack local basado en `Ollama`. En lugar de `ChatOpenAI` usa `ChatOllama`. La busqueda con Tavily sigue disponible cuando existe `TAVILY_API_KEY`, pero el spike agrega fallback sin credenciales con `wttr.in` para clima y `DuckDuckGo Instant Answer` para consultas generales. Asi el caso principal del laboratorio puede ejecutarse sin claves externas. Tambien se incluyen resueltos los ejercicios de calculadora segura y resumen de noticias.

## Roles de Archivos

- `main.py`: Punto de entrada de la practica.
- `config/react_agent_config.py`: Prompt del agente y consultas demo.
- `models/react_agent_state.py`: Estado tipado del agente con `add_messages`.
- `models/react_agent_entities.py`: Resultado tipado y pasos de tools.
- `models/react_agent_ollama_gateway.py`: Seleccion de modelo y construccion de `ChatOllama`.
- `models/react_search_gateway.py`: Fallbacks de busqueda y constantes para calculadora segura.
- `orchestration/react_tools_orchestration.py`: Definicion de tools y registro por nombre.
- `orchestration/react_agent_orchestration.py`: Nodo de modelo nodo de herramientas router grafo e invocacion.
- `orchestration/react_agent_lab_runner.py`: Runner guiado con clima calculadora noticias y Mermaid.

## Instalacion

1. Activar entorno: `\.venv\Scripts\Activate.ps1`.
2. Instalar dependencias base del repo: `pip install -r requirements.txt`.
3. Arrancar `Ollama`: `ollama serve`.
4. Descargar un modelo recomendado: `ollama pull qwen2.5:7b`.
5. Modelo compatible de menor consumo: `ollama pull llama3.2:3b`.
6. Opcional para Tavily: exportar `TAVILY_API_KEY` e instalar `pip install -U tavily-python`.

## Contenido del Lab

1. `search_tool`:
   Recupera informacion actual via Tavily o fallbacks sin API key.
2. `recommend_clothing`:
   Traduce una descripcion meteorologica en una recomendacion util.
3. `calculator_tool`:
   Evalua expresiones matematicas de forma segura con `ast`.
4. `news_summarizer_tool`:
   Resume hasta tres articulos o resultados de busqueda.
5. Grafo ReAct:
   Alterna entre un nodo `agent` y un nodo `tools` hasta que el modelo deje de pedir herramientas.

## Verificacion

1. Compilacion: `python -m compileall spikes\27-react_langgraph_agents`.
2. Practica: `.\venv\Scripts\python.exe .\spikes\27-react_langgraph_agents\main.py`.
3. Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_27_react_langgraph_agents.py`.

## Cobertura

1. `search_tool`: Usa Tavily o fallbacks para datos actuales.
2. `recommend_clothing`: Recomienda ropa segun el clima.
3. `calculator_tool`: Resuelve expresiones como porcentaje raiz o seno.
4. `news_summarizer_tool`: Resume resultados recientes.
5. `call_model`: Invoca el modelo con el estado actual.
6. `tool_node`: Ejecuta las tools pedidas por el modelo.
7. `should_continue`: Decide si el ciclo sigue o termina.
8. `invoke_react_query`: Ejecuta una consulta completa y resume pasos herramientas y respuesta final.

## Relacion con las Practicas 25 y 26

1. La practica 25 introduce reflexion iterativa.
2. La practica 26 agrega conocimiento externo y revision.
3. La practica 27 se centra en ReAct como patron general de razonamiento mas accion con herramientas reutilizables.