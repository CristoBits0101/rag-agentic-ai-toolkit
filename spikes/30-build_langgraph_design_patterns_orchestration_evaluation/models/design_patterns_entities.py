# --- DEPENDENCIAS ---
from typing import List

from pydantic import BaseModel
from pydantic import Field


class Dish(BaseModel):
    name: str = Field(description="Name of the dish.")
    ingredients: List[str] = Field(description="List of ingredients needed for the dish.")
    location: str = Field(description="Cuisine or cultural origin of the food.")


class Dishes(BaseModel):
    sections: List[Dish] = Field(description="A list of dishes with ingredients and cuisine.")