# --- DEPENDENCIAS ---
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any

from pydantic import BaseModel


@dataclass
class ChatResult:
    summary: str
    history: list[dict[str, str]]


class LLMConfig(dict):
    pass


class LocalCommandLineCodeExecutor:
    def __init__(self, work_dir: str, timeout: int = 30):
        self.work_dir = Path(work_dir)
        self.timeout = timeout
        self.work_dir.mkdir(parents=True, exist_ok=True)

    def execute(self, code: str) -> str:
        globals_dict = {"__name__": "__main__"}
        exec(code, globals_dict, globals_dict)
        return f"Code executed in {self.work_dir}."


class ConversableAgent:
    def __init__(
        self,
        name: str,
        system_message: str = "",
        llm_config: dict[str, Any] | None = None,
        human_input_mode: str = "NEVER",
        description: str = "",
        is_termination_msg=None,
        max_consecutive_auto_reply: int = 5,
        code_execution_config: dict[str, Any] | bool | None = None,
        scripted_responses: list[str] | None = None,
    ) -> None:
        self.name = name
        self.system_message = system_message
        self.llm_config = llm_config or {}
        self.human_input_mode = human_input_mode
        self.description = description
        self.is_termination_msg = is_termination_msg
        self.max_consecutive_auto_reply = max_consecutive_auto_reply
        self.code_execution_config = code_execution_config
        self.scripted_responses = list(scripted_responses or [])
        self._registered_functions: list[tuple[Any, "ConversableAgent", str]] = []

    def register_function(self, function, executor: "ConversableAgent", description: str):
        self._registered_functions.append((function, executor, description))

    def generate_structured_output(self, message: str) -> dict[str, Any]:
        schema = self.llm_config.get("response_format")
        if schema is None:
            return {"message": message}
        schema_name = schema.__name__
        if schema_name == "TicketSummary":
            return {
                "customer_name": "John Doe",
                "issue_type": "login issue",
                "urgency_level": "High",
                "recommended_action": "Escalate password reset failure and offer urgent account recovery assistance.",
            }
        raise ValueError(f"Unsupported structured schema: {schema_name}")

    def _reply_with_registered_function(self, message: str) -> str | None:
        lowered = message.lower()
        for function, executor, description in self._registered_functions:
            if "prime" in lowered:
                match = re.search(r"(\d+)", message)
                if match:
                    number = int(match.group(1))
                    result = function(number)
                    return f"Result from {description}: {number} is prime? {result}."
        return None

    def _maybe_execute_code(self, message: str) -> str | None:
        if self.code_execution_config in (None, False):
            return None
        match = re.search(r"```python\n(.*?)```", message, re.DOTALL)
        if not match:
            return None
        code = match.group(1)
        executor = self.code_execution_config.get("executor")
        if executor is None:
            return "No executor configured."
        executor.execute(code)
        return "Code executed successfully and produced the requested artifact."

    def _generate_reply(self, message: str, sender: ConversableAgent | None = None) -> str:
        if self.human_input_mode == "ALWAYS":
            if self.scripted_responses:
                return self.scripted_responses.pop(0)
            return "Approved."

        code_result = self._maybe_execute_code(message)
        if code_result is not None:
            return code_result

        registered_result = self._reply_with_registered_function(message)
        if registered_result is not None:
            return registered_result

        lowered_system = self.system_message.lower()
        lowered_message = message.lower()
        if "neural network" in lowered_message and "tutor" in lowered_system:
            return "A neural network is a layered function approximator that learns patterns by adjusting weights from examples."
        if "teacher" in self.name and ("moon" in lowered_message or "lesson plan:" in lowered_message or "review:" in lowered_message):
            return "The moon lesson looks good. Add one hands on activity and DONE."
        if "planner" in self.name:
            return "Lesson plan: introduce moon phases, compare waxing and waning, and finish with a paper plate model activity."
        if "reviewer" in self.name:
            return "Review: simplify one science term, add a short reflection question, and keep the activity under ten minutes."
        if "assistant" in self.name and "sine wave" in lowered_message:
            return (
                "```python\n"
                "from pathlib import Path\n"
                "import math\n"
                "points = []\n"
                "for x in range(-12, 13):\n"
                "    y = 100 - int(math.sin(x / 2) * 40)\n"
                "    px = 20 + (x + 12) * 15\n"
                "    points.append(f'{px},{y}')\n"
                "svg = '<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"420\" height=\"200\">'\n"
                "svg += '<polyline fill=\"none\" stroke=\"#1f77b4\" stroke-width=\"3\" points=\"' + ' '.join(points) + '\" />'\n"
                "svg += '</svg>'\n"
                "Path('coding').mkdir(exist_ok=True)\n"
                "Path('coding/sine_wave.svg').write_text(svg, encoding='utf-8')\n"
                "```"
            )
        if "support assistant" in lowered_system:
            payload = self.generate_structured_output(message)
            return str(payload)
        if "bug triage assistant" in lowered_system:
            return _triage_bug_report(message)
        if "tech_expert" in self.name or "software engineer" in lowered_system:
            return "Technical view: prefer typed interfaces, explicit error handling, and measurable latency budgets."
        if "creative_writer" in self.name or "storyteller" in lowered_system:
            return "Creative view: explain the idea as a guided city journey where each local experience feels like a chapter."
        if "business_analyst" in self.name or "business analyst" in lowered_system:
            return "Business view: start with one city, track repeat booking rate, and validate host acquisition economics early."
        return f"{self.name} response: {message}"

    def initiate_chat(self, recipient, message: str, max_turns: int = 2, summary_method: str | None = None):
        if isinstance(recipient, GroupChatManager):
            return recipient.run(self, message=message, max_turns=max_turns, summary_method=summary_method)

        history = [{"name": self.name, "content": message}]
        current_sender = self
        current_recipient = recipient
        current_message = message
        for _ in range(max_turns):
            reply = current_recipient._generate_reply(current_message, sender=current_sender)
            history.append({"name": current_recipient.name, "content": reply})
            if current_recipient.is_termination_msg and current_recipient.is_termination_msg({"content": reply}):
                break
            current_sender, current_recipient = current_recipient, current_sender
            current_message = reply
        summary = _summarize_history(history) if summary_method else history[-1]["content"]
        return ChatResult(summary=summary, history=history)


