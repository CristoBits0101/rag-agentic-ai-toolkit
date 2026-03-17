# Practica 23 Natural Language SQL Agent

## Leyenda

1. `create_sql_agent`: La practica usa el toolkit SQL de `LangChain` para traducir lenguaje natural a consultas SQL.
2. Modelo real: El camino principal usa `ChatOllama` y no depende de `watsonx.ai`.
3. Base reproducible: El laboratorio genera `artifacts/chinook.db` a partir del seed local `data/chinook.sql`.
4. SQL inspeccionable: La practica extrae las sentencias SQL generadas desde `intermediate_steps`.
5. Esquema relacional: El agente razona sobre tablas relaciones y joins del dataset Chinook.

## Adaptacion

Esta practica adapta el lab original sin `MySQL` gestionado y sin `IBM watsonx.ai`. En lugar de depender de un servicio externo levanta una base `SQLite` local a partir del seed oficial de Chinook y usa `ChatOllama` como modelo principal. La separacion con la practica 22 es tecnica y pedagogica. La `22` trabaja con `DataFrame agents` sobre CSV y visualizacion con `pandas`. La `23` se centra en `SQLDatabase Toolkit` consulta sobre un esquema relacional y extraccion del SQL que el agente decide ejecutar.

## Roles de Archivos

- `main.py`: Punto de entrada de la practica.
- `config/natural_language_sql_agent_config.py`: Rutas prompts y consultas de ejemplo.
- `data/chinook.sql`: Seed SQL oficial de Chinook para construir la base local.
- `models/natural_language_sql_entities.py`: Resultado tipado de cada consulta del agente SQL.
- `models/natural_language_sql_ollama_gateway.py`: Seleccion de modelo y construccion del `ChatOllama` principal.
- `orchestration/natural_language_sql_database_orchestration.py`: Inicializacion de `SQLite` listado de tablas y recuentos basicos.
- `orchestration/natural_language_sql_agent_orchestration.py`: Construccion del agente y extraccion del SQL generado.
- `orchestration/natural_language_sql_lab_runner.py`: Runner guiado con preguntas de ejemplo sobre Chinook.

## Instalacion

1. Activar entorno: `.\venv\Scripts\Activate.ps1`.
2. Instalar dependencias base del repo: `pip install -r requirements.txt`.
3. Instalar dependencia del toolkit SQL si hace falta: `pip install -U langchain-community`.
4. Arrancar `Ollama`: `ollama serve`.
5. Descargar un modelo recomendado: `ollama pull qwen2.5:7b`.
6. Modelo compatible de menor consumo: `ollama pull llama3.2:3b`.

## Funcionamiento

1. La practica copia el seed `chinook.sql` dentro del repo y construye `artifacts/chinook.db` si no existe.
2. `SQLDatabase` expone la base `SQLite` al agente de `LangChain`.
3. `create_sql_agent` crea un agente real con tools SQL y `ChatOllama`.
4. Cada consulta se formula en lenguaje natural y el agente decide listar tablas validar queries y ejecutar `SELECT`.
5. La practica recupera el SQL real desde `intermediate_steps` para que puedas inspeccionarlo.

## Verificacion

1. Compilacion: `python -m compileall spikes\23-natural_language_sql_agent_lab`.
2. Practica: `.\venv\Scripts\python.exe .\spikes\23-natural_language_sql_agent_lab\main.py`.
3. Tests: `.\venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_23_natural_language_sql_agent.py`.

## Cobertura

1. `ensure_chinook_database`: Genera o reutiliza la base local desde el seed SQL.
2. `build_chinook_sql_database`: Construye el `SQLDatabase` de `LangChain`.
3. `build_natural_language_sql_agent`: Crea el agente SQL real con `tool-calling`.
4. `extract_sql_statements`: Extrae las consultas SQL desde los pasos intermedios.
5. `invoke_natural_language_sql_query`: Ejecuta preguntas y devuelve respuesta SQL y tools usadas.
6. `run_natural_language_sql_lab`: Recorre consultas guiadas sobre Chinook.
