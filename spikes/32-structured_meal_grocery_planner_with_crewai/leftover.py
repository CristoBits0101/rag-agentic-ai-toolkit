# --- DEPENDENCIAS ---
from pathlib import Path

import yaml

from models.crewai_compat import Agent
from models.crewai_compat import Task


class LeftoversCrew:
    def __init__(self, llm):
        self.llm = llm
        config_dir = Path(__file__).resolve().parent / "config"
        self.agents_config = yaml.safe_load((config_dir / "agents.yaml").read_text(encoding="utf-8"))
        self.tasks_config = yaml.safe_load((config_dir / "tasks.yaml").read_text(encoding="utf-8"))

    def leftover_manager(self):
        payload = self.agents_config["leftover_manager"]
        return Agent(
            role=payload["role"],
            goal=payload["goal"],
            backstory=payload["backstory"],
            verbose=payload.get("verbose", False),
            allow_delegation=payload.get("allow_delegation", False),
            llm=self.llm,
            tools=[],
        )

    def leftover_task(self, agent, executor):
        payload = self.tasks_config["leftover_task"]
        return Task(
            description=payload["description"],
            expected_output=payload["expected_output"],
            agent=agent,
            executor=executor,
        )