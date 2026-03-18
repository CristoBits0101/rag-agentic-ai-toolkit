# --- DEPENDENCIAS ---
from pydantic import BaseModel


class TicketSummary(BaseModel):
    customer_name: str
    issue_type: str
    urgency_level: str
    recommended_action: str