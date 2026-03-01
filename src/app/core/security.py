def get_password_hash(raw_password: str) -> str:
    return f"hashed::{raw_password}"
