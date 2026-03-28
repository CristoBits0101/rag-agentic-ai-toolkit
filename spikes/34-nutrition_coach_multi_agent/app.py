# --- DEPENDENCIAS ---
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from ui.nourishbot_ui import launch_nourishbot_interface


if __name__ == "__main__":
    launch_nourishbot_interface()