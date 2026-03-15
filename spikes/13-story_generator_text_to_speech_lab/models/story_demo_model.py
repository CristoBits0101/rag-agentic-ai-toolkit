# --- DEPENDENCIAS ---
import re
from dataclasses import dataclass

# --- MODEL ---
@dataclass(frozen=True)
class StoryTopicBlueprint:
    sections: tuple[str, ...]
    summary: str


TOPIC_BLUEPRINTS = {
    "the life cycle of butterflies": StoryTopicBlueprint(
        sections=(
            "A butterfly begins life as a tiny egg attached to a leaf where it is protected while a new insect starts to grow.",
            "Soon the egg opens and a caterpillar appears. This larva stage is all about eating because the caterpillar must gather enough energy for the huge changes ahead.",
            "As the caterpillar grows it sheds its skin several times. Each time it becomes a little larger and a little more ready for the next stage of life.",
            "When the caterpillar is fully grown it forms a chrysalis. Inside that shell one of nature's most amazing changes takes place and the body is reorganized through metamorphosis.",
            "At last an adult butterfly emerges with soft folded wings. After resting and pumping fluid into the wings it can fly away to drink nectar and help pollinate flowers.",
            "The adult butterfly eventually lays eggs of its own which begins the cycle again and shows how each stage has a special job in the life of the insect.",
        ),
        summary=(
            "In summary we learned that butterflies move through four main stages which are egg caterpillar chrysalis and adult. "
            "Each stage helps the insect grow survive and continue the cycle of life."
        ),
    ),
    "the life cycle of a human": StoryTopicBlueprint(
        sections=(
            "A human life begins before birth while a baby is developing inside the mother. During this time the body forms organs bones and the basic systems needed for life.",
            "After birth the infant stage begins. Babies grow quickly and depend on adults for food comfort safety and care while they learn to smile move and recognize familiar voices.",
            "Childhood is a time of strong learning. Children develop language motor skills curiosity and friendships while their bodies and brains continue to mature.",
            "During the teenage years people experience puberty which brings major physical and emotional changes. Teenagers also develop a stronger sense of identity and independence.",
            "Adulthood often includes work family responsibility and community life. Adults keep learning while making decisions that shape their health goals and relationships.",
            "Later in life older adulthood brings reflection experience and new changes in the body. Healthy habits support quality of life and every stage contributes to the full human journey.",
        ),
        summary=(
            "In summary we learned that the human life cycle includes development before birth infancy childhood adolescence adulthood and older adulthood. "
            "Growth learning and change continue across the whole lifespan."
        ),
    ),
}


def normalize_topic(topic: str) -> str:
    return " ".join(topic.lower().split())


def extract_topic_from_prompt(prompt: str) -> str:
    match = re.search(r"about (.+?) for beginners", prompt, flags=re.IGNORECASE)
    if match:
        return normalize_topic(match.group(1))

    return normalize_topic(prompt)


def build_story_from_blueprint(blueprint: StoryTopicBlueprint, topic: str) -> str:
    introduction = (
        f"Here is a friendly story about {topic}. "
        "It uses simple language so a beginner can follow the main ideas step by step."
    )
    body = " ".join(blueprint.sections)
    return f"{introduction} {body} {blueprint.summary}"


def build_fallback_story(topic: str) -> str:
    return (
        f"Here is a beginner friendly story about {topic}. "
        f"We start by noticing that {topic} changes over time through clear stages and each stage has an important purpose. "
        "At the beginning something small or simple appears and starts to grow. "
        "Next it develops new abilities and responds to its environment. "
        "Then a major change happens which prepares it for a more mature stage. "
        "Finally it reaches a stage where it can support new life or new cycles and continue the process again. "
        "In summary we learned that life cycles and growth patterns help us understand how change happens in an organized way."
    )


def build_educational_story(topic: str) -> str:
    normalized_topic = normalize_topic(topic)
    blueprint = TOPIC_BLUEPRINTS.get(normalized_topic)

    if blueprint:
        return build_story_from_blueprint(blueprint, normalized_topic)

    return build_fallback_story(normalized_topic)


class EducationalStoryDemoModel:
    def generate_text(self, prompt: str) -> str:
        topic = extract_topic_from_prompt(prompt)
        return build_educational_story(topic)


def build_story_demo_model() -> EducationalStoryDemoModel:
    return EducationalStoryDemoModel()
