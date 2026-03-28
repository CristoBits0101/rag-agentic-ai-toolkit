# Practica 34 Building your own AI Nutrition Coach using a Multi Agent System and Multimodal AI

## Leyenda

1. Multimodal con fallback realista: El spike intenta enriquecer la deteccion con un modelo de vision en `Ollama` y si no esta disponible cae a matching visual local por similitud.
2. Multiagente claro: Se separan vision nutrition dietary recipe y escritura final en agentes especializados.
3. Dos workflows: `analysis` para desglosar nutrientes y `recipe` para proponer una adaptacion segun preferencia dietaria.
4. Interfaz Gradio: La practica incluye una UI lista para uso local ademas de una demo CLI.
5. Dataset local: Los ejemplos de comidas y sus nutrientes se generan y versionan de forma reproducible dentro del spike.

## Adaptacion

El laboratorio original dependia de `watsonx` y de un repositorio externo completo. En esta adaptacion el camino principal usa `ChatOllama` para la redaccion y un gateway de vision compatible con `Ollama` para enriquecer la descripcion cuando el modelo esta disponible. Para mantener la ejecucion local y estable el reconocimiento visual siempre tiene un fallback basado en similitud de imagenes generadas localmente. El resultado conserva el objetivo pedagogico del lab original sin requerir credenciales externas.

## Roles de Archivos

- `main.py`: Runner CLI con demo de `analysis` y `recipe`.
- `app.py`: Lanzador de la interfaz `Gradio`.
- `config/nourishbot_config.py`: Rutas modelos puertos y preferencias soportadas.
- `data/nourishbot_dataset.py`: Catalogo local de comidas nutrientes y reglas dietarias.
- `models/crewai_compat.py`: Compatibilidad local con `CrewAI`.
- `models/nourishbot_entities.py`: Modelos `Pydantic` para deteccion analisis dieta y recetas.
- `models/nourishbot_image_processor.py`: Embeddings visuales ligeros y matching por similitud.
- `models/nourishbot_llm_gateway.py`: Acceso al modelo de texto y al modelo de vision en `Ollama`.
- `models/nourishbot_tools.py`: Tools de deteccion nutricion dieta y recipe planning.
- `orchestration/nourishbot_asset_orchestration.py`: Generacion de assets y dataset con embeddings.
- `orchestration/nourishbot_workflow.py`: Definicion de crews y ejecucion de ambos workflows.
- `ui/nourishbot_ui.py`: Interfaz `Gradio` para carga de imagen y visualizacion del resultado.

## Instalacion

1. Activar entorno: `.\venv\Scripts\Activate.ps1`.
2. Instalar dependencias base del repo: `pip install -r requirements.txt`.
3. Arrancar `Ollama`: `ollama serve`.
4. Descargar un modelo de texto recomendado: `ollama pull qwen2.5:7b`.
5. Descargar un modelo de vision recomendado: `ollama pull qwen2.5vl:3b`.
6. Alternativas de vision: `ollama pull llava` o `ollama pull llama3.2-vision`.

## Verificacion

1. Compilacion: `python -m compileall spikes\34-nutrition_coach_multi_agent`.
2. Demo CLI: `venv\Scripts\python.exe .\spikes\34-nutrition_coach_multi_agent\main.py`.
3. Tests: `venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_34_nutrition_coach_multi_agent.py`.
4. UI local: `venv\Scripts\python.exe .\spikes\34-nutrition_coach_multi_agent\app.py`.

## Cobertura

1. `VisionMealDetectionTool`: Identifica la comida y adjunta notas multimodales o fallback local.
2. `NutritionLookupTool`: Traduce la deteccion a calorias macros micronutrientes y evaluacion de salud.
3. `DietaryPreferenceTool`: Filtra ingredientes y explica ajustes para la preferencia seleccionada.
4. `RecipePlanningTool`: Propone una receta remix alineada con la dieta.
5. `build_analysis_crew` y `build_recipe_crew`: Separan los dos workflows principales del coach.
6. `build_nourishbot_interface`: Expone la experiencia completa en `Gradio`.