# --- DEPENDENCIAS ---
import json

from config.meal_planner_config import DEFAULT_INPUTS
from models.crewai_compat import Agent
from models.crewai_compat import Crew
from models.crewai_compat import Process
from models.crewai_compat import Task
from models.meal_grocery_entities import DailyMeals
from models.meal_grocery_entities import GroceryItem
from models.meal_grocery_entities import GroceryShoppingPlan
from models.meal_grocery_entities import MealPlan
from models.meal_grocery_entities import ShoppingCategory
from models.meal_grocery_entities import WeeklyGroceryPlan
from models.meal_grocery_entities import WeeklyMealPlan
from models.meal_llm_gateway import build_meal_model
from models.recipe_search_tools import LocalRecipeSearchTool
from leftover import LeftoversCrew


def _invoke_model(agent: Agent, prompt: str) -> str:
    response = agent.llm.invoke(prompt)
    return str(getattr(response, "content", response)).strip()


def _lookup_recipe(inputs: dict):
    return LocalRecipeSearchTool().run(inputs["meal_name"])


def execute_meal_planning(agent: Agent, description: str, context_text: str, inputs: dict):
    recipe = _lookup_recipe(inputs)
    prompt = (
        f"Role: {agent.role}. Goal: {agent.goal}.\n\n"
        f"Task: {description}\n"
        f"Recipe knowledge: {recipe['ingredients']}\n"
        f"Dietary restrictions: {inputs['dietary_restrictions']}\n"
        f"Cooking skill: {inputs['cooking_skill']}\n"
        "Write a compact explanation of why this meal fits the request."
    )
    _invoke_model(agent, prompt)
    return MealPlan(
        meal_name=inputs["meal_name"],
        difficulty_level=recipe["difficulty_level"],
        servings=int(inputs["servings"]),
        researched_ingredients=recipe["ingredients"],
    )


def execute_shopping_task(agent: Agent, description: str, context_text: str, inputs: dict):
    recipe = _lookup_recipe(inputs)
    sections: dict[str, list[GroceryItem]] = {}
    for name, quantity, estimated_price, category in recipe["shopping_items"]:
        item = GroceryItem(name=name, quantity=quantity, estimated_price=estimated_price, category=category)
        sections.setdefault(category, []).append(item)

    shopping_sections = []
    for section_name, items in sections.items():
        shopping_sections.append(
            ShoppingCategory(
                section_name=section_name,
                items=items,
                estimated_total=_estimate_section_total(items),
            )
        )

    return GroceryShoppingPlan(
        total_budget=str(inputs["budget"]),
        meal_plans=[execute_meal_planning(agent, description, context_text, inputs)],
        shopping_sections=shopping_sections,
        shopping_tips=recipe["shopping_tips"],
    )


def _estimate_section_total(items: list[GroceryItem]) -> str:
    lows = 0
    highs = 0
    for item in items:
        parts = item.estimated_price.replace("$", "").split("-")
        if len(parts) == 2:
            lows += int(parts[0])
            highs += int(parts[1])
        else:
            lows += int(parts[0])
            highs += int(parts[0])
    return f"${lows}-{highs}"


def execute_budget_task(agent: Agent, description: str, context_text: str, inputs: dict):
    recipe = _lookup_recipe(inputs)
    prompt = (
        f"Role: {agent.role}. Goal: {agent.goal}.\n\n"
        f"Task: {description}\n"
        f"Context:\n{context_text}\n\n"
        "Produce a concise budget analysis with savings ideas."
    )
    model_summary = _invoke_model(agent, prompt)
    return (
        f"Budget target: {inputs['budget']}\n"
        f"Estimated plan: aligned with {recipe['shopping_tips'][0]}\n"
        f"Advisor summary: {model_summary}\n"
        "Money saving tips:\n"
        "- Prefer store brand pantry staples.\n"
        "- Batch prep vegetables to reduce waste."
    )


def execute_leftover_task(agent: Agent, description: str, context_text: str, inputs: dict):
    recipe = _lookup_recipe(inputs)
    prompt = (
        f"Role: {agent.role}. Goal: {agent.goal}.\n\n"
        f"Task: {description}\n"
        f"Meal: {inputs['meal_name']}\n"
        f"Ideas: {recipe['leftover_ideas']}"
    )
    model_text = _invoke_model(agent, prompt)
    ideas = "\n".join(f"- {idea}" for idea in recipe["leftover_ideas"])
    return f"Leftover strategy summary:\n{model_text}\n\nIdeas:\n{ideas}"


