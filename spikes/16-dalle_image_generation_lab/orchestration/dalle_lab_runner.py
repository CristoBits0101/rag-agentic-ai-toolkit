# --- DEPENDENCIAS ---
from config.dalle_image_generation_config import DALL_E_2_EXERCISE_FILE_NAME
from config.dalle_image_generation_config import DALL_E_3_EXERCISE_FILE_NAME
from config.dalle_image_generation_config import EXERCISE_PROMPT
from config.dalle_image_generation_config import OUTPUTS_DIR
from orchestration.dalle_generation_orchestration import build_dalle_2_request
from orchestration.dalle_generation_orchestration import build_dalle_3_request
from orchestration.dalle_generation_orchestration import generate_default_dalle_2_cat_image
from orchestration.dalle_generation_orchestration import generate_default_dalle_3_cat_image
from orchestration.dalle_generation_orchestration import generate_image_with_openai


def print_separator(title: str) -> None:
    print("=" * 60)
    print(title)
    print("=" * 60)


def run_dalle_image_generation_lab() -> None:
    print_separator("16. DALL-E IMAGE GENERATION LAB")

    try:
        dalle_2_cat = generate_default_dalle_2_cat_image()
        dalle_3_cat = generate_default_dalle_3_cat_image()
        dalle_2_lake = generate_image_with_openai(
            build_dalle_2_request(EXERCISE_PROMPT),
            OUTPUTS_DIR / DALL_E_2_EXERCISE_FILE_NAME,
        )
        dalle_3_lake = generate_image_with_openai(
            build_dalle_3_request(EXERCISE_PROMPT),
            OUTPUTS_DIR / DALL_E_3_EXERCISE_FILE_NAME,
        )
    except RuntimeError as exc:
        print(str(exc))
        return

    print("Cat Prompt Results:")
    print(f"{dalle_2_cat.model_name}: {dalle_2_cat.output_path}")
    print(f"{dalle_3_cat.model_name}: {dalle_3_cat.output_path}")
    print("\nExercise Prompt Results:")
    print(f"{dalle_2_lake.model_name}: {dalle_2_lake.output_path}")
    print(f"{dalle_3_lake.model_name}: {dalle_3_lake.output_path}")
