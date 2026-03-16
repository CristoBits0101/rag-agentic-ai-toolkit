# --- DEPENDENCIAS ---
from config.style_finder_fashion_config import STYLE_FINDER_DEFAULT_MODEL
from orchestration.style_finder_app_orchestration import StyleFinderApp


def print_separator(title: str) -> None:
    print("=" * 60)
    print(title)
    print("=" * 60)


def run_style_finder_fashion_rag_app(model_name: str = STYLE_FINDER_DEFAULT_MODEL) -> None:
    print_separator("14. STYLE FINDER FASHION RAG APP")
    app = StyleFinderApp(model_name=model_name)
    first_example_path = next(iter(app.example_image_paths.values()))
    print(f"Model: {model_name}")
    print(f"Example: {first_example_path}")
    print()
    print(app.process_image(str(first_example_path), model_name=model_name))
