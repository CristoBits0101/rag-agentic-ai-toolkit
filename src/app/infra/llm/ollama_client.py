class OllamaClient:
    def __init__(self, model: str = "llama3.2:3b") -> None:
        self.model = model

    def complete(self, prompt: str) -> str:
        # Placeholder adapter to keep architecture boundaries explicit.
        return f"ollama placeholder ({self.model}): {prompt}"
