# --- DEPENDENCIAS ---
from config.docchat_config import RELEVANCE_TOP_K


class RelevanceChecker:
    def __init__(self, model=None):
        self.model = model

    def check(self, question: str, retriever) -> tuple[str, list]:
        top_docs = retriever.invoke(question)
        if not top_docs:
            return "NO_MATCH", []

        top_docs = top_docs[:RELEVANCE_TOP_K]
        combined_text = "\n\n".join(doc.page_content for doc in top_docs)
        question_terms = set(question.lower().split())
        content_terms = set(combined_text.lower().split())
        overlap = len(question_terms & content_terms)

        if overlap == 0:
            return "NO_MATCH", top_docs
        if overlap < max(2, len(question_terms) // 5):
            return "PARTIAL", top_docs
        return "CAN_ANSWER", top_docs