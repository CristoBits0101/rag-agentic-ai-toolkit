# --- DEPENDENCIAS ---
from dataclasses import dataclass


@dataclass(frozen=True)
class NaturalLanguageSQLAgentResult:
    query: str
    output: str
    sql_statements: tuple[str, ...]
    tools_called: tuple[str, ...]
