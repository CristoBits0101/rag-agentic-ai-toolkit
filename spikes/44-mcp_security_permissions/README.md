# Practica 44 MCP Security with Permissions and Elicitation

## Leyenda

1. Permisos reales del cliente: El cliente aplica politicas `allow` `deny` y `ask` antes de ejecutar tools.
2. Elicitation real del servidor: Las operaciones sensibles usan `ctx.elicit` con esquemas estructurados.
3. Auditoria doble: El servidor registra operaciones sensibles y el cliente registra decisiones de seguridad.
4. Host conversacional local: El asistente usa una capa determinista para no depender de claves externas.
5. GUI opcional: La app visual existe pero queda fuera del camino principal de validacion.

## Adaptacion

El laboratorio original proponia un host con GPT y flujos de aprobacion en UI. Esta adaptacion conserva los patrones de permisos auditoria y elicitation pero deja el runner principal totalmente local y reproducible. El punto fuerte del spike es que la aprobacion del cliente y la solicitud estructurada del servidor son reales.

## Roles de Archivos

- `models/permission_mcp_server.py`: Servidor STDIO con herramientas de distinto riesgo y recursos de auditoria.
- `models/permission_client_base.py`: Cliente base con permisos auditoria y callback real de elicitation.
- `models/permission_client_app.py`: GUI opcional para explorar tools recursos prompts y politicas.
- `models/permission_host_app.py`: Host conversacional con aprobacion humana y evaluacion de riesgo.
- `orchestration/permission_workflow.py`: Demo programatica usada por tests y smoke runs.
- `data/`: Archivos de prueba y logs del spike.

## Instalacion

1. Activar entorno: `./venv/Scripts/Activate.ps1`.
2. Instalar dependencias base del repo: `pip install -r requirements.txt`.
3. Dependencia opcional de UI: `pip install gradio==5.49.1 openai==2.6.1`.

## Verificacion

1. Compilacion: `python -m compileall spikes\44-mcp_security_permissions`.
2. Practica: `venv\Scripts\python.exe .\spikes\44-mcp_security_permissions\main.py`.
3. GUI opcional: `venv\Scripts\python.exe .\spikes\44-mcp_security_permissions\models\permission_client_app.py .\spikes\44-mcp_security_permissions\models\permission_mcp_server.py`.
4. Host opcional: `venv\Scripts\python.exe .\spikes\44-mcp_security_permissions\models\permission_host_app.py .\spikes\44-mcp_security_permissions\models\permission_mcp_server.py`.
5. Tests: `venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_44_mcp_security_permissions.py`.

## Cobertura

1. `check_permission`: Resuelve politicas por tool y por argumentos concretos.
2. `call_tool_with_permission`: Bloquea aprueba o solicita confirmacion antes de llamar al servidor.
3. `ctx.elicit`: Solicita aprobaciones estructuradas desde el servidor para escritura borrado y comandos simulados.
4. `security_review`: Expone un prompt reusable para revisar operaciones sensibles.
5. `run_permission_demo`: Cubre permisos auditoria elicitation host conversacional y recursos del servidor.