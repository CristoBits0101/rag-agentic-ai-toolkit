# --- DEPENDENCIAS ---
# 1. Configuracion: Para obtener host y puerto de la practica.
# 2. Interfaz: Para construir la app de Gradio.
from config.icebreaker_config import SERVER_HOST
from config.icebreaker_config import SERVER_PORT
from ui.icebreaker_ui import build_interface

# Construye la interfaz principal de la practica.
demo = build_interface()

if __name__ == "__main__":
    # Lanza la practica con la configuracion definida para este spike.
    demo.launch(server_name=SERVER_HOST, server_port=SERVER_PORT)
