# Practica 32 Structured Meal Grocery Planner with CrewAI

## Leyenda

1. Modelos estructurados: La practica usa `Pydantic` para representar items comidas secciones y planes de compra.
2. Multi-agent planning: El flujo separa meal planner shopping organizer budget advisor leftover manager y report compiler.
3. YAML config: El agente y la tarea de leftovers viven en archivos YAML para reflejar el estilo `CrewBase`.
4. Ejercicios resueltos: Incluye nutrition analyst y modelos semanales de meal planning.
5. Modelo local: El camino principal usa `ChatOllama` y evita dependencias de `watsonx` o `Serper`.

## Adaptacion

Esta practica adapta el lab original a un entorno local reproducible. En lugar de depender de `SerperDevTool` y de `CrewAI` completo, el spike usa un catalogo local de recetas y una capa `crewai_compat` que mantiene los conceptos de agentes tareas y crews. El componente `LeftoversCrew` carga YAML desde `config/` para mostrar la idea de `CrewBase` sin depender de decoradores que en notebooks suelen ser fragiles.

## Roles de Archivos

- `main.py`: Punto de entrada del spike.
- `config/meal_planner_config.py`: Entradas demo y catalogo local de recetas y compras.
- `config/agents.yaml`: Configuracion YAML del agente de leftovers.
- `config/tasks.yaml`: Configuracion YAML de la tarea de leftovers.
- `models/meal_grocery_entities.py`: Modelos `Pydantic` de grocery planning y weekly planning.
- `models/meal_llm_gateway.py`: Seleccion de modelo y construccion de `ChatOllama`.
- `models/crewai_compat.py`: Compatibilidad local con el flujo conceptual de CrewAI.
- `models/recipe_search_tools.py`: Herramienta de recetas local y reproducible.
- `leftover.py`: Loader YAML que emula el comportamiento de un `CrewBase` simple.
- `orchestration/meal_grocery_workflow.py`: Agentes tareas crew principal crew nutricional y ejemplos semanales.

## Instalacion

1. Activar entorno: `\.venv\Scripts\Activate.ps1`.
2. Instalar dependencias base del repo: `pip install -r requirements.txt`.
3. Arrancar `Ollama`: `ollama serve`.
4. Descargar un modelo recomendado: `ollama pull qwen2.5:7b`.
5. Alternativa de menor consumo: `ollama pull llama3.2:3b`.
6. Opcional para usar CrewAI real: `pip install -U crewai crewai-tools`.

## Verificacion

1. Compilacion: `python -m compileall spikes\32-meal_grocery_planner`.
2. Practica: `venv\Scripts\python.exe .\spikes\32-meal_grocery_planner\main.py`.
3. Tests: `venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_32_meal_grocery_planner.py`.

## Cobertura

1. `MealPlan` y `GroceryShoppingPlan`: Estructuran el pipeline principal.
2. `LeftoversCrew`: Carga YAML y construye agente y tarea de leftovers.
3. `build_complete_grocery_crew`: Ejecuta el pipeline principal de cinco especialistas.
4. `build_health_focused_crew`: Resuelve el ejercicio del nutrition analyst.
5. `WeeklyMealPlan` y `WeeklyGroceryPlan`: Resuelven el ejercicio de weekly planning.