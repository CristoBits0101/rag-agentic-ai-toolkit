# --- DEPENDENCIAS ---
# 1.        Configuracion: Para obtener host y puerto de la practica.
# 2.           Interfaz: Para construir la app de Gradio.
from config.gradio_llama_runtime_config import SERVER_HOST
from config.gradio_llama_runtime_config import SERVER_PORT
from ui.gradio_llama_ui_builder import build_demo

# Construye la interfaz principal de la practica.
demo = build_demo()

if __name__ == "__main__":
    # Lanza la practica en local usando la configuracion definida arriba.
    demo.launch(server_name=SERVER_HOST, server_port=SERVER_PORT)