def execute_summary_task(agent: Agent, description: str, context_text: str, inputs: dict):
    prompt = (
        f"Role: {agent.role}. Goal: {agent.goal}.\n\n"
        f"Task: {description}\n"
        f"Context:\n{context_text}\n\n"
        "Compile a concise but structured final guide."
    )
    model_summary = _invoke_model(agent, prompt)
    return f"{model_summary}\n\nCompiled Guide:\n{context_text}"


def execute_nutrition_task(agent: Agent, description: str, context_text: str, inputs: dict):
    prompt = (
        f"Role: {agent.role}. Goal: {agent.goal}.\n\n"
        f"Task: {description}\n"
        f"Context:\n{context_text}\n\n"
        "Provide calorie protein carbs fats and practical healthy improvements."
    )
    return _invoke_model(agent, prompt)


def build_agents(model=None):
    llm = model or build_meal_model()
    meal_planner = Agent(
        role="Meal Planner & Recipe Researcher",
        goal="Search for optimal recipes and create detailed meal plans",
        backstory="A skilled meal planner who balances dietary needs cooking skill and budget constraints.",
        tools=[LocalRecipeSearchTool()],
        llm=llm,
        verbose=False,
    )
    shopping_organizer = Agent(
        role="Shopping Organizer",
        goal="Organize grocery lists by store sections efficiently",
        backstory="An experienced shopper who groups items by store flow and keeps trips efficient.",
        tools=[],
        llm=llm,
        verbose=False,
    )
    budget_advisor = Agent(
        role="Budget Advisor",
        goal="Provide cost estimates and money saving tips",
        backstory="A budget conscious shopper who keeps meal plans practical and affordable.",
        tools=[LocalRecipeSearchTool()],
        llm=llm,
        verbose=False,
    )
    summary_agent = Agent(
        role="Report Compiler",
        goal="Compile comprehensive meal planning reports from all team outputs",
        backstory="A coordinator who turns multi agent output into one guide people can actually follow in the kitchen.",
        tools=[],
        llm=llm,
        verbose=False,
    )
    nutrition_analyst = Agent(
        role="Nutrition Analyst & Health Advisor",
        goal="Analyze meal nutritional content and provide healthy recommendations",
        backstory="A certified nutritionist who reviews balance macros and ways to improve health outcomes.",
        tools=[LocalRecipeSearchTool()],
        llm=llm,
        verbose=False,
    )
    leftovers_cb = LeftoversCrew(llm=llm)
    leftover_manager = leftovers_cb.leftover_manager()
    return meal_planner, shopping_organizer, budget_advisor, summary_agent, nutrition_analyst, leftovers_cb, leftover_manager


def build_tasks(model=None):
    meal_planner, shopping_organizer, budget_advisor, summary_agent, nutrition_analyst, leftovers_cb, leftover_manager = build_agents(model=model)
    meal_planning_task = Task(
        description=(
            "Search for the best '{meal_name}' recipe for {servings} people within a {budget} budget. "
            "Consider dietary restrictions: {dietary_restrictions} and cooking skill level: {cooking_skill}."
        ),
        expected_output="A detailed meal plan with researched ingredients and quantities.",
        agent=meal_planner,
        output_pydantic=MealPlan,
        output_file="meals.json",
        executor=execute_meal_planning,
    )
    shopping_task = Task(
        description=(
            "Organize the ingredients from the '{meal_name}' meal plan into a grocery shopping list. "
            "Group items by store sections and stay within budget: {budget}."
        ),
        expected_output="An organized shopping list grouped by store sections with quantities and prices.",
        agent=shopping_organizer,
        context=[meal_planning_task],
        output_pydantic=GroceryShoppingPlan,
        output_file="shopping_list.json",
        executor=execute_shopping_task,
    )
    budget_task = Task(
        description=(
            "Analyze the shopping plan for '{meal_name}' serving {servings} people and provide money saving guidance within {budget}."
        ),
        expected_output="A complete shopping guide with detailed prices budget analysis and money saving tips.",
        agent=budget_advisor,
        context=[meal_planning_task, shopping_task],
        output_file="shopping_guide.md",
        executor=execute_budget_task,
    )
    leftover_task = leftovers_cb.leftover_task(leftover_manager, execute_leftover_task)
    leftover_task.context = [meal_planning_task, shopping_task]
    nutrition_task = Task(
        description=(
            "Analyze the nutritional content of the '{meal_name}' meal plan and suggest healthier alternatives while respecting {dietary_restrictions}."
        ),
        expected_output="Nutritional analysis with calorie estimates macro guidance and improvement suggestions.",
        agent=nutrition_analyst,
        context=[meal_planning_task, shopping_task, budget_task],
        output_file="nutrition_analysis.md",
        executor=execute_nutrition_task,
    )
    summary_task = Task(
        description=(
            "Compile a complete meal planning guide that includes recipe shopping list budget analysis and leftover management."
        ),
        expected_output="A comprehensive meal planning guide that combines all team outputs into one cohesive report.",
        agent=summary_agent,
        context=[meal_planning_task, shopping_task, budget_task, leftover_task],
        executor=execute_summary_task,
    )
    return {
        "agents": [meal_planner, shopping_organizer, budget_advisor, leftover_manager, summary_agent],
        "meal_planning_task": meal_planning_task,
        "shopping_task": shopping_task,
        "budget_task": budget_task,
        "leftover_task": leftover_task,
        "summary_task": summary_task,
        "nutrition_task": nutrition_task,
        "nutrition_agent": nutrition_analyst,
    }


