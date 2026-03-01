from pydantic import BaseModel


class AgentRunnerRequest(BaseModel):
    task: str


class AgentRunnerResponse(BaseModel):
    result: str
