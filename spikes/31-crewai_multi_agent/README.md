# Practica 31 CrewAI 101 Building Multi Agent AI Systems

## Leyenda

1. Agentes especializados: La practica separa investigacion redaccion y social media.
2. Pipeline secuencial: Las tareas se ejecutan en orden y cada salida alimenta a la siguiente.
3. Herramienta de busqueda: El spike usa un search tool local reproducible y deja abierta la sustitucion por Serper.
4. Enfoque CrewAI: Mantiene los conceptos de `Agent` `Task` `Crew` y `Process.sequential`.
5. Modelo local: El camino principal usa `ChatOllama` y evita `watsonx` o `OpenAI`.

## Adaptacion

Esta practica adapta el lab original al stack local del repositorio. En lugar de depender de `SerperDevTool` y `watsonx`, el spike usa un search tool local con conocimiento base reproducible y `ChatOllama` para la generacion. Tambien incluye una capa `crewai_compat` para que el flujo siga funcionando aunque `crewai` no este instalado en el entorno.

## Roles de Archivos

- `main.py`: Punto de entrada del spike.
- `config/content_pipeline_config.py`: Tema demo y base local de insights.
- `models/content_pipeline_entities.py`: Resultado tipado del pipeline.
- `models/content_llm_gateway.py`: Seleccion de modelo y construccion de `ChatOllama`.
- `models/crewai_compat.py`: Compatibilidad local con los conceptos de CrewAI.
- `models/search_tooling.py`: Herramienta de busqueda local para temas actuales.
- `orchestration/content_creation_workflow.py`: Definicion de agentes tareas crew y demo CLI.

## Instalacion

1. Activar entorno: `\.venv\Scripts\Activate.ps1`.
2. Instalar dependencias base del repo: `pip install -r requirements.txt`.
3. Arrancar `Ollama`: `ollama serve`.
4. Descargar un modelo recomendado: `ollama pull qwen2.5:7b`.
5. Alternativa de menor consumo: `ollama pull llama3.2:3b`.
6. Opcional para usar CrewAI real: `pip install -U crewai crewai-tools`.

## Verificacion

1. Compilacion: `python -m compileall spikes\31-crewai_multi_agent`.
2. Practica: `venv\Scripts\python.exe .\spikes\31-crewai_multi_agent\main.py`.
3. Tests: `venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_31_crewai_multi_agent.py`.

## Cobertura

1. `research_agent`: Investiga el tema y sintetiza hallazgos.
2. `writer_agent`: Convierte la investigacion en una entrada de blog.
3. `social_agent`: Resume el contenido en tres publicaciones cortas.
4. `Crew.kickoff`: Ejecuta el pipeline secuencial y expone salidas por tarea y uso de tokens.