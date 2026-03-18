# --- DEPENDENCIAS ---
from dataclasses import dataclass


@dataclass(frozen=True)
class ContentPipelineSummary:
    topic: str
    research_report: str
    blog_post: str
    social_posts: str