# --- DEPENDENCIAS ---
# 1. Sys: Para anadir la ruta del spike a los imports de prueba.
# 2. Path: Para resolver la ruta absoluta del spike.
import sys
from pathlib import Path

from langchain_core.runnables import RunnableLambda

ROOT = Path(__file__).resolve().parents[2]
SPIKE = ROOT / "spikes" / "01-prompting_lcel"

if str(SPIKE) not in sys.path:
    sys.path.insert(0, str(SPIKE))

import main as prompting_main
from models.prompting_model_gateway import llm_model
from orchestration.prompting_orchestration_lcel import build_lcel_chain


def test_llm_model_merges_default_params_and_invokes_model(monkeypatch):
    captured = {}

    class FakeLlm:
        def invoke(self, prompt_txt):
            captured["prompt"] = prompt_txt
            return "ok"

    def fake_build_llm(max_new_tokens, temperature, top_p, top_k):
        captured["params"] = {
            "max_new_tokens": max_new_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
        }
        return FakeLlm()

    monkeypatch.setattr("models.prompting_model_gateway.build_llm", fake_build_llm)

    result = llm_model("Hola mundo", {"temperature": 0.1, "max_new_tokens": 32})

    assert result == "ok"
    assert captured["prompt"] == "Hola mundo"
    assert captured["params"] == {
        "max_new_tokens": 32,
        "temperature": 0.1,
        "top_p": 0.2,
        "top_k": 1,
    }


def test_build_lcel_chain_formats_variables_with_patched_runnable(monkeypatch):
    fake_llm = RunnableLambda(lambda prompt_value: prompt_value.to_string())
    monkeypatch.setattr(
        "orchestration.prompting_orchestration_lcel.build_lcel_llm",
        lambda: fake_llm,
    )

    chain = build_lcel_chain("Hola {name}.")
    result = chain.invoke({"name": "Ana"})

    assert "Hola Ana." in result


def test_run_all_exercises_executes_expected_steps(monkeypatch):
    call_order = []

    monkeypatch.setattr(prompting_main, "run_greeting_example", lambda: call_order.append("greeting"))
    monkeypatch.setattr(prompting_main, "run_baseline", lambda: call_order.append("baseline"))
    monkeypatch.setattr(prompting_main, "run_task_prompts", lambda: call_order.append("task_prompts"))
    monkeypatch.setattr(
        prompting_main,
        "run_one_shot_prompts",
        lambda *args: call_order.append(("one_shot", len(args))),
    )
    monkeypatch.setattr(prompting_main, "run_few_shot", lambda: call_order.append("few_shot"))
    monkeypatch.setattr(
        prompting_main,
        "run_exercise_3_step_by_step",
        lambda: call_order.append("step_by_step"),
    )
    monkeypatch.setattr(
        prompting_main,
        "run_exercise_4_lcel",
        lambda: call_order.append("lcel"),
    )
    monkeypatch.setattr(
        prompting_main,
        "run_exercise_5_reasoning_and_reviews",
        lambda: call_order.append("reasoning"),
    )

    prompting_main.run_all_exercises()

    assert call_order == [
        "greeting",
        "baseline",
        "task_prompts",
        ("one_shot", 3),
        "few_shot",
        "step_by_step",
        "lcel",
        "reasoning",
    ]
