# --- DEPENDENCIAS ---
from dataclasses import dataclass
from functools import lru_cache

from models.story_demo_model import build_story_demo_model

# --- STORY ---
@dataclass(frozen=True)
class StoryGenerationContext:
    topic: str
    prompt: str
    story: str


def normalize_requested_topic(topic: str) -> str:
    return " ".join(topic.split())


def create_story_prompt(topic: str) -> str:
    return f"""Write an engaging and educational story about {topic} for beginners.
Use simple and clear language to explain basic concepts.
Include interesting facts and keep it friendly and encouraging.
The story should be around 200-300 words and end with a brief summary of what we learned.
Make it perfect for someone just starting to learn about this topic."""


@lru_cache(maxsize=16)
def build_story_generation_context(topic: str) -> StoryGenerationContext | None:
    normalized_topic = normalize_requested_topic(topic)
    if not normalized_topic:
        return None

    prompt = create_story_prompt(normalized_topic)
    story = build_story_demo_model().generate_text(prompt)

    return StoryGenerationContext(
        topic=normalized_topic,
        prompt=prompt,
        story=story,
    )


def generate_story(topic: str) -> str:
    story_context = build_story_generation_context(topic)
    if not story_context:
        return "Please provide a valid topic."

    return story_context.story
