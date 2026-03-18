# --- DEPENDENCIAS ---
import asyncio
from dataclasses import dataclass
from dataclasses import field
import math
import re
from typing import Any
from typing import Generic
from typing import TypeVar

from pydantic import BaseModel

from config.beeai_lab_config import WEATHER_DATA
from config.beeai_lab_config import WIKIPEDIA_SNIPPETS

TInput = TypeVar("TInput")
TOptions = TypeVar("TOptions")
TOutput = TypeVar("TOutput")


@dataclass
class ChatModelParameters:
    temperature: float = 0.0


@dataclass
class BaseMessage:
    content: str


class UserMessage(BaseMessage):
    pass


class SystemMessage(BaseMessage):
    pass


class TextResponse:
    def __init__(self, text: str):
        self.text = text

    def get_text_content(self) -> str:
        return self.text


class StructuredResponse:
    def __init__(self, obj: dict[str, Any]):
        self.object = obj


class ChatModel:
    def __init__(self, model_name: str, parameters: ChatModelParameters):
        self.model_name = model_name
        self.parameters = parameters

    @classmethod
    def from_name(cls, model_name: str, parameters: ChatModelParameters):
        return cls(model_name=model_name, parameters=parameters)

    async def create(self, messages: list[BaseMessage]):
        prompt = messages[-1].content if messages else ""
        system = messages[0].content if messages and isinstance(messages[0], SystemMessage) else ""
        return TextResponse(_generate_text_response(system, prompt))

    async def create_structure(self, schema: type[BaseModel], messages: list[BaseMessage]):
        prompt = messages[-1].content if messages else ""
        obj = _generate_structured_payload(schema, prompt)
        return StructuredResponse(obj)


def _generate_text_response(system: str, prompt: str) -> str:
    lowered = prompt.lower()
    if "food delivery service" in lowered:
        return (
            "Consider a neighborhood micro kitchen subscription that batches chef prepared meals around one street level pickup window per evening. "
            "It differentiates by combining hyperlocal menus predictable logistics and community events rather than on demand delivery."
        )
    if "machine learning project proposal" in lowered:
        project_name_match = re.search(r"project name:\s*(.+)", prompt, re.IGNORECASE)
        project_name = project_name_match.group(1).strip() if project_name_match else "the project"
        return (
            f"Feasibility for {project_name}: 8 out of 10. Main challenges include data quality model monitoring and stakeholder adoption. "
            "Recommended approach: start with a baseline model and phased rollout. Risks can be reduced with shadow testing human review and clear KPIs."
        )
    if "business plan" in lowered and "local experiences" in lowered:
        return "This concept works best as a curated local experiences marketplace focused on trust repeat bookings and city level partnerships."
    if "cybersecurity risks of quantum computing" in lowered:
        return (
            "Quantum risk centers on cryptographic breakage harvest now decrypt later exposure and long lead times for system migration. "
            "Financial institutions should inventory cryptography prioritize post quantum readiness and test hybrid migration paths now."
        )
    if "travel planning" in lowered or "japan" in lowered:
        return (
            "For Japan blend historical districts with rail friendly day planning. Layer clothing for seasonal variation and learn a few polite phrases to improve interactions."
        )
    return f"Structured local BeeAI style response for: {prompt}"


def _generate_structured_payload(schema: type[BaseModel], prompt: str) -> dict[str, Any]:
    schema_name = schema.__name__
    if schema_name == "BusinessPlan":
        return {
            "business_name": "CityLoop Experiences",
            "elevator_pitch": "A mobile app that curates bookable local experiences with trusted hosts and dynamic neighborhood itineraries.",
            "target_market": "Urban professionals and travelers seeking curated short format local experiences.",
            "unique_value_proposition": "Combines discovery booking and social proof for hyperlocal experiences that are hard to find on generic platforms.",
            "revenue_streams": ["booking fees", "host subscriptions", "premium concierge plans"],
            "startup_costs": "$120K to $180K for product design marketplace onboarding and go to market.",
            "key_success_factors": ["host quality", "city supply density", "trust and reviews"],
        }
    raise ValueError(f"Unsupported schema for local structured output: {schema_name}")


