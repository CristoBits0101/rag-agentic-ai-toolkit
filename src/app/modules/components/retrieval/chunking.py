def chunk_text(text: str, chunk_size: int = 500) -> list[str]:
    if chunk_size <= 0:
        return [text]
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
