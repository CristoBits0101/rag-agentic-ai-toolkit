# --- DEPENDENCIAS ---
from dataclasses import dataclass
from pathlib import Path

from config.story_real_provider_config import MISTRAL_API_AUDIO_FILE_NAME
from config.story_real_provider_config import MISTRAL_API_MODEL_NAME
from config.story_real_provider_config import OLLAMA_MISTRAL_AUDIO_FILE_NAME
from config.story_real_provider_config import OLLAMA_MISTRAL_EDGE_TTS_AUDIO_FILE_NAME
from config.story_real_provider_config import OLLAMA_STORY_MODEL_NAME
from models.story_audio_gateway import save_audio_artifact
from models.story_audio_gateway import synthesize_story_audio
from models.story_edge_tts_gateway import synthesize_story_with_edge_tts
from models.story_mistral_api_gateway import generate_story_with_mistral_api
from models.story_ollama_mistral_gateway import generate_story_with_ollama_mistral
from orchestration.story_generation_orchestration import create_story_prompt
from orchestration.story_generation_orchestration import normalize_requested_topic

# --- STORY ---
@dataclass(frozen=True)
class RealStoryVariantContext:
    topic: str
    prompt: str
    story: str
    llm_provider: str
    llm_model: str


@dataclass(frozen=True)
class RealStoryVariantRun:
    topic: str
    prompt: str
    story: str
    llm_provider: str
    llm_model: str
    tts_provider: str
    output_path: Path


def build_real_story_variant_context(
    topic: str,
    story_generator,
    llm_provider: str,
    llm_model: str,
) -> RealStoryVariantContext | None:
    normalized_topic = normalize_requested_topic(topic)
    if not normalized_topic:
        return None

    prompt = create_story_prompt(normalized_topic)
    story = str(story_generator(prompt)).strip()
    return RealStoryVariantContext(
        topic=normalized_topic,
        prompt=prompt,
        story=story,
        llm_provider=llm_provider,
        llm_model=llm_model,
    )


def save_story_variant_with_default_tts(
    story_context: RealStoryVariantContext,
    output_path: str | Path,
) -> RealStoryVariantRun:
    artifact = synthesize_story_audio(story_context.story, prefer_online_tts=True)
    path = save_audio_artifact(artifact, output_path)
    return RealStoryVariantRun(
        topic=story_context.topic,
        prompt=story_context.prompt,
        story=story_context.story,
        llm_provider=story_context.llm_provider,
        llm_model=story_context.llm_model,
        tts_provider=artifact.provider,
        output_path=path,
    )


def save_story_variant_with_edge_tts(
    story_context: RealStoryVariantContext,
    output_path: str | Path,
    edge_tts_generator=None,
) -> RealStoryVariantRun:
    generator = edge_tts_generator or synthesize_story_with_edge_tts
    path = generator(story_context.story, output_path)
    return RealStoryVariantRun(
        topic=story_context.topic,
        prompt=story_context.prompt,
        story=story_context.story,
        llm_provider=story_context.llm_provider,
        llm_model=story_context.llm_model,
        tts_provider="edge_tts",
        output_path=path,
    )


def run_ollama_mistral_story_variant(
    topic: str,
    output_path: str | Path = OLLAMA_MISTRAL_AUDIO_FILE_NAME,
) -> RealStoryVariantRun | None:
    story_context = build_real_story_variant_context(
        topic=topic,
        story_generator=generate_story_with_ollama_mistral,
        llm_provider="ollama",
        llm_model=OLLAMA_STORY_MODEL_NAME,
    )
    if not story_context:
        return None

    return save_story_variant_with_default_tts(story_context, output_path)


def run_mistral_api_story_variant(
    topic: str,
    output_path: str | Path = MISTRAL_API_AUDIO_FILE_NAME,
) -> RealStoryVariantRun | None:
    story_context = build_real_story_variant_context(
        topic=topic,
        story_generator=generate_story_with_mistral_api,
        llm_provider="mistral_api",
        llm_model=MISTRAL_API_MODEL_NAME,
    )
    if not story_context:
        return None

    return save_story_variant_with_default_tts(story_context, output_path)


def run_ollama_mistral_edge_tts_story_variant(
    topic: str,
    output_path: str | Path = OLLAMA_MISTRAL_EDGE_TTS_AUDIO_FILE_NAME,
) -> RealStoryVariantRun | None:
    story_context = build_real_story_variant_context(
        topic=topic,
        story_generator=generate_story_with_ollama_mistral,
        llm_provider="ollama",
        llm_model=OLLAMA_STORY_MODEL_NAME,
    )
    if not story_context:
        return None

    return save_story_variant_with_edge_tts(story_context, output_path)
