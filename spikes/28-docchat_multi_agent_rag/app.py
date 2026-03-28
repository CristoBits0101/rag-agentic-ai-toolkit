# --- DEPENDENCIAS ---
from ui.docchat_ui import build_demo

if __name__ == "__main__":
    demo = build_demo()
    demo.launch(server_name="127.0.0.1", server_port=5000, share=False)