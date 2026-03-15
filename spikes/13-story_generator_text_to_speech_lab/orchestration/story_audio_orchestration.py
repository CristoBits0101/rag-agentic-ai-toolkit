# --- DEPENDENCIAS ---
from dataclasses import dataclass
from pathlib import Path

from config.story_tts_config import DEFAULT_AUDIO_FILE_NAME
from models.story_audio_gateway import StoryAudioArtifact
from models.story_audio_gateway import save_audio_artifact
from models.story_audio_gateway import synthesize_story_audio
from orchestration.story_generation_orchestration import generate_story

# --- AUDIO ---
@dataclass(frozen=True)
class StoryAudioContext:
    topic: str
    story: str
    artifact: StoryAudioArtifact


def build_story_audio_context(
    topic: str,
    prefer_online_tts: bool = False,
) -> StoryAudioContext | None:
    story = generate_story(topic)
    if story == "Please provide a valid topic.":
        return None

    artifact = synthesize_story_audio(story, prefer_online_tts=prefer_online_tts)
    return StoryAudioContext(topic=topic, story=story, artifact=artifact)


def save_generated_story_audio(
    topic: str,
    output_path: str | Path = DEFAULT_AUDIO_FILE_NAME,
    prefer_online_tts: bool = False,
) -> Path | None:
    audio_context = build_story_audio_context(topic, prefer_online_tts=prefer_online_tts)
    if not audio_context:
        return None

    return save_audio_artifact(audio_context.artifact, output_path)
