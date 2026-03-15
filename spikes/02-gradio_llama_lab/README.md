# Practica 02 Gradio Llama

## Leyenda

1. Gradio: Componentes para construir la interfaz.
2. Ollama Llama: Modelo local para responder desde la practica.
3. Practica: Suma formulario y Llama en una sola interfaz.

## Roles de Archivos

- `main.py`: Punto de entrada de la practica.
- `config/gradio_llama_runtime_config.py`: Constantes de configuracion.
- `state/gradio_llama_runtime_state.py`: Estado compartido del modelo.
- `models/gradio_llama_model_gateway.py`: Acceso al modelo Ollama.
- `orchestration/gradio_llama_orchestration_steps.py`: Orquestacion de los pasos funcionales.
- `ui/gradio_llama_ui_builder.py`: Construccion de la interfaz Gradio.

## Instalacion

1. Ollama: `irm https://ollama.com/install.ps1 | iex`.
2. Llama 3.2 3B: `ollama pull llama3.2:3b`.
3. Gradio: `pip install -U gradio`.
4. LangChain Ollama: `pip install -U langchain-ollama`.

## Verificacion

1. Ollama: `ollama --version`.
2. Ollama Servidor: `ollama serve`.
3. Ollama Modelos: `ollama list`.
4. Gradio: `pip show gradio`.
