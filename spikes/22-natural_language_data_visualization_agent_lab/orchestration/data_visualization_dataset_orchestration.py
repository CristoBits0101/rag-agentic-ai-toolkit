# --- DEPENDENCIAS ---
from pathlib import Path
import re

import pandas as pd

from config.data_visualization_agent_config import ARTIFACTS_DIR
from config.data_visualization_agent_config import DATA_PATH


def load_student_dataframe() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH)


def ensure_artifacts_dir() -> Path:
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    return ARTIFACTS_DIR


def clear_generated_artifacts() -> None:
    artifacts_dir = ensure_artifacts_dir()
    for artifact_path in artifacts_dir.glob("*.png"):
        artifact_path.unlink()


def build_artifact_path(slug: str) -> Path:
    safe_slug = re.sub(r"[^a-zA-Z0-9_-]+", "_", slug).strip("_") or "chart"
    return ensure_artifacts_dir() / f"{safe_slug}.png"
