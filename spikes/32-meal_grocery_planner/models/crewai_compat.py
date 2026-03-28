# --- DEPENDENCIAS ---
from dataclasses import dataclass
from dataclasses import field
from enum import Enum
import json
from typing import Any
from typing import Callable


class Process(str, Enum):
    sequential = "sequential"


@dataclass
class Agent:
    role: str
    goal: str
    backstory: str
    verbose: bool = False
    allow_delegation: bool = False
    llm: Any = None
    tools: list[Any] = field(default_factory=list)


@dataclass
class Task:
    description: str
    agent: Agent
    expected_output: str
    context: list[Any] = field(default_factory=list)
    output_pydantic: Any = None
    output_file: str | None = None
    executor: Callable[..., Any] | None = None


@dataclass
class TaskOutput:
    description: str
    raw: str
    agent: str


@dataclass
class TokenUsage:
    total_tokens: int
    prompt_tokens: int
    completion_tokens: int


@dataclass
class CrewOutput:
    raw: str
    tasks_output: list[TaskOutput]
    token_usage: TokenUsage


class Crew:
    def __init__(self, agents: list[Agent], tasks: list[Task], process: Process, verbose: bool = False):
        self.agents = agents
        self.tasks = tasks
        self.process = process
        self.verbose = verbose

    def kickoff(self, inputs: dict[str, Any]):
        completed_outputs: dict[int, TaskOutput] = {}
        task_outputs: list[TaskOutput] = []
        prompt_tokens = 0
        completion_tokens = 0

        for index, task in enumerate(self.tasks):
            description = task.description.format(**inputs)
            related_context = []
            for context_task in task.context:
                context_index = self.tasks.index(context_task)
                related_context.append(completed_outputs[context_index].raw)
            context_text = "\n\n".join(related_context)
            prompt_tokens += len(description.split()) + len(context_text.split())

            result = task.executor(task.agent, description, context_text, inputs) if task.executor else description
            if task.output_pydantic and not isinstance(result, str):
                rendered = json.dumps(result.model_dump(), indent=2, ensure_ascii=False)
            else:
                rendered = str(result)
            completion_tokens += len(rendered.split())
            task_output = TaskOutput(description=description, raw=rendered, agent=task.agent.role)
            completed_outputs[index] = task_output
            task_outputs.append(task_output)

        final_raw = task_outputs[-1].raw if task_outputs else ""
        return CrewOutput(
            raw=final_raw,
            tasks_output=task_outputs,
            token_usage=TokenUsage(
                total_tokens=prompt_tokens + completion_tokens,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
            ),
        )