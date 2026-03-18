# --- DEPENDENCIAS ---
from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any


@dataclass
class ChatResult:
    summary: str
    history: list[dict[str, str]]


class ConversableAgent:
    def __init__(self, name: str, system_message: str = "", llm_config: dict[str, Any] | None = None, human_input_mode: str = "NEVER", is_termination_msg=None):
        self.name = name
        self.system_message = system_message
        self.llm_config = llm_config or {}
        self.human_input_mode = human_input_mode
        self.is_termination_msg = is_termination_msg

    def _generate_reply(self, message: str, sender: ConversableAgent | None = None) -> str:
        lowered_system = self.system_message.lower()
        lowered_message = message.lower()
        if self.name == "diagnosis":
            if any(keyword in lowered_message for keyword in ["headache", "fatigue", "dizziness"]):
                return "Possible causes include dehydration migraine tension headache or anemia. Monitor hydration rest and symptom duration."
            return "This looks like a general non emergency issue that still benefits from monitoring."
        if self.name == "pharmacy":
            return "Suggested next steps: hydrate consider basic pain relief if appropriate and avoid self medicating beyond over the counter guidance."
        if self.name == "consultation":
            urgent = any(keyword in lowered_message for keyword in ["chest pain", "fainting", "severe", "shortness of breath"])
            if urgent:
                return "A prompt doctor visit is recommended due to potentially urgent symptoms. CONSULTATION_COMPLETE"
            return "If symptoms persist or worsen schedule a doctor visit within the next few days. CONSULTATION_COMPLETE"
        if self.name == "emotion_analysis":
            if any(keyword in lowered_message for keyword in ["overwhelmed", "stressed", "anxious", "panic"]):
                return "Detected emotions: stress and anxiety with possible sleep disruption."
            return "Detected emotions: low mood with moderate stress."
        if self.name == "therapy_recommendation":
            return "Try a short breathing exercise reduce stimulation before sleep and consider journaling or speaking with a trusted professional if symptoms continue."
        return message

    def initiate_chat(self, recipient, message: str, max_turns: int = 4, summary_method: str | None = None):
        if isinstance(recipient, GroupChatManager):
            return recipient.run(self, message=message, max_turns=max_turns, summary_method=summary_method)
        history = [{"name": self.name, "content": message}]
        reply = recipient._generate_reply(message, sender=self)
        history.append({"name": recipient.name, "content": reply})
        return ChatResult(summary=reply, history=history)


@dataclass
class GroupChat:
    agents: list[ConversableAgent]
    messages: list[dict[str, str]]
    max_round: int = 5
    speaker_selection_method: str = "round_robin"


class GroupChatManager:
    def __init__(self, name: str, groupchat: GroupChat):
        self.name = name
        self.groupchat = groupchat

    def run(self, initiator: ConversableAgent, message: str, max_turns: int = 4, summary_method: str | None = None):
        history = [{"name": initiator.name, "content": message}]
        current_message = message
        for agent in self.groupchat.agents[: min(len(self.groupchat.agents), max_turns)]:
            reply = agent._generate_reply(current_message, sender=initiator)
            history.append({"name": agent.name, "content": reply})
            current_message = reply
            if agent.is_termination_msg and agent.is_termination_msg({"content": reply}):
                break
        summary = " ".join(entry["content"] for entry in history[1:])
        return ChatResult(summary=summary, history=history)