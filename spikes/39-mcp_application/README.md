# Practica 39 Build an MCP Application

## Leyenda

1. Multi servidor real: La practica usa `MultiServerMCPClient` de `langchain-mcp-adapters`.
2. Dos transportes: Context7 compatible por HTTP y Met Museum compatible por STDIO.
3. Agente con memoria: El agente conserva el historial de la sesion para responder preguntas sobre el contexto previo.
4. Sin claves obligatorias: El loop principal usa un agente local determinista para mantener la practica reproducible.
5. Arquitectura equivalente: La configuracion coincide con el patron de host MCP con varias sesiones y herramientas compartidas.

## Adaptacion

El laboratorio original proponia un agente ReAct con GPT-5. En esta adaptacion el cliente multi servidor y los tools MCP son reales pero el razonamiento del agente por defecto es local y determinista para no depender de credenciales externas. La estructura de transportes y la carga de tools con `MultiServerMCPClient` se mantienen intactas. Si quieres sustituir el agente local por un modelo real puedes hacerlo sobre la misma base.

## Roles de Archivos

- `main.py`: Runner principal de la aplicacion MCP.
- `config/mcp_application_config.py`: Catalogo de documentacion y objetos del museo.
- `models/context7_http_server.py`: Servidor HTTP compatible con Context7.
- `models/met_museum_server.py`: Servidor MCP local con datos del museo.
- `models/met_museum_stdio_server.py`: Entry point STDIO del servidor del museo.
- `models/mcp_application_agent.py`: Agente con memoria y seleccion local de tools.
- `orchestration/mcp_application_workflow.py`: Ciclo de vida de servidores y cliente multi servidor.

## Instalacion

1. Activar entorno: `.\venv\Scripts\Activate.ps1`.
2. Instalar dependencias base del repo: `pip install -r requirements.txt`.
3. Instalar dependencias MCP de esta practica: `pip install fastmcp==2.12.5 mcp==1.16.0 langchain-mcp-adapters==0.1.9`.
4. Opcional para usar un agente real: `pip install langchain-openai==0.3.33` y configurar `OPENAI_API_KEY`.

## Verificacion

1. Compilacion: `python -m compileall spikes\39-mcp_application`.
2. Practica: `venv\Scripts\python.exe .\spikes\39-mcp_application\main.py`.
3. Tests: `venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_39_mcp_application.py`.

## Cobertura

1. `MultiServerMCPClient`: Carga tools desde dos servidores MCP con transportes distintos.
2. `local_context7_http_server`: Arranca el servidor de documentacion por HTTP en segundo plano.
3. `SessionPersistentMcpAgent`: Responde con memoria de sesion y uso explicito de tools.
4. `run_mcp_application_demo`: Demuestra introduccion consulta documental consulta de museo y memoria.