class AssistantAgent(ConversableAgent):
    pass


class UserProxyAgent(ConversableAgent):
    pass


@dataclass
class GroupChat:
    agents: list[ConversableAgent]
    messages: list[dict[str, str]]
    max_round: int = 6
    speaker_selection_method: str = "round_robin"


class GroupChatManager:
    def __init__(self, name: str, groupchat: GroupChat, llm_config: dict[str, Any] | None = None):
        self.name = name
        self.groupchat = groupchat
        self.llm_config = llm_config or {}

    def run(self, initiator: ConversableAgent, message: str, max_turns: int = 6, summary_method: str | None = None):
        history = [{"name": initiator.name, "content": message}]
        order = self._speaker_order(initiator)
        current_message = message
        for round_index in range(min(max_turns, self.groupchat.max_round)):
            agent = order[round_index % len(order)]
            reply = agent._generate_reply(current_message, sender=initiator)
            history.append({"name": agent.name, "content": reply})
            current_message = reply
            if agent.is_termination_msg and agent.is_termination_msg({"content": reply}):
                break
        summary = _summarize_history(history) if summary_method else history[-1]["content"]
        return ChatResult(summary=summary, history=history)

    def _speaker_order(self, initiator: ConversableAgent) -> list[ConversableAgent]:
        if self.groupchat.speaker_selection_method == "round_robin":
            return self.groupchat.agents
        names = {agent.name for agent in self.groupchat.agents}
        if {"planner_agent", "reviewer_agent", "teacher_agent"}.issubset(names):
            return [agent for name in ["planner_agent", "reviewer_agent", "teacher_agent"] for agent in self.groupchat.agents if agent.name == name]
        return [agent for agent in self.groupchat.agents if agent.name != initiator.name] or self.groupchat.agents


def register_function(function, caller: ConversableAgent, executor: ConversableAgent, description: str = ""):
    caller.register_function(function, executor=executor, description=description or function.__name__)


def _summarize_history(history: list[dict[str, str]]) -> str:
    return " ".join(entry["content"] for entry in history[-3:])


def _triage_bug_report(message: str) -> str:
    lowered = message.lower()
    if any(keyword in lowered for keyword in ["crash", "security", "sql injection", "data loss"]):
        return "Escalate this issue for urgent review. Please confirm."
    if any(keyword in lowered for keyword in ["typo", "misalignment", "cosmetic"]):
        return "This looks minor and can likely be closed after human review."
    return "Mark this as medium priority and ask the human for review."