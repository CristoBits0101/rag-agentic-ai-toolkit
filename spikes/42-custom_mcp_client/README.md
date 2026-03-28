# Practica 42 Build a Custom MCP Client with Python

## Leyenda

1. MCP de bajo nivel: El cliente usa `ClientSession` y `stdio_client` del SDK `mcp`.
2. FastMCP real: El servidor se construye con `FastMCP` y expone tools resources y prompts.
3. CLI minima: El cliente permite descubrir tools recursos prompts y ejecutarlos desde terminal.
4. Recursos reales: El servidor expone archivos del directorio `resources` por URI template.
5. Sin dependencias externas: Todo el flujo principal es local y reproducible.

## Adaptacion

El laboratorio original estaba ya muy orientado a un entorno local. Esta adaptacion conserva el mismo planteamiento con `mcp` y `fastmcp` reales pero lo empaqueta como un spike del repositorio con un runner programatico adicional para pruebas automatizadas y smoke tests.

## Roles de Archivos

- `mcp_server.py`: Servidor FastMCP con tool de eco tool de escritura resource template y prompt template.
- `mcp_client.py`: Cliente MCP con `ClientSession` y transporte STDIO.
- `main.py`: Runner programatico para validar las operaciones clave sin usar la CLI interactiva.
- `resources/project_info.txt`: Recurso de texto del laboratorio.
- `resources/README.md`: Recurso markdown del laboratorio.
- `resources/notes.txt`: Recurso adicional para probar templates dinamicos.

## Instalacion

1. Activar entorno: `.\venv\Scripts\Activate.ps1`.
2. Instalar dependencias base del repo: `pip install -r requirements.txt`.
3. Instalar dependencias MCP de esta practica: `pip install mcp==1.16.0 fastmcp==2.12.5`.

## Verificacion

1. Compilacion: `python -m compileall spikes\42-custom_mcp_client`.
2. Practica: `venv\Scripts\python.exe .\spikes\42-custom_mcp_client\main.py`.
3. Cliente interactivo: `venv\Scripts\python.exe .\spikes\42-custom_mcp_client\mcp_client.py .\spikes\42-custom_mcp_client\mcp_server.py`.
4. Tests: `venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_42_custom_mcp_client.py`.

## Cobertura

1. `connect`: Handshake STDIO completo con `ClientSession`.
2. `list_tools` y `call_tool`: Descubrimiento e invocacion de tools.
3. `list_resources` y `read_resource`: Lectura de recursos via URIs.
4. `list_prompts` y `get_prompt`: Uso de prompt templates renderizados.
5. `run_custom_client_demo`: Flujo no interactivo para pruebas automatizadas.
