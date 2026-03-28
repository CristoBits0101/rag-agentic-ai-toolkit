# --- DEPENDENCIAS ---
from models.voice_microphone_gateway import build_recording_path
from models.voice_microphone_gateway import record_audio_with_push_to_talk
from models.voice_transcription_gateway import transcribe_audio_file
from orchestration.voice_desktop_session_orchestration import process_voice_transcript
from orchestration.voice_desktop_session_orchestration import should_exit_session


def run_voice_desktop_assistant_lab() -> None:
    print("Voice Desktop Assistant")
    print("Hold space to talk.")
    print("Release the key to send the command.")
    print("Say salir to close the assistant.")
    print("Deletion requests always require confirmation.")

    pending_plan = None
    recording_path = build_recording_path()

    while True:
        try:
            audio_path = record_audio_with_push_to_talk(recording_path)
            transcript = transcribe_audio_file(audio_path)
        except KeyboardInterrupt:
            print("Session interrupted by user.")
            break
        except Exception as exc:
            print(f"Assistant: {exc}")
            continue

        print(f"User: {transcript}")
        if should_exit_session(transcript):
            print("Assistant: Session closed.")
            break

        result, pending_plan = process_voice_transcript(transcript, pending_plan=pending_plan)
        print(f"Assistant: {result.message}")
