# --- DEPENDENCIAS ---
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

from models.meeting_assistant_llm_gateway import build_meeting_assistant_llm


def product_assistant(ascii_transcript: str) -> str:
    prompt = PromptTemplate.from_template(
        "You are an intelligent assistant specializing in financial products. "
        "Process the transcript and normalize common financial terms into their correct expanded format. "
        "Return the result using exactly these sections.\n"
        "Adjusted Transcript:\n"
        "Changed Terms:\n\n"
        "{transcript}"
    )
    chain = {"transcript": RunnablePassthrough()} | prompt | build_meeting_assistant_llm() | StrOutputParser()
    return chain.invoke(ascii_transcript)


def extract_adjusted_transcript(cleanup_response: str) -> str:
    if "Adjusted Transcript:" not in cleanup_response:
        return cleanup_response.strip()

    adjusted_block = cleanup_response.split("Adjusted Transcript:", maxsplit=1)[1]
    if "Changed Terms:" in adjusted_block:
        adjusted_block = adjusted_block.split("Changed Terms:", maxsplit=1)[0]
    return adjusted_block.strip()
