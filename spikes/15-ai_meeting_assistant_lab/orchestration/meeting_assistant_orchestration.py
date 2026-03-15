# --- DEPENDENCIAS ---
from config.meeting_assistant_config import OUTPUT_FILE_NAME
from orchestration.meeting_cleanup_orchestration import extract_adjusted_transcript
from orchestration.meeting_cleanup_orchestration import product_assistant
from orchestration.meeting_minutes_orchestration import generate_meeting_minutes
from orchestration.meeting_minutes_orchestration import write_meeting_report
from orchestration.meeting_transcription_orchestration import remove_non_ascii
from orchestration.meeting_transcription_orchestration import transcribe_audio_source


def transcript_audio(audio_file: str):
    raw_transcript = transcribe_audio_source(audio_file)
    if not raw_transcript:
        return "Please provide an audio file.", None

    ascii_transcript = remove_non_ascii(raw_transcript)
    cleanup_response = product_assistant(ascii_transcript)
    adjusted_transcript = extract_adjusted_transcript(cleanup_response)
    result = generate_meeting_minutes(adjusted_transcript)
    output_file = write_meeting_report(result, OUTPUT_FILE_NAME)
    return result, output_file
