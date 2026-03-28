# --- DEPENDENCIAS ---
from pydantic import BaseModel
from pydantic import Field


class BusinessPlan(BaseModel):
    business_name: str = Field(description="Catchy name for the business.")
    elevator_pitch: str = Field(description="30 second description of the business.")
    target_market: str = Field(description="Primary target audience.")
    unique_value_proposition: str = Field(description="What makes this business special.")
    revenue_streams: list[str] = Field(description="Ways the business will make money.")
    startup_costs: str = Field(description="Estimated initial investment needed.")
    key_success_factors: list[str] = Field(description="Critical elements for success.")


class TravelPlanSummary(BaseModel):
    destination_guidance: str = Field(description="Destination guidance summary.")
    weather_guidance: str = Field(description="Weather guidance summary.")
    language_guidance: str = Field(description="Language and etiquette summary.")
    coordinator_summary: str = Field(description="Final coordinator synthesis.")