def build_complete_grocery_crew(model=None):
    payload = build_tasks(model=model)
    crew = Crew(
        agents=payload["agents"],
        tasks=[payload["meal_planning_task"], payload["shopping_task"], payload["budget_task"], payload["leftover_task"], payload["summary_task"]],
        process=Process.sequential,
        verbose=True,
    )
    return crew, payload


def build_health_focused_crew(model=None):
    payload = build_tasks(model=model)
    crew = Crew(
        agents=payload["agents"] + [payload["nutrition_agent"]],
        tasks=[
            payload["meal_planning_task"],
            payload["shopping_task"],
            payload["budget_task"],
            payload["nutrition_task"],
            payload["leftover_task"],
            payload["summary_task"],
        ],
        process=Process.sequential,
        verbose=True,
    )
    return crew, payload


def build_sample_weekly_plan() -> WeeklyMealPlan:
    breakfast = MealPlan(meal_name="Oatmeal", difficulty_level="Easy", servings=2, researched_ingredients=["oats", "milk", "berries"])
    lunch = MealPlan(meal_name="Salad", difficulty_level="Easy", servings=2, researched_ingredients=["lettuce", "tomatoes", "dressing"])
    dinner = MealPlan(meal_name="Pasta", difficulty_level="Medium", servings=2, researched_ingredients=["pasta", "sauce", "cheese"])
    return WeeklyMealPlan(
        week_start_date="2026-03-16",
        daily_meals=[DailyMeals(date="2026-03-16", breakfast=breakfast, lunch=lunch, dinner=dinner)],
        weekly_themes=["Simple Monday", "Prep Friendly Week"],
        prep_suggestions=["Wash vegetables on Sunday.", "Cook grains in bulk."],
    )


def build_sample_weekly_grocery_plan() -> WeeklyGroceryPlan:
    sample_week = build_sample_weekly_plan()
    bulk_items = [
        GroceryItem(name="Rice", quantity="1 large bag", estimated_price="$8-10", category="Pantry"),
        GroceryItem(name="Olive Oil", quantity="1 bottle", estimated_price="$7-9", category="Pantry"),
    ]
    return WeeklyGroceryPlan(
        weekly_budget="$85",
        meal_plans=sample_week.daily_meals,
        shopping_sections=[],
        bulk_items=bulk_items,
        shopping_tips=["Batch your produce prep.", "Buy grains in bulk."],
        budget_breakdown={"2026-03-16": "$25", "2026-03-17": "$20"},
    )


def run_complete_grocery_demo(inputs: dict | None = None):
    crew, _ = build_complete_grocery_crew()
    result = crew.kickoff(inputs=inputs or DEFAULT_INPUTS)
    print(result.raw)
    print("\n=== Weekly Meal Plan Example ===")
    print(json.dumps(build_sample_weekly_plan().model_dump(), indent=2, ensure_ascii=False))
    print("\n=== Weekly Grocery Plan Example ===")
    print(json.dumps(build_sample_weekly_grocery_plan().model_dump(), indent=2, ensure_ascii=False))
    return result