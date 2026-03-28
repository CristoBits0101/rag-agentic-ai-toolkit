# --- DEPENDENCIAS ---
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPIKE = ROOT / "spikes" / "34-nutrition_coach_multi_agent"

if str(SPIKE) not in sys.path:
    sys.path.insert(0, str(SPIKE))

for module_name in list(sys.modules):
    if module_name == "models" or module_name.startswith("models."):
        sys.modules.pop(module_name)
    if module_name == "orchestration" or module_name.startswith("orchestration."):
        sys.modules.pop(module_name)
    if module_name == "config" or module_name.startswith("config."):
        sys.modules.pop(module_name)
    if module_name == "data" or module_name.startswith("data."):
        sys.modules.pop(module_name)
    if module_name == "ui" or module_name.startswith("ui."):
        sys.modules.pop(module_name)

from orchestration.nourishbot_asset_orchestration import build_meal_dataset
from orchestration.nourishbot_asset_orchestration import ensure_example_assets
from orchestration.nourishbot_workflow import analyze_food_image
from orchestration.nourishbot_workflow import build_analysis_crew
from orchestration.nourishbot_workflow import build_recipe_crew
from models.nourishbot_image_processor import NourishBotImageProcessor
from ui.nourishbot_ui import build_nourishbot_interface


class FakeResponse:
    def __init__(self, content: str):
        self.content = content


class FakeModel:
    def invoke(self, prompt: str):
        lowered = prompt.lower()
        if "nutrition summary" in lowered or "calories macros" in lowered:
            return FakeResponse("This meal is balanced and benefits from fiber rich vegetables with room to moderate sodium.")
        if "create a concise customer facing markdown answer" in lowered and "analysis" in lowered:
            return FakeResponse("This meal offers strong protein moderate carbs and a practical improvement path for a healthier plate.")
        if "create a concise customer facing markdown answer" in lowered and "recipe" in lowered:
            return FakeResponse("This remix preserves the main flavors while adapting the dish to the selected dietary preference.")
        return FakeResponse("General nutrition guidance.")


def test_example_assets_and_dataset_are_built():
    processor = NourishBotImageProcessor()
    assets = ensure_example_assets()
    dataset = build_meal_dataset(processor)

    assert len(assets) == 3
    assert len(dataset) == 3
    assert dataset.iloc[0]["Embedding"].size > 0


def test_analysis_workflow_returns_detected_meal_and_calories():
    assets = ensure_example_assets()
    result = analyze_food_image(
        image_path=str(assets["salmon_power_bowl"]),
        dietary_preference="balanced",
        workflow_type="analysis",
        model=FakeModel(),
    )

    assert "AI Nutrition Coach" in result
    assert "Calories" in result
    assert "Salmon Power Bowl" in result


def test_recipe_workflow_returns_dietary_guidance_and_recipe():
    assets = ensure_example_assets()
    result = analyze_food_image(
        image_path=str(assets["chicken_stir_fry"]),
        dietary_preference="gluten-free",
        workflow_type="recipe",
        model=FakeModel(),
    )

    assert "Dietary Fit" in result
    assert "Recipe Suggestion" in result
    assert "gluten-free" in result.lower()


def test_crews_have_expected_number_of_tasks():
    analysis_crew = build_analysis_crew(model=FakeModel())
    recipe_crew = build_recipe_crew(model=FakeModel())

    assert len(analysis_crew.tasks) == 3
    assert len(recipe_crew.tasks) == 4


def test_gradio_interface_is_constructed():
    demo = build_nourishbot_interface()

    assert demo is not None