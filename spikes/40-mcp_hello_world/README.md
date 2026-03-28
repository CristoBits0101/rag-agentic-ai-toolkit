# Practica 40 Hello World of MCP Servers

## Leyenda

1. FastMCP real: La practica usa `FastMCP` y `Client` reales para tools resources y prompts.
2. Cuatro modos: Demuestra transporte in-memory HTTP STDIO y un escenario multi servidor.
3. Recursos y prompts: Incluye recursos template y lectura real de archivos ademas de un prompt reusable.
4. Multi servidor: Carga tools por `langchain-mcp-adapters` desde HTTP y STDIO al mismo tiempo.
5. ReAct reproducible: El paso final simula el transcript del agente para evitar dependencia de claves externas.

## Adaptacion

El laboratorio original combinaba FastMCP con clientes de alto y bajo nivel y terminaba con un agente LangGraph. En esta adaptacion los servidores y clientes son reales y el ultimo paso multi servidor usa `MultiServerMCPClient`. El bloque del agente se representa con un transcript deterministico basado en tool calls reales para mantener la practica local y testeable.

## Roles de Archivos

- `main.py`: Runner principal del laboratorio.
- `config/hello_mcp_config.py`: Puerto y archivos de datos del ejemplo.
- `models/hello_world_mcp_server.py`: Servidor MCP con tools resources y prompts.
- `models/hello_world_stdio_server.py`: Entry point STDIO del servidor.
- `orchestration/hello_mcp_workflow.py`: Ejecucion de las variantes in-memory HTTP STDIO y multi servidor.
- `data/documents`: Archivos reales expuestos por recursos MCP.

## Instalacion

1. Activar entorno: `.\venv\Scripts\Activate.ps1`.
2. Instalar dependencias base del repo: `pip install -r requirements.txt`.
3. Instalar dependencias MCP de esta practica: `pip install fastmcp==2.12.5 mcp==1.16.0 langchain-mcp-adapters==0.1.9`.

## Verificacion

1. Compilacion: `python -m compileall spikes\40-mcp_hello_world`.
2. Practica: `venv\Scripts\python.exe .\spikes\40-mcp_hello_world\main.py`.
3. Tests: `venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_40_mcp_hello_world.py`.

## Cobertura

1. `call_add_tool_in_memory`: Cliente contra servidor en el mismo proceso.
2. `call_add_tool_http`: Servidor MCP por HTTP con `StreamableHttpTransport`.
3. `call_add_tool_stdio`: Servidor MCP por subprocess con `StdioTransport`.
4. `read_template_resource` y `read_disk_resource`: Recursos template y archivo real.
5. `get_review_prompt`: Prompt MCP reusable.
6. `run_multi_server_demo`: Carga tools desde dos servidores a la vez.
