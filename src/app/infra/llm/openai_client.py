class OpenAIClient:
    def __init__(self, model: str = "gpt-4o-mini") -> None:
        self.model = model

    def complete(self, prompt: str) -> str:
        # Placeholder adapter to keep architecture boundaries explicit.
        return f"openai placeholder ({self.model}): {prompt}"
