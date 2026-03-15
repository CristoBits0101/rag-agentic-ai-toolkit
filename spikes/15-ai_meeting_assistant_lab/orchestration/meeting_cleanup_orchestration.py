# --- DEPENDENCIAS ---
from models.meeting_assistant_demo_llm import build_cleanup_response


def product_assistant(ascii_transcript: str) -> str:
    system_prompt = (
        "You are an intelligent assistant specializing in financial products. "
        "Your task is to process transcripts of earnings calls ensuring that all references to financial products and common financial terms are in the correct format. "
        "Once you've done that, produce the adjusted transcript and a list of the words you've changed\n"
    )
    prompt_input = system_prompt + ascii_transcript
    return build_cleanup_response(prompt_input.split(system_prompt, maxsplit=1)[1])


def extract_adjusted_transcript(cleanup_response: str) -> str:
    if "Adjusted Transcript:" not in cleanup_response:
        return cleanup_response.strip()

    adjusted_block = cleanup_response.split("Adjusted Transcript:", maxsplit=1)[1]
    if "Changed Terms:" in adjusted_block:
        adjusted_block = adjusted_block.split("Changed Terms:", maxsplit=1)[0]
    return adjusted_block.strip()
