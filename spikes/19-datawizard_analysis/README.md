# Practica 19 DataWizard AI Powered Data Analysis

## Leyenda

1. DataWizard: Asistente de analisis de datos para usuarios no tecnicos.
2. Cache compartida: Los `DataFrame` se cargan una vez y se reutilizan entre tools.
3. Structured data tools: El spike usa herramientas de descubrimiento resumen exploracion y evaluacion de modelos.
4. Baseline sin tools: Demuestra por que una conversacion normal no basta para trabajar con CSV reales.
5. Executor agent: El flujo usa `ChatOllama` como modelo real principal y conserva un modelo demo solo para tests.

## Adaptacion

Esta practica adapta el notebook original de Skills Network pero reemplaza `OpenAI` por un modelo real local servido por `Ollama`. El repositorio sigue fijado en `langchain 0.3.27` y esa version no expone `create_agent`, por eso el spike implementa un executor controlado con tools modernas de `LangChain` y datasets locales reproducibles. El modelo demo se mantiene solo como soporte complementario para tests. La idea pedagogica se conserva: descubrir datasets resumirlos explorar `DataFrame` y evaluar modelos de clasificacion o regresion desde lenguaje natural.

## Roles de Archivos

- `main.py`: Punto de entrada de la practica.
- `config/datawizard_config.py`: Introduccion y consultas demo.
- `data/classification-dataset.csv`: Dataset local para clasificacion.
- `data/regression-dataset.csv`: Dataset local para regresion.
- `models/datawizard_entities.py`: Dataclasses para pasos y resultados del flujo.
- `models/datawizard_baseline_chat.py`: Baseline conversacional sin acceso a tools.
- `models/datawizard_ollama_gateway.py`: Seleccion de modelo y construccion del `ChatOllama` principal.
- `models/datawizard_demo_chat_model.py`: Modelo demo que decide llamadas a herramientas.
- `orchestration/datawizard_tools_orchestration.py`: Cache resolucion de datasets y tools de analisis.
- `orchestration/datawizard_agent_orchestration.py`: Executor local que recorre el bucle de tool calling.
- `orchestration/datawizard_lab_runner.py`: Runner guiado para comparar baseline y agent.

## Instalacion

1. Activar entorno: `.\venv\Scripts\Activate.ps1`.
2. Instalar dependencias base del repo: `pip install -r requirements.txt`.
3. Instalar dependencias del laboratorio: `pip install -U pandas numpy scikit-learn`.
4. Arrancar `Ollama`: `ollama serve`.
5. Descargar un modelo recomendado: `ollama pull qwen2.5:7b`.
6. Modelo compatible de menor consumo: `ollama pull llama3.2:3b`.
7. No hacen falta claves de `OpenAI`.

## Funcionamiento

1. El baseline intenta responder sin acceso a CSV ni metricas reales.
2. El agent con `ChatOllama` lista datasets locales y decide que tools necesita.
3. Las tools cargan los CSV en una cache compartida para no repetir lecturas.
4. El flujo puede resumir datasets ejecutar metodos seguros de `DataFrame` y evaluar modelos.
5. La respuesta final combina la observacion de las tools con una explicacion en lenguaje natural.

## Verificacion

1. Compilacion: `python -m compileall spikes\19-datawizard_analysis`.
2. Practica: `.\venv\Scripts\python.exe .\spikes\19-datawizard_analysis\main.py`.
3. Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_19_datawizard_analysis.py`.

## Cobertura

1. `list_csv_files`: Descubre datasets CSV locales.
2. `preload_datasets`: Carga y reutiliza datasets desde cache.
3. `get_dataset_summaries`: Resume estructura target y tipo de problema sugerido.
4. `call_dataframe_method`: Ejecuta `head` `tail` `describe` `corr` o `info`.
5. `evaluate_classification_dataset`: Entrena y mide accuracy.
6. `evaluate_regression_dataset`: Entrena y mide `r2_score` y `mean_squared_error`.
7. `execute_datawizard_query`: Ejecuta workflows multi paso con tool calling local.
8. `build_datawizard_ollama_chat_model`: Construye el modelo real principal con `Ollama`.
