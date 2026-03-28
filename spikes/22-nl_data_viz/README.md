# Practica 22 Natural Language Data Visualization Agent

## Leyenda

1. `create_pandas_dataframe_agent`: La practica usa el agente experimental de `LangChain` para consultar y visualizar un `DataFrame`.
2. Modelo real: El camino principal usa `ChatOllama` y no depende de `watsonx.ai`.
3. Graficos en disco: Los charts se guardan en `artifacts` para que la practica funcione desde terminal y no dependa de Jupyter.
4. Codigo generado: La practica extrae el Python que el agente ejecuta para responder o dibujar.
5. Visualizacion conversacional: El usuario pide consultas y plots en lenguaje natural.

## Adaptacion

Esta practica adapta el lab original sin `IBM watsonx.ai` y sin notebook. En lugar de `Granite` remoto usa `ChatOllama` local y mantiene el objetivo real del laboratorio: hablar con un CSV y generar charts con lenguaje natural. La separacion con la practica 19 es tecnica y pedagogica. La `19` construye un asistente de analisis tabular con tools propias y evaluacion de modelos. La `22` se centra en `create_pandas_dataframe_agent`, visualizacion dinamica y extraccion del codigo que el agente propone.

## Roles de Archivos

- `main.py`: Punto de entrada de la practica.
- `config/data_visualization_agent_config.py`: Dataset prompts y lista de consultas visuales.
- `data/student-mat.csv`: Dataset local de estudiantes para analisis y graficos.
- `models/data_visualization_entities.py`: Resultado tipado de cada consulta del agente.
- `models/data_visualization_ollama_gateway.py`: Seleccion de modelo y construccion del `ChatOllama` principal.
- `orchestration/data_visualization_dataset_orchestration.py`: Carga del dataset y gestion de artifacts.
- `orchestration/data_visualization_agent_orchestration.py`: Construccion del agente generacion de prompts y captura del codigo.
- `orchestration/data_visualization_lab_runner.py`: Runner guiado con consultas textuales y graficos.

## Instalacion

1. Activar entorno: `.\venv\Scripts\Activate.ps1`.
2. Instalar dependencias base del repo: `pip install -r requirements.txt`.
3. Instalar dependencias del laboratorio: `pip install -U langchain-experimental matplotlib seaborn`.
4. Arrancar `Ollama`: `ollama serve`.
5. Descargar un modelo recomendado: `ollama pull qwen2.5:7b`.
6. Modelo compatible de menor consumo: `ollama pull llama3.2:3b`.

## Funcionamiento

1. La practica carga el dataset local `student-mat.csv` en un `DataFrame`.
2. `create_pandas_dataframe_agent` crea un agente con acceso al `DataFrame` y a un `python_repl_ast`.
3. Las consultas simples devuelven respuestas textuales sobre el CSV.
4. Las consultas visuales anaden una ruta de guardado al prompt para que el agente escriba el chart en `artifacts`.
5. La respuesta del agente incluye `intermediate_steps` y la practica extrae el Python usado para cada respuesta o grafico.

## Verificacion

1. Compilacion: `python -m compileall spikes\22-nl_data_viz`.
2. Practica: `.\venv\Scripts\python.exe .\spikes\22-nl_data_viz\main.py`.
3. Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_22_nl_data_viz.py`.

## Cobertura

1. `load_student_dataframe`: Carga el CSV local del laboratorio.
2. `build_data_visualization_agent`: Construye el agente real de `LangChain`.
3. `build_query_with_artifact_path`: Fuerza el guardado de charts en disco.
4. `extract_generated_code`: Extrae el Python usado por el agente.
5. `invoke_data_visualization_query`: Ejecuta consultas y devuelve salida codigo y artifact.
6. `run_natural_language_data_visualization_lab`: Recorre preguntas simples visualizaciones y ejercicios.
