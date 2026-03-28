# --- DEPENDENCIAS ---
import asyncio
import logging
import os
from pathlib import Path
from typing import Any

from pydantic import BaseModel
from pydantic import Field

from config.beeai_lab_config import CALCULATOR_QUERIES
from config.beeai_lab_config import DEFAULT_ANALYSIS_QUERY
from config.beeai_lab_config import DEFAULT_TEXT_MODEL
from config.beeai_lab_config import DEFAULT_TRAVEL_QUERY
from config.beeai_lab_config import PROJECT_SCENARIOS
from models.beeai_compat import AgentRunResult
from models.beeai_compat import AskPermissionRequirement
from models.beeai_compat import ChatModel
from models.beeai_compat import ChatModelParameters
from models.beeai_compat import ConditionalRequirement
from models.beeai_compat import Emitter
from models.beeai_compat import GlobalTrajectoryMiddleware
from models.beeai_compat import HandoffTool
from models.beeai_compat import OpenMeteoTool
from models.beeai_compat import RequirementAgent
from models.beeai_compat import RunContext
from models.beeai_compat import StringToolOutput
from models.beeai_compat import SystemMessage
from models.beeai_compat import ThinkTool
from models.beeai_compat import Tool
from models.beeai_compat import ToolRunOptions
from models.beeai_compat import UnconstrainedMemory
from models.beeai_compat import UserMessage
from models.beeai_compat import WikipediaTool
from models.beeai_entities import BusinessPlan
from models.beeai_entities import TravelPlanSummary


class SimplePromptTemplate:
    def __init__(self, template: str):
        self.template = template

    def render(self, variables: dict[str, str]) -> str:
        formatted_template = self.template
        for key in variables:
            formatted_template = formatted_template.replace(f"{{{{{key}}}}}", f"{{{key}}}")
        return formatted_template.format(**variables)


class CalculatorInput(BaseModel):
    expression: str = Field(description="Basic arithmetic expression.")


class SimpleCalculatorTool(Tool[CalculatorInput, ToolRunOptions, StringToolOutput]):
    name = "SimpleCalculator"
    description = "Perform basic arithmetic calculations."
    input_schema = CalculatorInput

    def __init__(self, options: dict[str, Any] | None = None) -> None:
        super().__init__(options)

    def _create_emitter(self) -> Emitter:
        return Emitter.root().child(namespace=["tool", "calculator", "basic"], creator=self)

    def _safe_calculate(self, expression: str) -> float:
        expr = expression.replace(" ", "")
        allowed_chars = set("0123456789+-*/().")
        if not all(char in allowed_chars for char in expr):
            raise ValueError("Only numbers and + - * / parentheses are allowed.")
        try:
            result = eval(expr, {"__builtins__": {}}, {})
            return float(result)
        except ZeroDivisionError as exc:
            raise ValueError("Division by zero is not allowed.") from exc
        except Exception as exc:
            raise ValueError(f"Invalid arithmetic expression: {exc}") from exc

    async def _run(self, input: CalculatorInput, options: ToolRunOptions | None, context: RunContext) -> StringToolOutput:
        result = self._safe_calculate(input.expression)
        return StringToolOutput(
            f"Simple Calculator\nExpression: {input.expression}\nResult: {result:g}"
        )


def build_model(model_name: str = DEFAULT_TEXT_MODEL) -> ChatModel:
    return ChatModel.from_name(model_name, ChatModelParameters(temperature=0))


def configure_environment() -> str:
    os.environ["WATSONX_PROJECT_ID"] = "skills-network"
    return "Environment configured successfully!"


async def basic_chat_example(model: ChatModel | None = None) -> str:
    llm = model or build_model()
    messages = [
        SystemMessage(content="You are a helpful AI assistant and creative writing expert."),
        UserMessage(content="Help me brainstorm a unique business idea for a food delivery service that doesn't exist yet."),
    ]
    response = await llm.create(messages=messages)
    return response.get_text_content()


async def prompt_template_example(model: ChatModel | None = None) -> list[dict[str, str]]:
    llm = model or build_model()
    template_content = """
    You are a senior data scientist evaluating a machine learning project proposal.

    Project Details:
    - Project Name: {{project_name}}
    - Business Problem: {{business_problem}}
    - Available Data: {{data_description}}
    - Timeline: {{timeline}}
    - Success Metrics: {{success_metrics}}

    Please provide:
    1. Feasibility assessment (1-10 scale)
    2. Key technical challenges
    3. Recommended approach
    4. Risk mitigation strategies
    5. Expected outcomes
    """
    prompt_template = SimplePromptTemplate(template_content)
    outputs = []
    for scenario in PROJECT_SCENARIOS:
        rendered_prompt = prompt_template.render(scenario)
        response = await llm.create(messages=[UserMessage(content=rendered_prompt)])
        outputs.append({"project_name": scenario["project_name"], "rendered_prompt": rendered_prompt, "response": response.get_text_content()})
    return outputs


