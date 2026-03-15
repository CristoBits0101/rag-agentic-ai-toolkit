# --- DEPENDENCIAS ---
# 1.           Bootstrap: Para aplicar la configuracion de warnings.
# 2.        Configuracion: Para obtener host y puerto de la interfaz.
# 3.           Interfaz: Para construir la aplicacion de Gradio.
from bootstrap.rag_bootstrap import configure_warnings
from config.rag_config import SERVER_HOST
from config.rag_config import SERVER_PORT
from ui.rag_ui import build_interface

# Aplica la configuracion comun antes de crear la interfaz.
configure_warnings()

# Construye la interfaz principal del spike.
rag_application = build_interface()

# Ejecuta la interfaz solo si este archivo se lanza directamente.
if __name__ == "__main__":
    # Lanza la aplicacion usando el host y puerto definidos para la practica.
    rag_application.launch(server_name=SERVER_HOST, server_port=SERVER_PORT)
