# --- DEPENDENCIAS ---
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPIKE = ROOT / "spikes" / "32-meal_grocery_planner"

if str(SPIKE) not in sys.path:
    sys.path.insert(0, str(SPIKE))

for module_name in list(sys.modules):
    if module_name == "models" or module_name.startswith("models."):
        sys.modules.pop(module_name)
    if module_name == "orchestration" or module_name.startswith("orchestration."):
        sys.modules.pop(module_name)
    if module_name == "config" or module_name.startswith("config."):
        sys.modules.pop(module_name)
    if module_name == "leftover" or module_name.startswith("leftover"):
        sys.modules.pop(module_name)

from models.meal_grocery_entities import MealType
from orchestration.meal_grocery_workflow import build_complete_grocery_crew
from orchestration.meal_grocery_workflow import build_health_focused_crew
from orchestration.meal_grocery_workflow import build_sample_weekly_grocery_plan
from orchestration.meal_grocery_workflow import build_sample_weekly_plan


class FakeResponse:
    def __init__(self, content: str):
        self.content = content


class FakeModel:
    def invoke(self, prompt: str):
        lowered = prompt.lower()
        if "leftover" in lowered:
            return FakeResponse("Reuse cooked ingredients in lunch bowls and quick wraps.")
        if "budget analysis" in lowered or "money saving" in lowered:
            return FakeResponse("The plan stays close to budget and benefits from store brand pantry staples.")
        if "nutritional content" in lowered:
            return FakeResponse("Approximate macros are balanced with moderate protein complex carbs and fiber.")
        if "compile a concise but structured final guide" in lowered:
            return FakeResponse("This guide combines the recipe shopping plan budget analysis and leftovers.")
        return FakeResponse("The recipe fits the requested skill level and dietary restrictions.")


def test_complete_grocery_crew_returns_five_outputs():
    crew, _ = build_complete_grocery_crew(model=FakeModel())
    result = crew.kickoff(
        inputs={
            "meal_name": "Chicken Stir Fry",
            "servings": 4,
            "budget": "$25",
            "dietary_restrictions": ["no nuts", "low sodium"],
            "cooking_skill": "beginner",
        }
    )
    assert len(result.tasks_output) == 5
    assert "guide" in result.raw.lower() or "compiled" in result.raw.lower()


def test_health_focused_crew_adds_nutrition_stage():
    crew, _ = build_health_focused_crew(model=FakeModel())
    result = crew.kickoff(
        inputs={
            "meal_name": "Quinoa Buddha Bowl",
            "servings": 2,
            "budget": "$20",
            "dietary_restrictions": ["vegetarian", "high protein"],
            "cooking_skill": "intermediate",
        }
    )
    assert len(result.tasks_output) == 6


def test_weekly_models_are_constructed_correctly():
    weekly_plan = build_sample_weekly_plan()
    weekly_grocery_plan = build_sample_weekly_grocery_plan()
    assert weekly_plan.daily_meals
    assert weekly_grocery_plan.bulk_items
    assert MealType.DINNER.value == "dinner"