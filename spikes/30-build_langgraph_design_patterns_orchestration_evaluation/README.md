# Practica 30 Build LangGraph Design Patterns Orchestration Evaluation

## Leyenda

1. Orchestrator worker: La practica divide una solicitud de comidas en platos y lanza un worker por plato.
2. Reflection: El segundo flujo genera un plan de inversion lo evalua y lo refina en un bucle controlado.
3. Estado compartido: Ambos patrones dependen de `TypedDict` y en el caso orquestado usan `Annotated` para agregacion.
4. Routing condicional: La reflexion decide si acepta la propuesta o vuelve a generarla.
5. Modelo local: El camino principal usa `ChatOllama` y evita `ChatOpenAI`.

## Adaptacion

Esta practica adapta el lab a `LangGraph` 0.2.x y al stack local del repositorio. Para mantener el flujo reproducible la descomposicion de comidas usa un catalogo determinista y la evaluacion de riesgo aplica reglas transparentes. Las partes creativas del laboratorio siguen usando `ChatOllama` para que el resultado conserve el comportamiento multiagente sin depender de credenciales externas.

## Roles de Archivos

- `main.py`: Punto de entrada del spike.
- `config/design_patterns_config.py`: Solicitudes demo de comidas e inversion y catalogo base.
- `models/design_patterns_entities.py`: Modelos `Dish` y `Dishes`.
- `models/design_patterns_state.py`: Estados tipados del flujo orquestado y del flujo reflexivo.
- `models/design_patterns_ollama_gateway.py`: Seleccion de modelo y construccion de `ChatOllama`.
- `orchestration/orchestrator_worker_workflow.py`: Grafo del patron orquestador worker con `Send`.
- `orchestration/reflection_workflow.py`: Grafo de generacion evaluacion y refinamiento.
- `orchestration/design_patterns_lab_runner.py`: Runner CLI con Mermaid y resultados formateados.

## Instalacion

1. Activar entorno: `\.venv\Scripts\Activate.ps1`.
2. Instalar dependencias base del repo: `pip install -r requirements.txt`.
3. Arrancar `Ollama`: `ollama serve`.
4. Descargar un modelo recomendado: `ollama pull qwen2.5:7b`.
5. Alternativa de menor consumo: `ollama pull llama3.2:3b`.

## Verificacion

1. Compilacion: `python -m compileall spikes\30-build_langgraph_design_patterns_orchestration_evaluation`.
2. Practica: `venv\Scripts\python.exe .\spikes\30-build_langgraph_design_patterns_orchestration_evaluation\main.py`.
3. Tests: `venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_30_build_langgraph_design_patterns_orchestration_evaluation.py`.

## Cobertura

1. `orchestrator`: Divide la solicitud de comidas en platos estructurados.
2. `assign_workers`: Lanza un worker por plato con `Send`.
3. `chef_worker`: Genera una guia de cocina por plato.
4. `synthesizer`: Une todos los resultados en una guia final.
5. `determine_target_grade`: Estima el perfil de riesgo objetivo.
6. `investment_plan_generator`: Genera o corrige una estrategia de inversion.
7. `evaluate_plan`: Asigna grado de riesgo y feedback.
8. `route_investment`: Decide aceptar o iterar.