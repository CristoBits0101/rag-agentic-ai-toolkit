# --- DEPENDENCIAS ---
import re

from langchain_core.documents import Document


class VerificationAgent:
    def __init__(self, model=None):
        self.model = model

    def verify(self, question: str, answer: str, documents: list[Document]) -> dict:
        context = "\n\n".join(doc.page_content for doc in documents)
        unsupported_claims = []
        contradictions = []
        normalized_context = context.lower()

        for sentence in [item.strip() for item in answer.split(".") if item.strip()]:
            if not self._sentence_is_supported(sentence, normalized_context):
                unsupported_claims.append(sentence)

        relevant = "YES" if any(term in normalized_context for term in question.lower().split()) else "NO"
        supported = "YES" if not unsupported_claims else "NO"
        if supported == "NO" and relevant == "NO":
            contradictions.append("The answer is not grounded in the provided context.")

        verification = {
            "Supported": supported,
            "Unsupported Claims": unsupported_claims,
            "Contradictions": contradictions,
            "Relevant": relevant,
            "Additional Details": "Rule based verification against retrieved context.",
        }
        return {
            "verification": verification,
            "report": self.format_verification_report(verification),
        }

    def _sentence_is_supported(self, sentence: str, normalized_context: str) -> bool:
        tokens = [token for token in re.findall(r"[a-z0-9@.]+", sentence.lower()) if len(token) > 2]
        numeric_tokens = re.findall(r"\d+(?:\.\d+)?", sentence.lower())
        if numeric_tokens and any(token not in normalized_context for token in numeric_tokens):
            return False
        if not tokens:
            return True
        overlap = sum(1 for token in tokens if token in normalized_context)
        return overlap >= max(1, len(tokens) // 2)

    def format_verification_report(self, verification: dict) -> str:
        unsupported_claims = verification.get("Unsupported Claims", [])
        contradictions = verification.get("Contradictions", [])
        report = f"**Supported:** {verification.get('Supported', 'NO')}\n"
        report += f"**Unsupported Claims:** {', '.join(unsupported_claims) if unsupported_claims else 'None'}\n"
        report += f"**Contradictions:** {', '.join(contradictions) if contradictions else 'None'}\n"
        report += f"**Relevant:** {verification.get('Relevant', 'NO')}\n"
        report += f"**Additional Details:** {verification.get('Additional Details', 'None')}\n"
        return report