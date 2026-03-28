# Practica 43 Advanced MCP Applications with Streamable HTTP Roots and Sampling

## Leyenda

1. HTTP real: El servidor se publica con `FastMCP` sobre `Streamable HTTP`.
2. Roots reales: El cliente declara un root de workspace mediante el callback `roots/list` del SDK `mcp`.
3. Sampling real: El servidor usa `ctx.sample` y el cliente responde con un callback local determinista.
4. Base client reutilizable: La logica de protocolo vive en `advanced_http_client_base.py`.
5. UIs opcionales: La GUI y el host conversacional usan `Gradio` solo si quieres lanzarlos manualmente.

## Adaptacion

El laboratorio original proponia un host con OpenAI y una GUI remota. Esta adaptacion conserva el transporte HTTP el soporte de roots y el sampling iniciado por servidor pero deja el camino principal libre de claves externas. El host conversacional funciona en modo local determinista y las UIs se mantienen como extensiones opcionales.

## Roles de Archivos

- `models/advanced_http_mcp_server.py`: Servidor HTTP con tools resources prompts y uso real de `ctx.list_roots` y `ctx.sample`.
- `models/advanced_http_client_base.py`: Cliente base con `ClientSession` y `streamablehttp_client`.
- `models/advanced_http_client_app.py`: GUI opcional para tools resources y prompts.
- `models/advanced_http_host_app.py`: Host conversacional local sobre el cliente base.
- `orchestration/advanced_http_workflow.py`: Runner programatico para tests y smoke runs.
- `workspace/`: Frontera de archivos permitidos para el root del cliente.

## Instalacion

1. Activar entorno: `./venv/Scripts/Activate.ps1`.
2. Instalar dependencias base del repo: `pip install -r requirements.txt`.
3. Dependencias opcionales de UI y LLM: `pip install httpx==0.28.1 gradio==5.49.1 openai==2.6.1`.

## Verificacion

1. Compilacion: `python -m compileall spikes\43-mcp_http_roots_sampling`.
2. Practica: `venv\Scripts\python.exe .\spikes\43-mcp_http_roots_sampling\main.py`.
3. GUI opcional: `venv\Scripts\python.exe .\spikes\43-mcp_http_roots_sampling\models\advanced_http_client_app.py http://127.0.0.1:8000 .\spikes\43-mcp_http_roots_sampling\workspace`.
4. Host opcional: `venv\Scripts\python.exe .\spikes\43-mcp_http_roots_sampling\models\advanced_http_host_app.py http://127.0.0.1:8000 .\spikes\43-mcp_http_roots_sampling\workspace`.
5. Tests: `venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_43_mcp_http_roots_sampling.py`.

## Cobertura

1. `list_roots_boundary`: Demuestra roots reales solicitados por el servidor.
2. `analyze_code`: Demuestra sampling real con callback local del cliente.
3. `MCPHTTPClient`: Centraliza `connect` `list_tools` `call_tool` `read_resource` y `get_prompt`.
4. `MCPHTTPHostApp`: Resuelve tareas comunes por lenguaje natural sin depender de claves externas.
5. `run_advanced_http_demo`: Ejercita HTTP roots sampling resources prompts y host app en una sola pasada.