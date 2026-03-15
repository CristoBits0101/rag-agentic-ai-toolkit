from pydantic import BaseModel


class AgentRunRequest(BaseModel):
    task: str


class AgentRunResponse(BaseModel):
    result: str
