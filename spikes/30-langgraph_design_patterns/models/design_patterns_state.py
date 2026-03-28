# --- DEPENDENCIAS ---
import operator
from typing import Annotated
from typing import List
from typing import Literal
from typing import TypedDict

from models.design_patterns_entities import Dish

Grades = Literal[
    "ultra-conservative",
    "conservative",
    "moderate",
    "aggressive",
    "high risk",
]


class OrchestrationState(TypedDict, total=False):
    meals: str
    sections: List[Dish]
    completed_menu: Annotated[List[str], operator.add]
    final_meal_guide: str


class WorkerState(TypedDict, total=False):
    section: Dish
    completed_menu: Annotated[list[str], operator.add]


class ReflectionState(TypedDict, total=False):
    investment_plan: str
    investor_profile: str
    target_grade: Grades
    feedback: str
    grade: Grades
    n: int