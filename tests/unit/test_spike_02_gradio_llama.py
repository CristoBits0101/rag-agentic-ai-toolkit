# --- DEPENDENCIAS ---
# 1. Sys: Para anadir la ruta del spike a los imports de prueba.
# 2. Path: Para resolver la ruta absoluta del spike.
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPIKE = ROOT / "spikes" / "02-gradio_llama"

if str(SPIKE) not in sys.path:
    sys.path.insert(0, str(SPIKE))

from orchestration.gradio_llama_orchestration_steps import add_numbers
from orchestration.gradio_llama_orchestration_steps import build_sentence
from orchestration.gradio_llama_orchestration_steps import run_llama_step
from state.gradio_llama_runtime_state import runtime_state
from ui.gradio_llama_ui_builder import build_demo


def test_add_numbers_returns_direct_sum():
    assert add_numbers(2, 5) == 7
    assert add_numbers(-1, 3.5) == 2.5


def test_build_sentence_handles_validation_and_success_cases():
    assert build_sentence(1, "Software Developer", [], "la oficina", ["coded"], True) == "Selecciona al menos un pais."
    assert (
        build_sentence(1, "Software Developer", ["Canada"], "la oficina", [], True)
        == "Selecciona al menos una actividad."
    )

    sentence = build_sentence(
        3,
        "Software Developer",
        ["Canada", "Japan"],
        "la oficina",
        ["coded", "fixed bugs"],
        True,
    )

    assert "3 software developer de Canada y Japan" in sentence
    assert "coded y fixed bugs" in sentence
    assert sentence.endswith("hasta la manana.")


def test_run_llama_step_formats_prompt_and_handles_empty_input(monkeypatch):
    prompts = []

    class FakeLlama:
        def invoke(self, prompt):
            prompts.append(prompt)
            return "  salida lista  "

    runtime_state.llama_model = None
    monkeypatch.setattr(
        "orchestration.gradio_llama_orchestration_steps.get_llama_model",
        lambda: FakeLlama(),
    )

    empty_result = run_llama_step("Explicar", "   ")
    result = run_llama_step("Traducir", "  Hello world.  ")

    assert empty_result == "Escribe una pregunta o un texto."
    assert result == "salida lista"
    assert "Traduce el contenido al espanol." in prompts[0]
    assert "Hello world." in prompts[0]


def test_build_demo_returns_blocks_ready_for_launch():
    demo = build_demo()

    assert hasattr(demo, "launch")
    assert demo.title == "Practica 02 Gradio con Llama"
