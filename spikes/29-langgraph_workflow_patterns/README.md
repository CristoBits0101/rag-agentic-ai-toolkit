# Practica 29 Implement Workflow Patterns with LangGraph

## Leyenda

1. Prompt chaining: La practica encadena dos agentes para convertir una oferta de trabajo en un resumen y luego en una cover letter.
2. Routing: Un router clasifica si la solicitud debe resumirse o traducirse.
3. Parallelization: Tres traducciones independientes se ejecutan en paralelo y luego se agregan.
4. Multi-agent routing: El ejercicio final enruta peticiones a ride hailing restaurante groceries o soporte.
5. Modelo local: El camino principal usa `ChatOllama` y evita `ChatOpenAI`.

## Adaptacion

Esta practica adapta el lab original a la version de `LangGraph` ya instalada en el repositorio y al stack local basado en `Ollama`. La clasificacion de routing usa heuristicas estables para que el laboratorio siga siendo reproducible con modelos locales. Las generaciones siguen pasando por `ChatOllama`, lo que conserva el enfoque multiagente sin depender de claves de `OpenAI`.

## Roles de Archivos

- `main.py`: Punto de entrada del spike.
- `config/workflow_patterns_config.py`: Entradas demo para cada patron.
- `models/workflow_patterns_state.py`: Estados tipados para cadenas rutas y traducciones.
- `models/workflow_patterns_entities.py`: Entidad simple de resultados del laboratorio.
- `models/workflow_patterns_ollama_gateway.py`: Seleccion de modelo y construccion de `ChatOllama`.
- `orchestration/prompt_chaining_workflow.py`: Workflow secuencial de resumen y cover letter.
- `orchestration/routing_workflow.py`: Router de resumen o traduccion.
- `orchestration/parallel_workflow.py`: Flujo de traduccion paralela a tres idiomas.
- `orchestration/service_router_workflow.py`: Ejercicio final de routing multiagente por intencion.
- `orchestration/workflow_patterns_lab_runner.py`: Runner CLI con Mermaid y ejemplos.

## Instalacion

1. Activar entorno: `\.venv\Scripts\Activate.ps1`.
2. Instalar dependencias base del repo: `pip install -r requirements.txt`.
3. Arrancar `Ollama`: `ollama serve`.
4. Descargar un modelo recomendado: `ollama pull qwen2.5:7b`.
5. Alternativa de menor consumo: `ollama pull llama3.2:3b`.

## Verificacion

1. Compilacion: `python -m compileall spikes\29-langgraph_workflow_patterns`.
2. Practica: `venv\Scripts\python.exe .\spikes\29-langgraph_workflow_patterns\main.py`.
3. Tests: `venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_29_langgraph_workflow_patterns.py`.

## Cobertura

1. `generate_resume_summary`: Resume la candidatura ideal a partir de la vacante.
2. `generate_cover_letter`: Produce una carta profesional usando el resumen previo.
3. `router_node`: Decide entre resumen y traduccion.
4. `translate_french` `translate_spanish` `translate_japanese`: Ejecutan traducciones paralelas.
5. `aggregator`: Une los tres resultados en una sola salida.
6. `service_router_workflow`: Resuelve el ejercicio de routing con cuatro destinos.