@dataclass
class UnconstrainedMemory:
    items: list[str] = field(default_factory=list)

    def add(self, value: str) -> None:
        self.items.append(value)


@dataclass
class ToolRunOptions:
    timeout: int | None = None


@dataclass
class RunContext:
    query: str
    trajectory: list[str]


class Emitter:
    def __init__(self, namespace: list[str] | None = None):
        self.namespace = namespace or []

    @classmethod
    def root(cls):
        return cls([])

    def child(self, namespace: list[str], creator=None):
        return Emitter(self.namespace + namespace)


@dataclass
class StringToolOutput:
    text: str

    def get_text_content(self) -> str:
        return self.text

    def __str__(self) -> str:
        return self.text


class Tool(Generic[TInput, TOptions, TOutput]):
    name = "Tool"
    description = "Generic tool"
    input_schema: type[BaseModel] | None = None

    def __init__(self, options: dict[str, Any] | None = None) -> None:
        self.options = options or {}

    def _create_emitter(self) -> Emitter:
        return Emitter.root().child(namespace=["tool", self.name.lower()], creator=self)

    async def _run(self, input: TInput, options: TOptions | None, context: RunContext) -> TOutput:
        raise NotImplementedError()

    async def run(self, input: TInput, options: TOptions | None = None, context: RunContext | None = None) -> TOutput:
        context = context or RunContext(query="", trajectory=[])
        if self.input_schema is not None and isinstance(input, dict):
            input = self.input_schema(**input)
        return await self._run(input, options, context)


class ThinkTool(Tool[dict[str, str], ToolRunOptions, StringToolOutput]):
    name = "ThinkTool"
    description = "Produce a short structured reasoning note before or after a tool action."

    async def _run(self, input: dict[str, str], options: ToolRunOptions | None, context: RunContext) -> StringToolOutput:
        query = input.get("query", context.query)
        step = input.get("step", "analysis")
        text = (
            f"Reasoning step for {step}: identify the main objective classify the domain and choose the safest next action for query '{query}'."
        )
        return StringToolOutput(text)


class WikipediaInput(BaseModel):
    query: str


class WikipediaTool(Tool[WikipediaInput, ToolRunOptions, StringToolOutput]):
    name = "WikipediaTool"
    description = "Return a short local encyclopedia style snippet related to the query."
    input_schema = WikipediaInput

    async def _run(self, input: WikipediaInput, options: ToolRunOptions | None, context: RunContext) -> StringToolOutput:
        query = input.query.lower()
        matches = []
        if any(keyword in query for keyword in ["cultural", "culture", "respectful", "language", "etiquette"]):
            matches.append(WIKIPEDIA_SNIPPETS["japanese etiquette"])
        for key, value in WIKIPEDIA_SNIPPETS.items():
            if key == "japanese etiquette":
                continue
            if key in query:
                matches.append(value)
        if not matches:
            matches.append("No direct encyclopedia match was found so rely on the model synthesis and conservative guidance.")
        return StringToolOutput(" ".join(matches))


class WeatherInput(BaseModel):
    location: str


class OpenMeteoTool(Tool[WeatherInput, ToolRunOptions, StringToolOutput]):
    name = "OpenMeteoTool"
    description = "Return a short local weather planning note for a destination."
    input_schema = WeatherInput

    async def _run(self, input: WeatherInput, options: ToolRunOptions | None, context: RunContext) -> StringToolOutput:
        location = input.location.lower()
        return StringToolOutput(WEATHER_DATA.get(location, WEATHER_DATA["japan"]))


@dataclass
class ConditionalRequirement:
    tool: Any
    force_at_step: int | None = None
    min_invocations: int = 0
    max_invocations: int | None = None
    only_after: list[Any] | None = None
    force_after: Any | None = None
    consecutive_allowed: bool = True


