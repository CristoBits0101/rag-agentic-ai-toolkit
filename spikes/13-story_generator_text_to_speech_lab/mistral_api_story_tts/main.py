# --- DEPENDENCIAS ---
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from config.story_tts_config import DEFAULT_TOPIC
from orchestration.story_real_variants_orchestration import run_mistral_api_story_variant


def main() -> None:
    try:
        run = run_mistral_api_story_variant(DEFAULT_TOPIC)
    except RuntimeError as exc:
        print("MISTRAL API STORY TTS")
        print(str(exc))
        return

    if not run:
        print("Please provide a valid topic.")
        return

    print("MISTRAL API STORY TTS")
    print(f"Topic: {run.topic}")
    print(f"LLM Provider: {run.llm_provider}")
    print(f"LLM Model: {run.llm_model}")
    print(f"TTS Provider: {run.tts_provider}")
    print(f"Audio Path: {run.output_path}")
    print("\nPrompt:\n")
    print(run.prompt)
    print("\nGenerated Story:\n")
    print(run.story)


if __name__ == "__main__":
    main()
