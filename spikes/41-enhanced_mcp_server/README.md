# Practica 41 Build an Enhanced MCP Server

## Leyenda

1. FastMCP real: El servidor usa tools resources prompts y `Context` reales.
2. Cliente CLI real: El cliente se conecta por STDIO y maneja progreso mensajes y elicitation.
3. Sin Claude obligatorio: El flujo principal usa un asistente local para revisar codigo y generar documentacion.
4. Operaciones de archivos: Se cubren escritura borrado lectura de recursos y listado de directorio.
5. Prompt workflow: La documentacion se genera con `ctx.elicit` y despues se escribe mediante una tool MCP.

## Adaptacion

El laboratorio original usaba Claude como motor conversacional. En esta adaptacion el servidor y el cliente MCP son reales y el razonamiento del asistente es local para que el spike se pueda ejecutar sin claves externas. Eso permite seguir aprendiendo `Context` `elicit` `report_progress` y el patron de prompts que disparan workflows con tools.

## Roles de Archivos

- `server.py`: Servidor MCP enriquecido con tools resources y prompts.
- `client.py`: Cliente CLI con handlers de progreso mensajes y elicitation.
- `config/enhanced_mcp_config.py`: Parametros y archivo de muestra.
- `models/local_mcp_assistant.py`: Logica local para code review y documentacion.
- `orchestration/enhanced_mcp_workflow.py`: Runner programatico para la demo y los tests.
- `sample_subject.py`: Archivo base para las demostraciones.

## Instalacion

1. Activar entorno: `.\venv\Scripts\Activate.ps1`.
2. Instalar dependencias base del repo: `pip install -r requirements.txt`.
3. Instalar dependencias MCP de esta practica: `pip install fastmcp==2.12.5`.
4. Nota: la version adaptada no requiere `ANTHROPIC_API_KEY` para el camino principal.

## Verificacion

1. Compilacion: `python -m compileall spikes\41-enhanced_mcp_server`.
2. Practica: `venv\Scripts\python.exe .\spikes\41-enhanced_mcp_server\main.py`.
3. Tests: `venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_41_enhanced_mcp_server.py`.

## Cobertura

1. `write_file` y `delete_file`: Tools con progreso y logging.
2. `read_file_resource` y `list_files_resource`: Recursos de archivo y directorio.
3. `code_review`: Prompt con archivo y lenguaje detectado.
4. `documentation_generator`: Prompt con `ctx.elicit` y generacion de un `.md` separado.
5. `MCPClient`: Cliente reutilizable con menu y handlers MCP.