@dataclass
class AskPermissionRequirement:
    tools: Any


@dataclass
class GlobalTrajectoryMiddleware:
    included: list[Any] = field(default_factory=list)


@dataclass
class AgentAnswer:
    text: str


@dataclass
class AgentRunResult:
    answer: AgentAnswer
    trajectory: list[str]


class HandoffTool(Tool[dict[str, str], ToolRunOptions, StringToolOutput]):
    def __init__(self, agent: "RequirementAgent", name: str, description: str):
        super().__init__()
        self.agent = agent
        self.name = name
        self.description = description

    async def _run(self, input: dict[str, str], options: ToolRunOptions | None, context: RunContext) -> StringToolOutput:
        query = input.get("query", context.query)
        result = await self.agent.run(query)
        return StringToolOutput(result.answer.text)


class RequirementAgent:
    def __init__(
        self,
        llm: ChatModel,
        tools: list[Tool[Any, Any, Any]],
        memory: UnconstrainedMemory,
        instructions: str,
        middlewares: list[GlobalTrajectoryMiddleware] | None = None,
        requirements: list[Any] | None = None,
    ) -> None:
        self.llm = llm
        self.tools = tools
        self.memory = memory
        self.instructions = instructions
        self.middlewares = middlewares or []
        self.requirements = requirements or []

    async def run(self, query: str) -> AgentRunResult:
        self.memory.add(query)
        trajectory: list[str] = []
        executed_tools: list[tuple[str, str]] = []
        tool_map = {tool.name: tool for tool in self.tools}
        counts: dict[str, int] = {}

        plan = await self._build_plan(query, tool_map)
        for tool_name, payload in plan:
            tool = tool_map[tool_name]
            if self._needs_permission(tool_name):
                trajectory.append(f"Permission granted for {tool_name}.")
            counts[tool_name] = counts.get(tool_name, 0) + 1
            if self._exceeded_max(tool_name, counts):
                continue
            context = RunContext(query=query, trajectory=trajectory)
            output = await tool.run(payload, ToolRunOptions(), context)
            rendered = output.get_text_content() if hasattr(output, "get_text_content") else str(output)
            executed_tools.append((tool_name, rendered))
            trajectory.append(f"{tool_name}: {rendered}")

        answer_text = self._synthesize_answer(query, executed_tools)
        return AgentRunResult(answer=AgentAnswer(answer_text), trajectory=trajectory)

    async def _build_plan(self, query: str, tool_map: dict[str, Tool[Any, Any, Any]]) -> list[tuple[str, Any]]:
        plan: list[tuple[str, Any]] = []
        lowered = query.lower()

        if "ThinkTool" in tool_map and self._should_use_tool("ThinkTool"):
            plan.append(("ThinkTool", {"query": query, "step": "initial"}))

        handoff_tools = [tool_name for tool_name, tool in tool_map.items() if isinstance(tool, HandoffTool)]
        if handoff_tools:
            ordered = [name for name in ["DestinationResearch", "WeatherPlanning", "LanguageCulturalGuidance"] if name in handoff_tools]
            for handoff_name in ordered:
                plan.append((handoff_name, {"query": query}))
                if "ThinkTool" in tool_map and self._forces_think_after_tool():
                    plan.append(("ThinkTool", {"query": query, "step": f"after {handoff_name}"}))
            return plan

        if any(tool_name == "SimpleCalculator" for tool_name in tool_map):
            expression = _extract_expression(query)
            plan.append(("SimpleCalculator", {"expression": expression}))
            return plan

        if "WikipediaTool" in tool_map and self._should_use_tool("WikipediaTool"):
            plan.append(("WikipediaTool", WikipediaInput(query=query)))
            if "ThinkTool" in tool_map and self._forces_think_after_tool():
                plan.append(("ThinkTool", {"query": query, "step": "post research"}))

        if "OpenMeteoTool" in tool_map and self._should_use_tool("OpenMeteoTool"):
            location = "tokyo" if "tokyo" in lowered else "osaka" if "osaka" in lowered else "japan"
            plan.append(("OpenMeteoTool", WeatherInput(location=location)))

        return plan

    def _needs_permission(self, tool_name: str) -> bool:
        for requirement in self.requirements:
            if isinstance(requirement, AskPermissionRequirement):
                tools = requirement.tools
                if isinstance(tools, list):
                    if tool_name in tools:
                        return True
                elif isinstance(tools, type):
                    if tool_name == tools.__name__:
                        return True
                elif hasattr(tools, "__name__") and tool_name == tools.__name__:
                    return True
        return False

    def _should_use_tool(self, tool_name: str) -> bool:
        for requirement in self.requirements:
            if isinstance(requirement, ConditionalRequirement):
                requirement_name = requirement.tool if isinstance(requirement.tool, str) else getattr(requirement.tool, "__name__", "")
                if requirement_name == tool_name:
                    return True
        return tool_name in {tool.name for tool in self.tools}

    def _forces_think_after_tool(self) -> bool:
        for requirement in self.requirements:
            if isinstance(requirement, ConditionalRequirement):
                requirement_name = requirement.tool if isinstance(requirement.tool, str) else getattr(requirement.tool, "__name__", "")
                if requirement_name == "ThinkTool" and requirement.force_after is not None:
                    return True
        return False

    def _exceeded_max(self, tool_name: str, counts: dict[str, int]) -> bool:
        for requirement in self.requirements:
            if isinstance(requirement, ConditionalRequirement):
                requirement_name = requirement.tool if isinstance(requirement.tool, str) else getattr(requirement.tool, "__name__", "")
                if requirement_name == tool_name and requirement.max_invocations is not None:
                    return counts[tool_name] > requirement.max_invocations
        return False

    def _synthesize_answer(self, query: str, executed_tools: list[tuple[str, str]]) -> str:
        lowered = query.lower()
        tool_text = "\n".join(f"- {name}: {text}" for name, text in executed_tools)
        tool_names = [name for name, _ in executed_tools]
        if tool_names == ["OpenMeteoTool"] or tool_names == ["ThinkTool", "OpenMeteoTool"]:
            weather_text = executed_tools[-1][1]
            return f"Weather planning summary: {weather_text}"
        if tool_names == ["WikipediaTool"] or tool_names == ["ThinkTool", "WikipediaTool"]:
            wiki_text = executed_tools[-1][1]
            if "language" in self.instructions.lower() or "cultural" in self.instructions.lower():
                return f"Language and cultural guidance: {wiki_text}"
            if "destination" in self.instructions.lower():
                return f"Destination guidance: {wiki_text}"
        if "quantum computing" in lowered:
            return (
                "Quantum risk for financial institutions centers on cryptographic exposure long retention encrypted data and migration complexity.\n"
                "Main threats: broken public key cryptography harvest now decrypt later risk and vendor dependency lag.\n"
                "Timeline: preparation should start now because migration spans years before fault tolerant quantum systems arrive.\n"
                "Recommended actions: inventory cryptography prioritize customer facing systems test post quantum alternatives and coordinate with regulators.\n"
                f"Tool evidence:\n{tool_text}"
            )
        if "japan" in lowered:
            return (
                "Comprehensive travel guidance for Japan:\n"
                f"{tool_text}\n"
                "Summary: combine historical districts in Tokyo and Osaka with flexible weather aware planning and respectful etiquette such as quiet transit behavior and polite greetings."
            )
        if any(name == "SimpleCalculator" for name, _ in executed_tools):
            return executed_tools[-1][1]
        return _generate_text_response(self.instructions, query)


def _extract_expression(query: str) -> str:
    normalized = query.lower().replace("divided by", "/").replace("times", "*").replace("equals", "")
    normalized = normalized.replace("what is", "").replace("calculate", "")
    candidate = re.sub(r"[^0-9\+\-\*\/\(\)\. ]", " ", normalized)
    candidate = re.sub(r"\s+", " ", candidate).strip()
    return candidate or "0"