async def structured_output_example(model: ChatModel | None = None) -> dict[str, Any]:
    llm = model or build_model()
    response = await llm.create_structure(
        schema=BusinessPlan,
        messages=[
            SystemMessage(content="You are an expert business consultant and entrepreneur."),
            UserMessage(content="Create a business plan for a mobile app that helps people find and book unique local experiences in their city."),
        ],
    )
    return response.object


async def minimal_tracked_agent_example(model: ChatModel | None = None) -> AgentRunResult:
    llm = model or build_model()
    agent = RequirementAgent(
        llm=llm,
        tools=[],
        memory=UnconstrainedMemory(),
        instructions="You are an expert cybersecurity analyst specializing in threat assessment and risk analysis.",
    )
    return await agent.run(DEFAULT_ANALYSIS_QUERY)


def _cyber_agent(requirements: list[Any], tools: list[Any], model: ChatModel | None = None) -> RequirementAgent:
    llm = model or build_model()
    return RequirementAgent(
        llm=llm,
        tools=tools,
        memory=UnconstrainedMemory(),
        instructions="You are an expert cybersecurity analyst specializing in threat assessment and risk analysis.",
        middlewares=[GlobalTrajectoryMiddleware(included=[Tool])],
        requirements=requirements,
    )


async def wikipedia_enhanced_agent_example(model: ChatModel | None = None) -> AgentRunResult:
    agent = _cyber_agent(
        requirements=[ConditionalRequirement(WikipediaTool, max_invocations=2)],
        tools=[WikipediaTool()],
        model=model,
    )
    return await agent.run(DEFAULT_ANALYSIS_QUERY)


async def reasoning_enhanced_agent_example(model: ChatModel | None = None) -> AgentRunResult:
    agent = _cyber_agent(
        requirements=[ConditionalRequirement(ThinkTool, max_invocations=2), ConditionalRequirement(WikipediaTool, max_invocations=2)],
        tools=[ThinkTool(), WikipediaTool()],
        model=model,
    )
    return await agent.run(DEFAULT_ANALYSIS_QUERY)


async def controlled_execution_example(model: ChatModel | None = None) -> AgentRunResult:
    agent = _cyber_agent(
        requirements=[
            ConditionalRequirement(ThinkTool, force_at_step=1, min_invocations=1, max_invocations=3, consecutive_allowed=False),
            ConditionalRequirement(WikipediaTool, only_after=[ThinkTool], min_invocations=1, max_invocations=2),
        ],
        tools=[ThinkTool(), WikipediaTool()],
        model=model,
    )
    return await agent.run(DEFAULT_ANALYSIS_QUERY)


async def react_agent_example(model: ChatModel | None = None) -> AgentRunResult:
    agent = _cyber_agent(
        requirements=[
            ConditionalRequirement(ThinkTool, force_at_step=1, force_after=Tool, min_invocations=1, max_invocations=5, consecutive_allowed=False),
            ConditionalRequirement(WikipediaTool, max_invocations=2),
        ],
        tools=[ThinkTool(), WikipediaTool()],
        model=model,
    )
    return await agent.run(DEFAULT_ANALYSIS_QUERY)


async def production_security_example(model: ChatModel | None = None) -> AgentRunResult:
    agent = _cyber_agent(
        requirements=[
            ConditionalRequirement(ThinkTool, force_at_step=1, min_invocations=1, max_invocations=2, consecutive_allowed=False),
            AskPermissionRequirement(WikipediaTool),
            ConditionalRequirement(WikipediaTool, only_after=[ThinkTool], max_invocations=1),
        ],
        tools=[ThinkTool(), WikipediaTool()],
        model=model,
    )
    return await agent.run(DEFAULT_ANALYSIS_QUERY)


