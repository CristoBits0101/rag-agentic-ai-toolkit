# Practica 38 Run Existing MCP Servers

## Leyenda

1. Transporte real: La practica usa `FastMCP Client` con `StdioTransport` y `StreamableHttpTransport`.
2. Context7 compatible: El spike incluye un servidor local que replica `resolve-library-id` y `query-docs`.
3. Sin dependencia remota: El camino principal no requiere internet para demostrar MCP.
4. Mismo flujo: La llamada a tools es identica tanto para STDIO como para HTTP.
5. Referencia real: El README deja documentados el paquete `npx` y la URL reales de Context7.

## Adaptacion

El laboratorio original dependia del servidor remoto de Context7 y de `npx @upstash/context7-mcp`. En esta adaptacion el repositorio usa `fastmcp` real para crear un servidor local compatible con las dos tools clave. Eso permite practicar el mismo flujo de transporte y llamadas asincronas con una ejecucion reproducible. El `README` tambien conserva las referencias a los endpoints reales para contraste.

## Roles de Archivos

- `main.py`: Runner principal del laboratorio.
- `config/mcp_existing_servers_config.py`: Catalogo local de librerias y parametros de transporte.
- `models/context7_compat_server.py`: Servidor `FastMCP` compatible con Context7.
- `models/context7_stdio_server.py`: Entry point STDIO para lanzar el servidor como subprocess.
- `orchestration/mcp_existing_servers_workflow.py`: Configuracion de transportes y llamadas asincronas.

## Instalacion

1. Activar entorno: `.\venv\Scripts\Activate.ps1`.
2. Instalar dependencias base del repo: `pip install -r requirements.txt`.
3. Instalar dependencias MCP de esta practica: `pip install fastmcp==2.12.5 mcp==1.16.0`.
4. Opcional para usar el servidor real via `npx`: instalar Node.js y ejecutar `npx -y @upstash/context7-mcp`.

## Verificacion

1. Compilacion: `python -m compileall spikes\38-mcp_existing_servers`.
2. Practica: `venv\Scripts\python.exe .\spikes\38-mcp_existing_servers\main.py`.
3. Tests: `venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_38_mcp_existing_servers.py`.

## Cobertura

1. `build_stdio_transport`: Configura el cliente para un servidor local por STDIO.
2. `build_http_transport`: Configura el cliente para un servidor MCP por HTTP streaming.
3. `list_tools_with_transport`: Lista las tools disponibles de forma asincrona.
4. `resolve_and_query_fastmcp`: Resuelve el `libraryId` y luego recupera documentacion.
5. `run_existing_mcp_servers_demo`: Ejecuta el mismo flujo sobre ambos transportes.
