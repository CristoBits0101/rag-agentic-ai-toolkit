# --- DEPENDENCIAS ---
from pathlib import Path

SPIKE_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = SPIKE_ROOT / "data"
SERVER_AUDIT_LOG = DATA_DIR / "audit.log"
CLIENT_AUDIT_LOG = DATA_DIR / "client_audit.log"
CLIENT_PERMISSIONS_FILE = DATA_DIR / "permissions.json"
GUI_PORT = 7863
HOST_PORT = 7864

DEFAULT_PERMISSIONS = {
    "read_file": "allow",
    "write_file": "ask",
    "delete_file": "deny",
    "execute_command": "deny",
}

RISK_LEVELS = {
    "read_file": "low",
    "write_file": "medium",
    "delete_file": "high",
    "execute_command": "critical",
}

SAMPLE_FILE_NAME = "test.txt"
SAMPLE_FILE_CONTENT = "Sample content for testing\n"