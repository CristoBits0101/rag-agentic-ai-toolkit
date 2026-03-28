# --- DEPENDENCIAS ---
from pathlib import Path

SPIKE_ROOT = Path(__file__).resolve().parents[1]
SAMPLE_FILE = "sample_subject.py"
SAMPLE_CODE = "def add(a: int, b: int) -> int:\n    return a + b\n"
