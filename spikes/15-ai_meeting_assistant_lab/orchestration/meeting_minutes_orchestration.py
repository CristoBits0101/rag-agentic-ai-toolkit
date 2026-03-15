# --- DEPENDENCIAS ---
from pathlib import Path

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

from config.meeting_assistant_config import OUTPUT_FILE_NAME
from models.meeting_assistant_llm_gateway import build_meeting_assistant_llm


def create_meeting_minutes_prompt() -> PromptTemplate:
    template = """
Generate meeting minutes and a list of tasks based on the provided context.

Context:
{context}

Meeting Minutes:
- Key points discussed
- Decisions made

Task List:
- Actionable items with assignees and deadlines
"""
    return PromptTemplate.from_template(template)


def build_meeting_minutes_chain():
    prompt = create_meeting_minutes_prompt()
    llm = build_meeting_assistant_llm()
    return {"context": RunnablePassthrough()} | prompt | llm | StrOutputParser()


def generate_meeting_minutes(adjusted_transcript: str) -> str:
    chain = build_meeting_minutes_chain()
    return chain.invoke(adjusted_transcript)


def write_meeting_report(
    report_text: str,
    output_path: str | Path = OUTPUT_FILE_NAME,
) -> str:
    path = Path(output_path)
    path.write_text(report_text, encoding="utf-8")
    return str(path)
