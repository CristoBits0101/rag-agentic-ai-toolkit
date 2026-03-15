# --- DEPENDENCIAS ---
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from orchestration.dalle_generation_orchestration import generate_default_dalle_2_cat_image


def main() -> None:
    try:
        result = generate_default_dalle_2_cat_image()
    except RuntimeError as exc:
        print("DALL-E 2 GENERATION")
        print(str(exc))
        return

    print("DALL-E 2 GENERATION")
    print(f"Model: {result.model_name}")
    print(f"Prompt: {result.prompt}")
    print(f"Saved Image: {result.output_path}")


if __name__ == "__main__":
    main()
