# --- DEPENDENCIAS ---
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from orchestration.vision_real_variants_orchestration import run_llava_example


def main() -> None:
    try:
        run = run_llava_example()
    except RuntimeError as exc:
        print("LLAVA VISION QUERYING")
        print(str(exc))
        return

    print("LLAVA VISION QUERYING")
    print(f"Model: {run.model_name}")
    print(f"Image Path: {run.image_path}")
    print("\nPrompt:\n")
    print(run.prompt)
    print("\nResponse:\n")
    print(run.response)


if __name__ == "__main__":
    main()
