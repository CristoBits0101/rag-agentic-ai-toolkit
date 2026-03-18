# --- DEPENDENCIAS ---
import json
from pathlib import Path
from tempfile import NamedTemporaryFile

from PIL import Image

from config.nourishbot_config import DEFAULT_DIETARY_PREFERENCE
from models.crewai_compat import Agent
from models.crewai_compat import Crew
from models.crewai_compat import Process
from models.crewai_compat import Task
from models.nourishbot_entities import DetectedMeal
from models.nourishbot_entities import DietaryAdvice
from models.nourishbot_entities import NutritionSnapshot
from models.nourishbot_entities import RecipeSuggestion
from models.nourishbot_image_processor import NourishBotImageProcessor
from models.nourishbot_llm_gateway import build_text_model
from models.nourishbot_tools import DietaryPreferenceTool
from models.nourishbot_tools import NutritionLookupTool
from models.nourishbot_tools import RecipePlanningTool
from models.nourishbot_tools import VisionMealDetectionTool
from orchestration.nourishbot_asset_orchestration import build_meal_dataset
from orchestration.nourishbot_asset_orchestration import ensure_example_assets


def _invoke_model(agent: Agent, prompt: str) -> str:
    response = agent.llm.invoke(prompt)
    return str(getattr(response, "content", response)).strip()


def _load_context_objects(context_text: str) -> list[dict]:
    if not context_text.strip():
        return []
    return [json.loads(chunk) for chunk in context_text.split("\n\n") if chunk.strip()]


def execute_detection_task(agent: Agent, description: str, context_text: str, inputs: dict):
    tool = agent.tools[0]
    return tool.run(inputs["image_path"])


def execute_nutrition_task(agent: Agent, description: str, context_text: str, inputs: dict):
    detected = DetectedMeal.model_validate(_load_context_objects(context_text)[0])
    summary = _invoke_model(
        agent,
        (
            f"Role: {agent.role}. Goal: {agent.goal}.\n\n"
            f"Meal: {detected.title}\n"
            f"Items: {', '.join(detected.identified_items)}\n"
            f"Visual notes: {detected.vision_notes}\n"
            "Write a compact nutrition summary with one improvement suggestion."
        ),
    )
    tool = agent.tools[0]
    return tool.run(detected.image_key, summary=summary)


def execute_dietary_task(agent: Agent, description: str, context_text: str, inputs: dict):
    detected = DetectedMeal.model_validate(_load_context_objects(context_text)[0])
    tool = agent.tools[0]
    return tool.run(detected.identified_items, inputs["dietary_preference"])


def execute_recipe_task(agent: Agent, description: str, context_text: str, inputs: dict):
    detected_payload, dietary_payload = _load_context_objects(context_text)
    detected = DetectedMeal.model_validate(detected_payload)
    dietary = DietaryAdvice.model_validate(dietary_payload)
    tool = agent.tools[0]
    return tool.run(detected.image_key, dietary.dietary_preference, dietary.allowed_ingredients)


