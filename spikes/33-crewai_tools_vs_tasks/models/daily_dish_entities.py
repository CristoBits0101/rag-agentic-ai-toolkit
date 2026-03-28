# --- DEPENDENCIAS ---
from pydantic import BaseModel
from pydantic import Field


class ToolingComparisonSummary(BaseModel):
    query: str = Field(..., description="Customer question used for the comparison.")
    agent_centric_answer: str = Field(..., description="Final answer from the agent centric crew.")
    task_centric_answer: str = Field(..., description="Final answer from the task centric crew.")
    agent_centric_tools: list[str] = Field(default_factory=list, description="Tools touched by the generalist flow.")
    task_centric_tools: list[str] = Field(default_factory=list, description="Tools touched by the task specific flow.")
    key_difference: str = Field(..., description="Human readable explanation of the observed difference.")


class CalculatorDemoResult(BaseModel):
    addition_result: int = Field(..., description="Result of the addition custom tool demo.")
    multiplication_result: int = Field(..., description="Result of the multiplication custom tool demo.")