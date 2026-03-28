# Practica 37 Build a Multi Agent Chatbot with AG2 for Healthcare

## Leyenda

1. Multiagente sanitario: La practica divide la consulta entre diagnostico farmacia y decision final.
2. Basada en AG2 compatible: Usa una capa local inspirada en `ConversableAgent`, `GroupChat` y `GroupChatManager`.
3. Flujo sanitario claro: El paciente inicia la consulta y el manager coordina la secuencia de agentes.
4. Ejercicio incluido: Se aÃ±ade el chatbot de salud mental con analisis emocional y recomendaciones de cuidado.
5. Aviso pedagÃ³gico: La salida no sustituye atencion medica profesional.

## Adaptacion

El laboratorio original dependia de GPT remoto y de `AutoGen`. Esta adaptacion conserva la arquitectura multiagente y los roles clinicos pero la ejecuta con una capa local reproducible. El foco es aprender comunicacion entre agentes y orquestacion estructurada no ofrecer diagnostico real.

## Roles de Archivos

- `main.py`: Runner principal del chatbot sanitario.
- `config/healthcare_chatbot_config.py`: Configuracion de sintomas y prompts demo.
- `models/ag2_compat.py`: Capa local compatible con AG2 para este spike.
- `orchestration/healthcare_chatbot_workflow.py`: Construccion del sistema AutoMed y del ejercicio de salud mental.

## Instalacion

1. Activar entorno: `.\venv\Scripts\Activate.ps1`.
2. Instalar dependencias base del repo: `pip install -r requirements.txt`.
3. Opcional para contrastar con AG2 real fuera del camino principal: `pip install autogen==0.7 openai==1.64.0 python-dotenv==1.1.0`.

## Verificacion

1. Compilacion: `python -m compileall spikes\37-ag2_healthcare_chatbot`.
2. Practica: `venv\Scripts\python.exe .\spikes\37-ag2_healthcare_chatbot\main.py`.
3. Tests: `venv\Scripts\python.exe -m pytest -c NUL --rootdir . tests\unit\test_spike_37_ag2_healthcare_chatbot.py`.

## Cobertura

1. `build_healthcare_agents`: Crea paciente diagnostico farmacia y consulta final.
2. `run_automed_consultation`: Ejecuta la consulta sanitaria multiagente.
3. `run_mental_health_chatbot`: Resuelve el ejercicio de salud mental con dos especialistas.
4. `run_healthcare_demo`: Muestra ambos ejemplos de forma seguida.