def execute_writer_task(agent: Agent, description: str, context_text: str, inputs: dict):
    workflow_type = inputs["workflow_type"]
    prompt = (
        f"Role: {agent.role}. Goal: {agent.goal}.\n\n"
        f"Workflow: {workflow_type}\n"
        f"Selected dietary preference: {inputs['dietary_preference']}\n"
        "Create a concise customer facing markdown answer from the JSON snippets below.\n"
        f"Context:\n{context_text}"
    )
    drafted = _invoke_model(agent, prompt)
    sections = _load_context_objects(context_text)
    detected = DetectedMeal.model_validate(sections[0])
    if workflow_type == "analysis":
        nutrition = NutritionSnapshot.model_validate(sections[1])
        return (
            f"## AI Nutrition Coach\n\n"
            f"### Detected Meal\n- {detected.title}\n- Confidence: {detected.similarity_score}\n- Visible items: {', '.join(detected.identified_items)}\n\n"
            f"### Nutritional Analysis\n- Calories: {nutrition.estimated_calories}\n- Protein: {nutrition.protein}\n- Carbohydrates: {nutrition.carbohydrates}\n- Fats: {nutrition.fats}\n- Fiber: {nutrition.fiber}\n\n"
            f"### Health Evaluation\n{nutrition.health_evaluation}\n\n"
            f"### Coach Summary\n{drafted}"
        )

    dietary = DietaryAdvice.model_validate(sections[1])
    recipe = RecipeSuggestion.model_validate(sections[2])
    blocked_line = ", ".join(dietary.blocked_ingredients) if dietary.blocked_ingredients else "none"
    return (
        f"## AI Nutrition Coach\n\n"
        f"### Detected Meal\n- {detected.title}\n- Visible items: {', '.join(detected.identified_items)}\n\n"
        f"### Dietary Fit\n- Preference: {dietary.dietary_preference}\n- Compatible: {dietary.compatible}\n- Blocked ingredients: {blocked_line}\n- Advice: {dietary.coaching_note}\n\n"
        f"### Recipe Suggestion\n- Title: {recipe.title}\n- Ingredients: {', '.join(recipe.ingredients)}\n- Instructions: {recipe.instructions}\n- Calorie target: {recipe.calorie_target}\n\n"
        f"### Coach Summary\n{drafted}"
    )


def build_agents(model=None, image_processor=None):
    llm = model or build_text_model()
    processor = image_processor or NourishBotImageProcessor()
    dataset = build_meal_dataset(processor)
    vision_agent = Agent(
        role="Vision AI Specialist",
        goal="Identify the meal from an uploaded image and describe what is visible.",
        backstory="A multimodal analyst that matches user images against a local nutrition dataset and can enrich the match with vision model notes.",
        tools=[VisionMealDetectionTool(processor, dataset)],
        llm=llm,
        allow_delegation=False,
    )
    nutrition_agent = Agent(
        role="Nutrition Analysis Specialist",
        goal="Translate the detected meal into calories macros micronutrients and a practical health interpretation.",
        backstory="A nutrition coach that reasons over structured meal data before writing a short explanation.",
        tools=[NutritionLookupTool(dataset)],
        llm=llm,
        allow_delegation=False,
    )
    dietary_agent = Agent(
        role="Dietary Preference Specialist",
        goal="Check whether the meal fits the requested dietary preference and suggest safe substitutions.",
        backstory="A diet aware planner that understands vegetarian vegan gluten free and high protein constraints.",
        tools=[DietaryPreferenceTool()],
        llm=llm,
        allow_delegation=False,
    )
    recipe_agent = Agent(
        role="Recipe Generation Specialist",
        goal="Create a refined recipe idea from the detected meal and dietary preference.",
        backstory="A meal planning assistant that remixes the detected dish without losing its nutritional intent.",
        tools=[RecipePlanningTool()],
        llm=llm,
        allow_delegation=False,
    )
    writer_agent = Agent(
        role="Wellness Writer",
        goal="Turn the intermediate outputs into a clear markdown answer for the end user.",
        backstory="A concise health communicator who summarizes analysis or recipe planning in a practical tone.",
        tools=[],
        llm=llm,
        allow_delegation=False,
    )
    return vision_agent, nutrition_agent, dietary_agent, recipe_agent, writer_agent


