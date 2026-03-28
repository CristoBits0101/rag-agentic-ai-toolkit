# --- DEPENDENCIAS ---
from config.content_pipeline_config import TOPIC_KNOWLEDGE_BASE


class LocalTopicSearchTool:
    name = "local_topic_search"

    def run(self, query: str):
        lowered = query.lower().strip()
        insights = TOPIC_KNOWLEDGE_BASE.get(lowered, TOPIC_KNOWLEDGE_BASE["latest generative ai breakthroughs"])
        return {
            "query": query,
            "insights": insights,
        }