# --- DEPENDENCIAS ---
import subprocess
import sys
from pathlib import Path

from config.story_real_provider_config import EDGE_TTS_VOICE

# --- AUDIO ---
def synthesize_story_with_edge_tts(
    story: str,
    output_path: str | Path,
    voice: str = EDGE_TTS_VOICE,
) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "edge_tts",
            "--voice",
            voice,
            "--text",
            story,
            "--write-media",
            str(path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0 or not path.exists():
        raise RuntimeError("edge-tts could not synthesize the requested story.")

    return path