def build_analysis_crew(model=None, image_processor=None):
    vision_agent, nutrition_agent, _, _, writer_agent = build_agents(model=model, image_processor=image_processor)
    detection_task = Task(
        description="Identify the meal in the uploaded image located at {image_path}.",
        expected_output="A detected meal object with visual notes.",
        agent=vision_agent,
        executor=execute_detection_task,
        output_pydantic=DetectedMeal,
    )
    nutrition_task = Task(
        description="Analyze calories macros and health qualities for the detected meal.",
        expected_output="A structured nutrition snapshot.",
        agent=nutrition_agent,
        context=[detection_task],
        executor=execute_nutrition_task,
        output_pydantic=NutritionSnapshot,
    )
    writer_task = Task(
        description="Create the final analysis response for the user.",
        expected_output="A markdown response.",
        agent=writer_agent,
        context=[detection_task, nutrition_task],
        executor=execute_writer_task,
        tools=[],
    )
    crew = Crew(
        agents=[vision_agent, nutrition_agent, writer_agent],
        tasks=[detection_task, nutrition_task, writer_task],
        process=Process.sequential,
        verbose=True,
    )
    return crew


def build_recipe_crew(model=None, image_processor=None):
    vision_agent, _, dietary_agent, recipe_agent, writer_agent = build_agents(model=model, image_processor=image_processor)
    detection_task = Task(
        description="Identify the meal in the uploaded image located at {image_path}.",
        expected_output="A detected meal object with visual notes.",
        agent=vision_agent,
        executor=execute_detection_task,
        output_pydantic=DetectedMeal,
    )
    dietary_task = Task(
        description="Evaluate whether the meal fits the dietary preference {dietary_preference}.",
        expected_output="Structured dietary advice.",
        agent=dietary_agent,
        context=[detection_task],
        executor=execute_dietary_task,
        output_pydantic=DietaryAdvice,
    )
    recipe_task = Task(
        description="Generate a recipe suggestion adapted to the dietary preference {dietary_preference}.",
        expected_output="A structured recipe suggestion.",
        agent=recipe_agent,
        context=[detection_task, dietary_task],
        executor=execute_recipe_task,
        output_pydantic=RecipeSuggestion,
    )
    writer_task = Task(
        description="Create the final recipe workflow response for the user.",
        expected_output="A markdown response.",
        agent=writer_agent,
        context=[detection_task, dietary_task, recipe_task],
        executor=execute_writer_task,
        tools=[],
    )
    crew = Crew(
        agents=[vision_agent, dietary_agent, recipe_agent, writer_agent],
        tasks=[detection_task, dietary_task, recipe_task, writer_task],
        process=Process.sequential,
        verbose=True,
    )
    return crew


def analyze_food_image(
    image_path: str,
    dietary_preference: str = DEFAULT_DIETARY_PREFERENCE,
    workflow_type: str = "analysis",
    model=None,
    image_processor=None,
) -> str:
    if workflow_type == "analysis":
        crew = build_analysis_crew(model=model, image_processor=image_processor)
    elif workflow_type == "recipe":
        crew = build_recipe_crew(model=model, image_processor=image_processor)
    else:
        raise ValueError("workflow_type must be analysis or recipe.")
    result = crew.kickoff(
        inputs={
            "image_path": image_path,
            "dietary_preference": dietary_preference,
            "workflow_type": workflow_type,
        }
    )
    return result.raw


def analyze_pil_image(image: Image.Image, dietary_preference: str, workflow_type: str, model=None, image_processor=None) -> str:
    with NamedTemporaryFile(suffix=".png", delete=False) as temporary_file:
        temp_path = Path(temporary_file.name)
    try:
        image.save(temp_path)
        return analyze_food_image(
            image_path=str(temp_path),
            dietary_preference=dietary_preference,
            workflow_type=workflow_type,
            model=model,
            image_processor=image_processor,
        )
    finally:
        if temp_path.exists():
            temp_path.unlink()


def run_nourishbot_cli_demo() -> None:
    assets = ensure_example_assets()
    print("=== Analysis Workflow ===")
    print(analyze_food_image(str(assets["salmon_power_bowl"]), workflow_type="analysis", dietary_preference="balanced"))
    print("\n=== Recipe Workflow ===")
    print(analyze_food_image(str(assets["veggie_buddha_bowl"]), workflow_type="recipe", dietary_preference="vegan"))