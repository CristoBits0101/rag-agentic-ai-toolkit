# Practica 24 LangGraph 101 Building Stateful AI Workflows

## Leyenda

1. `StateGraph`: La practica usa el grafo con estado compartido de `LangGraph` como base de todos los flujos.
2. Workflow ciclico: El flujo de autenticacion demuestra reintentos y lockout con aristas condicionales.
3. QA con contexto: El flujo de preguntas y respuestas valida entrada aporta contexto y delega la respuesta a `ChatOllama`.
4. Ejercicio resuelto: La practica incluye el contador ciclico del lab original como tercer workflow.
5. Modelo real: El camino principal usa `ChatOllama` y no depende de `watsonx.ai` ni de `OpenAI`.

## Adaptacion

Esta practica adapta el lab original de Skills Network sobre `LangGraph` a la estructura real del repositorio. Se elimina la dependencia de `langchain-ibm` y se sustituye por `ChatOllama` como implementacion principal para el workflow de preguntas y respuestas. Tambien se reemplaza la entrada interactiva del notebook por una cola de intentos de autenticacion dentro del estado para que el flujo ciclico sea reproducible desde terminal y testeable en unit tests.

## Roles de Archivos

- `main.py`: Punto de entrada de la practica.
- `config/langgraph_workflows_config.py`: Contexto del lab credenciales demo preguntas y modelos recomendados.
- `models/langgraph_workflows_state.py`: Estados tipados de autenticacion QA y contador.
- `models/langgraph_workflows_entities.py`: Resultados tipados de cada workflow.
- `models/langgraph_workflows_ollama_gateway.py`: Seleccion de modelo y construccion de `ChatOllama`.
- `orchestration/langgraph_auth_workflow.py`: Workflow de autenticacion con reintentos lockout y salida tipada.
- `orchestration/langgraph_qa_workflow.py`: Workflow QA con validacion contexto y llamada al modelo.
- `orchestration/langgraph_counter_workflow.py`: Ejercicios 1 a 6 del contador implementados con `LangGraph`.
- `orchestration/langgraph_lab_runner.py`: Runner guiado que ejecuta las tres demostraciones.

## Instalacion

1. Activar entorno: `\.venv\Scripts\Activate.ps1`.
2. Instalar dependencias base del repo: `pip install -r requirements.txt`.
3. Instalar `LangGraph` si aun no esta disponible: `pip install -U langgraph==0.2.57`.
4. Arrancar `Ollama`: `ollama serve`.
5. Descargar un modelo recomendado: `ollama pull qwen2.5:7b`.
6. Modelo compatible de menor consumo: `ollama pull llama3.2:3b`.

## Contenido del Lab

1. Workflow de autenticacion:
   Usa `AuthState` nodos de entrada validacion exito fallo y lockout. El flujo demuestra `StateGraph` aristas normales y una arista condicional que decide entre exito reintento o bloqueo.
2. Workflow QA sobre LangGraph:
   Usa `QAState` para validar la pregunta decidir si hay contexto suficiente y responder con `ChatOllama` solo cuando la consulta esta relacionada con el guided project.
3. Ejercicio del contador:
   Implementa `ChainState` la funcion `add` la funcion `print_out` la condicion de parada y el bucle hasta que `n` alcance 13.

## Verificacion

1. Compilacion: `python -m compileall spikes\24-langgraph_stateful_workflows`.
2. Practica: `.\.venv\Scripts\python.exe .\spikes\24-langgraph_stateful_workflows\main.py`.
3. Tests: `.\.venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_24_langgraph_stateful_workflows.py`.

## Cobertura

1. `input_node`: Carga credenciales desde el estado o desde una cola de intentos.
2. `validate_credentials_node`: Comprueba usuario y password y actualiza el contador de intentos.
3. `auth_router`: Decide entre exito reintento o lockout.
4. `input_validation_node`: Rechaza preguntas vacias.
5. `context_provider_node`: Decide si la pregunta es relevante para el guided project.
6. `llm_qa_node`: Construye el prompt y consulta el modelo real.
7. `add`: Incrementa el contador y genera una letra aleatoria.
8. `stop_condition`: Cierra el workflow cuando `n` llega a 13.

## Relacion con el Lab Original

1. Se conserva el objetivo de aprender `StateGraph` nodos aristas y aristas condicionales.
2. Se mantienen los dos casos de uso principales del lab original: autenticacion y QA sobre LangGraph.
3. Se implementan los ejercicios finales dentro de `langgraph_counter_workflow.py`.
4. Se adapta el stack a los modelos reales y accesibles del repositorio.