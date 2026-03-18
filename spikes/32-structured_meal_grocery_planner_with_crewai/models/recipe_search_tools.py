# --- DEPENDENCIAS ---
from config.meal_planner_config import RECIPE_CATALOG


class LocalRecipeSearchTool:
    name = "local_recipe_search"

    def run(self, meal_name: str):
        return RECIPE_CATALOG.get(meal_name.lower(), RECIPE_CATALOG["chicken stir fry"])