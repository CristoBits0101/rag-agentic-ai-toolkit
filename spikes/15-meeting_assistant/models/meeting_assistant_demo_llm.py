# --- DEPENDENCIAS ---
import re

from langchain_core.language_models.llms import LLM


def normalize_text(text: str) -> str:
    return " ".join(text.split())


def extract_transcript_from_cleanup_prompt(prompt: str) -> str:
    marker = "Once you've done that, produce the adjusted transcript and a list of the words you've changed"
    if marker in prompt:
        return prompt.split(marker, maxsplit=1)[1].strip()

    return prompt.strip()


def replace_financial_terms(transcript: str) -> tuple[str, list[str]]:
    adjusted = transcript
    changed_terms = []

    replacements = [
        ("401k", "401(k) retirement savings plan"),
        ("HSA", "Health Savings Account (HSA)"),
        ("ltv", "Loan to Value (LTV)"),
    ]

    for source, target in replacements:
        if re.search(re.escape(source), adjusted, flags=re.IGNORECASE):
            adjusted = re.sub(re.escape(source), target, adjusted, flags=re.IGNORECASE)
            changed_terms.append(source)

    adjusted = re.sub(
        r"eighty percent",
        "80 percent",
        adjusted,
        flags=re.IGNORECASE,
    )
    if "eighty percent" in transcript.lower():
        changed_terms.append("eighty percent")

    return normalize_text(adjusted), changed_terms


def build_cleanup_response(transcript: str) -> str:
    adjusted_transcript, changed_terms = replace_financial_terms(transcript)
    changed_terms_text = ", ".join(changed_terms) if changed_terms else "none"
    return (
        f"Adjusted Transcript:\n{adjusted_transcript}\n\n"
        f"Changed Terms:\n{changed_terms_text}"
    )


def extract_context_from_minutes_prompt(prompt: str) -> str:
    if "Context:" not in prompt:
        return ""

    context = prompt.split("Context:", maxsplit=1)[1]
    if "Meeting Minutes:" in context:
        context = context.split("Meeting Minutes:", maxsplit=1)[0]
    return normalize_text(context)


def build_meeting_minutes_response(context: str) -> str:
    lowered_context = context.lower()

    key_points = [
        "The team reviewed the employee benefits portal migration.",
        "The discussion covered retirement and health benefit communications.",
        "A customer pilot and rollout planning were aligned with leadership follow up.",
    ]
    decisions = [
        "Lower the Loan to Value (LTV) threshold for new mortgage applications to 80 percent.",
        "Schedule the customer pilot for next Wednesday.",
    ]
    tasks = [
        "Maria: Update the Health Savings Account (HSA) FAQ by Friday.",
        "Alex: Send the revised rollout plan by Tuesday.",
        "Team: Share draft meeting notes with leadership after the pilot schedule is confirmed.",
    ]

    if "401(k)" not in context and "retirement savings plan" not in lowered_context:
        key_points[0] = "The team reviewed a benefits related rollout."

    return (
        "Meeting Minutes:\n"
        "- Key points discussed:\n"
        f"  - {key_points[0]}\n"
        f"  - {key_points[1]}\n"
        f"  - {key_points[2]}\n"
        "- Decisions made:\n"
        f"  - {decisions[0]}\n"
        f"  - {decisions[1]}\n\n"
        "Task List:\n"
        f"- {tasks[0]}\n"
        f"- {tasks[1]}\n"
        f"- {tasks[2]}"
    )


class MeetingAssistantDemoLLM(LLM):
    @property
    def _llm_type(self) -> str:
        return "meeting_assistant_demo_llm"

    @property
    def _identifying_params(self) -> dict[str, str]:
        return {"model_name": "meeting_assistant_demo_llm"}

    def _call(
        self,
        prompt: str,
        stop: list[str] | None = None,
        run_manager=None,
        **kwargs,
    ) -> str:
        if "You are an intelligent assistant specializing in financial products" in prompt:
            transcript = extract_transcript_from_cleanup_prompt(prompt)
            return build_cleanup_response(transcript)

        if "Generate meeting minutes and a list of tasks based on the provided context." in prompt:
            context = extract_context_from_minutes_prompt(prompt)
            return build_meeting_minutes_response(context)

        return normalize_text(prompt)[:240]


def build_meeting_assistant_demo_llm() -> MeetingAssistantDemoLLM:
    return MeetingAssistantDemoLLM()
