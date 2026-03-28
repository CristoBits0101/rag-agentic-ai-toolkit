# --- DEPENDENCIAS ---
from enum import Enum
from typing import Dict
from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class GroceryItem(BaseModel):
    name: str = Field(description="Name of the grocery item")
    quantity: str = Field(description="Quantity needed")
    estimated_price: str = Field(description="Estimated price")
    category: str = Field(description="Store section")


class MealPlan(BaseModel):
    meal_name: str = Field(description="Name of the meal")
    difficulty_level: str = Field(description="Difficulty level")
    servings: int = Field(description="Number of servings")
    researched_ingredients: List[str] = Field(description="Ingredients found through research")


class ShoppingCategory(BaseModel):
    section_name: str = Field(description="Store section")
    items: List[GroceryItem] = Field(description="Items in this section")
    estimated_total: str = Field(description="Estimated cost for the section")


class GroceryShoppingPlan(BaseModel):
    total_budget: str = Field(description="Total planned budget")
    meal_plans: List[MealPlan] = Field(description="Planned meals")
    shopping_sections: List[ShoppingCategory] = Field(description="Shopping list organized by section")
    shopping_tips: List[str] = Field(description="Money saving and efficiency tips")


class MealType(str, Enum):
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    SNACK = "snack"


class DailyMeals(BaseModel):
    date: str = Field(description="Date in YYYY-MM-DD format")
    breakfast: Optional[MealPlan] = Field(default=None, description="Breakfast meal plan")
    lunch: Optional[MealPlan] = Field(default=None, description="Lunch meal plan")
    dinner: Optional[MealPlan] = Field(default=None, description="Dinner meal plan")
    snacks: Optional[List[MealPlan]] = Field(default=None, description="Snack meal plans")


class WeeklyMealPlan(BaseModel):
    week_start_date: str = Field(description="Start date of the week")
    daily_meals: List[DailyMeals] = Field(description="Meals for each day")
    weekly_themes: List[str] = Field(description="Weekly cooking themes")
    prep_suggestions: List[str] = Field(description="Meal prep suggestions")


class WeeklyGroceryPlan(BaseModel):
    weekly_budget: str = Field(description="Total weekly budget")
    meal_plans: List[DailyMeals] = Field(description="All weekly meals")
    shopping_sections: List[ShoppingCategory] = Field(description="Store sections for the week")
    bulk_items: List[GroceryItem] = Field(description="Items to buy in bulk")
    shopping_tips: List[str] = Field(description="Weekly shopping efficiency tips")
    budget_breakdown: Dict[str, str] = Field(description="Daily budget allocation")