async def calculator_agent_example(model: ChatModel | None = None) -> list[str]:
    llm = model or build_model()
    calculator_agent = RequirementAgent(
        llm=llm,
        tools=[SimpleCalculatorTool()],
        memory=UnconstrainedMemory(),
        instructions="You are a helpful math assistant that uses the calculator tool for accurate arithmetic.",
        middlewares=[GlobalTrajectoryMiddleware(included=[Tool])],
    )
    outputs = []
    for query in CALCULATOR_QUERIES:
        result = await calculator_agent.run(query)
        outputs.append(result.answer.text)
    return outputs


async def multi_agent_travel_planner_with_language(model: ChatModel | None = None) -> TravelPlanSummary:
    llm = model or build_model()
    destination_expert = RequirementAgent(
        llm=llm,
        tools=[WikipediaTool(), ThinkTool()],
        memory=UnconstrainedMemory(),
        instructions="You are a Destination Research Expert.",
        middlewares=[GlobalTrajectoryMiddleware(included=[Tool])],
        requirements=[ConditionalRequirement(ThinkTool, force_at_step=1), ConditionalRequirement(WikipediaTool, only_after=[ThinkTool], max_invocations=4)],
    )
    travel_meteorologist = RequirementAgent(
        llm=llm,
        tools=[OpenMeteoTool(), ThinkTool()],
        memory=UnconstrainedMemory(),
        instructions="You are a Travel Meteorologist.",
        middlewares=[GlobalTrajectoryMiddleware(included=[Tool])],
        requirements=[ConditionalRequirement(ThinkTool, force_at_step=1), ConditionalRequirement(OpenMeteoTool, only_after=[ThinkTool], max_invocations=1)],
    )
    language_expert = RequirementAgent(
        llm=llm,
        tools=[WikipediaTool(), ThinkTool()],
        memory=UnconstrainedMemory(),
        instructions="You are a Language and Cultural Expert.",
        middlewares=[GlobalTrajectoryMiddleware(included=[Tool])],
        requirements=[ConditionalRequirement(ThinkTool, force_at_step=1), ConditionalRequirement(WikipediaTool, max_invocations=2)],
    )
    coordinator = RequirementAgent(
        llm=llm,
        tools=[
            HandoffTool(destination_expert, name="DestinationResearch", description="Destination research handoff."),
            HandoffTool(travel_meteorologist, name="WeatherPlanning", description="Weather planning handoff."),
            HandoffTool(language_expert, name="LanguageCulturalGuidance", description="Language and etiquette handoff."),
            ThinkTool(),
        ],
        memory=UnconstrainedMemory(),
        instructions="You are the Travel Coordinator for comprehensive travel planning.",
        middlewares=[GlobalTrajectoryMiddleware(included=[Tool])],
        requirements=[ConditionalRequirement(ThinkTool, consecutive_allowed=False), AskPermissionRequirement(["DestinationResearch", "WeatherPlanning", "LanguageCulturalGuidance"])],
    )
    result = await coordinator.run(DEFAULT_TRAVEL_QUERY)
    trajectory_text = "\n".join(result.trajectory)
    return TravelPlanSummary(
        destination_guidance=_extract_trajectory_line(trajectory_text, "DestinationResearch"),
        weather_guidance=_extract_trajectory_line(trajectory_text, "WeatherPlanning"),
        language_guidance=_extract_trajectory_line(trajectory_text, "LanguageCulturalGuidance"),
        coordinator_summary=result.answer.text,
    )


def _extract_trajectory_line(trajectory_text: str, prefix: str) -> str:
    for line in trajectory_text.splitlines():
        if line.startswith(f"{prefix}:"):
            return line.split(":", 1)[1].strip()
    return ""


async def run_beeai_lab_demo() -> None:
    logging.getLogger("asyncio").setLevel(logging.CRITICAL)
    print(configure_environment())
    print("\n=== Basic Chat ===")
    print(await basic_chat_example())
    print("\n=== Prompt Templates ===")
    for scenario_output in await prompt_template_example():
        print(f"{scenario_output['project_name']}: {scenario_output['response']}")
    print("\n=== Structured Output ===")
    print(await structured_output_example())
    print("\n=== Minimal Agent ===")
    print((await minimal_tracked_agent_example()).answer.text)
    print("\n=== Wikipedia Agent ===")
    print((await wikipedia_enhanced_agent_example()).answer.text)
    print("\n=== ReAct Agent ===")
    print((await react_agent_example()).answer.text)
    print("\n=== Calculator Tool ===")
    for entry in await calculator_agent_example():
        print(entry)
    print("\n=== Multi Agent Travel Planner ===")
    print((await multi_agent_travel_planner_with_language()).coordinator_summary)