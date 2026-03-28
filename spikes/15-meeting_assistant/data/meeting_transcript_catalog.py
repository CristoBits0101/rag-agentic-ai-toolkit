# --- DEPENDENCIAS ---
from dataclasses import dataclass


@dataclass(frozen=True)
class MeetingTranscriptRecord:
    audio_file_name: str
    transcript: str


MEETING_TRANSCRIPT_RECORDS = {
    "sample-meeting.wav": MeetingTranscriptRecord(
        audio_file_name="sample-meeting.wav",
        transcript=(
            "Welcome everyone. Today we reviewed the 401k migration for the employee benefits portal. "
            "Maria will update the HSA FAQ by Friday. The team agreed to lower the ltv threshold for new mortgage applications to eighty percent. "
            "Alex will send the revised rollout plan by Tuesday. We also decided to schedule the customer pilot next Wednesday and share the draft notes with leadership."
        ),
    ),
}
