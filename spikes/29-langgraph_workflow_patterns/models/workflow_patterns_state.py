# --- DEPENDENCIAS ---
from typing import TypedDict


class ChainState(TypedDict, total=False):
    job_description: str
    resume_summary: str
    cover_letter: str


class RouterState(TypedDict, total=False):
    user_input: str
    task_type: str
    output: str


class TranslationState(TypedDict, total=False):
    text: str
    french: str
    spanish: str
    japanese: str
    combined_output: str


class ServiceRouterState(TypedDict, total=False):
    user_input: str
    task_type: str
    output: str