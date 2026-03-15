from app.modules.features.agent_runner.schemas import (
    AgentRunnerRequest,
    AgentRunnerResponse,
)


def run_agent(payload: AgentRunnerRequest) -> AgentRunnerResponse:
    return AgentRunnerResponse(result=f"agent_runner placeholder: {payload.task}")
