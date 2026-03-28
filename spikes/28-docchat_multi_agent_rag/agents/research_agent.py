# --- DEPENDENCIAS ---
from langchain_core.documents import Document


class ResearchAgent:
    def __init__(self, model):
        self.model = model

    def generate_prompt(self, question: str, context: str) -> str:
        return (
            "You are an AI assistant designed to provide precise and factual answers based on the given context. "
            "Answer the question using only the provided context. Be clear concise and factual. "
            f"Question: {question}\n\nContext:\n{context}\n\nProvide your answer below."
        )

    def sanitize_response(self, response_text: str) -> str:
        return response_text.strip()

    def run(self, question: str, documents: list[Document]) -> dict[str, str]:
        context = "\n\n".join(doc.page_content for doc in documents)
        prompt = self.generate_prompt(question, context)
        response = self.model.invoke(prompt)
        content = getattr(response, "content", response)
        draft_answer = self.sanitize_response(str(content)) or (
            "I cannot answer this question based on the provided documents."
        )
        return {
            "draft_answer": draft_answer,
            "context_used": context,
        }