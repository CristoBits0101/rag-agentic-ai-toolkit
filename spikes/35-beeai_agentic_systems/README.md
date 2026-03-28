# Practica 35 Building Agentic AI Systems with the BeeAI Framework

## Leyenda

1. Tutorial progresivo: La practica cubre conversacion plantillas salida estructurada agentes herramientas requisitos y multiagentes.
2. BeeAI compatible: El spike reproduce los conceptos de `ChatModel`, `RequirementAgent`, `ThinkTool`, `ConditionalRequirement` y `HandoffTool` con una capa local ejecutable.
3. Sin bloqueo externo: El camino principal no exige credenciales de OpenAI ni watsonx para poder aprender los patrones.
4. Scripts por seccion: Se incluyen `t1.py` a `t12.py` para reflejar el material paso a paso.
5. Enfoque productivo: La practica muestra trazabilidad aprobaciones y control declarativo de herramientas.

## Adaptacion

El laboratorio original dependia del paquete `beeai-framework`, de modelos remotos y de servicios externos. En esta adaptacion el repositorio mantiene la semantica de BeeAI mediante una capa local compatible y determinista. La sintaxis conceptual se conserva y la ejecucion por defecto es reproducible. El README documenta tambien las dependencias opcionales si quieres contrastar el spike con el framework real fuera del repo.

## Roles de Archivos

- `main.py`: Runner principal del tutorial.
- `t1.py` a `t12.py`: Scripts equivalentes a las secciones del laboratorio.
- `config/beeai_lab_config.py`: Prompts consultas base snippets y clima local.
- `models/beeai_compat.py`: Capa local compatible con los conceptos centrales de BeeAI.
- `models/beeai_entities.py`: Modelos `Pydantic` para salidas estructuradas y resumenes.
- `orchestration/beeai_tutorial_workflow.py`: Implementacion de todos los ejemplos del tutorial.

## Instalacion

1. Activar entorno: `.\venv\Scripts\Activate.ps1`.
2. Instalar dependencias base del repo: `pip install -r requirements.txt`.
3. Opcional para contrastar con el framework real fuera del camino principal: `pip install openai==1.99.9 beeai-framework[wikipedia]==0.1.35 pydantic==2.11.7 pydantic-core==2.33.2`.
4. Opcional si quieres sustituir la capa local por modelos remotos en tus propias variantes: configura credenciales de `watsonx.ai` u `OpenAI` fuera del repo.

## Verificacion

1. Compilacion: `python -m compileall spikes\35-beeai_agentic_systems`.
2. Practica: `venv\Scripts\python.exe .\spikes\35-beeai_agentic_systems\main.py`.
3. Tests: `venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_35_beeai_agentic_systems.py`.

## Cobertura

1. `configure_environment`: Replica la configuracion inicial de entorno.
2. `basic_chat_example`: Presenta el patron base de conversacion.
3. `SimplePromptTemplate` y `prompt_template_example`: Reutilizan prompts con variables.
4. `structured_output_example`: Genera un `BusinessPlan` tipado.
5. `RequirementAgent`: Muestra el salto de chat simple a agente controlado.
6. `WikipediaTool` `ThinkTool` y `OpenMeteoTool`: EnseÃ±an herramientas y razonamiento explicito.
7. `ConditionalRequirement` y `AskPermissionRequirement`: Muestran control declarativo y human in the loop.
8. `SimpleCalculatorTool`: EnseÃ±a creacion de herramientas custom.
9. `HandoffTool` y `multi_agent_travel_planner_with_language`: Construyen el ejemplo multiagente de viaje.