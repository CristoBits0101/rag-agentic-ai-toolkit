# --- DEPENDENCIAS ---
import re
import unicodedata
from difflib import SequenceMatcher


APPLICATION_COMMAND_STOPWORDS = {
    "a",
    "al",
    "de",
    "del",
    "el",
    "la",
    "las",
    "los",
    "me",
    "podrias",
    "por",
    "porfa",
    "porfavor",
    "puede",
    "puedes",
    "quiero",
    "un",
    "una",
}

LEAGUE_OF_LEGENDS_HINTS = {
    "diage",
    "diagraf",
    "diagrafo",
    "ims",
    "lega",
    "legends",
    "league",
    "leaguea",
    "lig",
    "liga",
    "log",
    "lol",
    "livos",
}


def normalize_text(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text or "")
    return normalized.encode("ascii", "ignore").decode("ascii").lower().strip()


def normalize_application_candidate(text: str) -> str:
    cleaned = normalize_text(re.sub(r"[^a-z0-9\s]", " ", text or ""))
    tokens = [token for token in cleaned.split() if token not in APPLICATION_COMMAND_STOPWORDS]
    return " ".join(tokens)


def extract_application_candidate(transcript: str) -> str:
    normalized = normalize_text(transcript)
    patterns = (
        r"(?:abre|abrir|lanzar|ejecuta|cierra|cerrar|cierre|termina|finaliza)\s+(.+)",
        r"(?:puede|puedes|podrias)\s+(?:abrir|cerrar)\s+(.+)",
        r"(?:jugar|abrir)\s+(?:al|el|la)?\s+(.+)",
    )
    for pattern in patterns:
        match = re.search(pattern, normalized)
        if match:
            return normalize_application_candidate(match.group(1))

    return normalize_application_candidate(normalized)


def _matches_league_of_legends(candidate_text: str) -> bool:
    if not candidate_text:
        return False

    candidate_tokens = set(candidate_text.split())
    if "legends" in candidate_tokens:
        return True

    return bool(candidate_tokens & LEAGUE_OF_LEGENDS_HINTS)


def resolve_application_name_from_transcript(
    transcript: str,
    allowed_applications: dict[str, list[str]],
    application_aliases: dict[str, str],
) -> str | None:
    normalized_transcript = normalize_text(transcript)
    if not normalized_transcript:
        return None

    for alias, resolved_name in application_aliases.items():
        if alias in normalized_transcript and resolved_name in allowed_applications:
            return resolved_name

    candidate_text = extract_application_candidate(transcript)
    if _matches_league_of_legends(candidate_text) and "league_of_legends" in allowed_applications:
        return "league_of_legends"

    best_score = 0.0
    best_application = None
    for alias, resolved_name in application_aliases.items():
        if resolved_name not in allowed_applications:
            continue

        normalized_alias = normalize_application_candidate(alias)
        if not normalized_alias:
            continue

        score = SequenceMatcher(None, candidate_text, normalized_alias).ratio()
        if normalized_alias in candidate_text or candidate_text in normalized_alias:
            score = max(score, 0.92)

        if score > best_score:
            best_score = score
            best_application = resolved_name

    if best_score >= 0.72:
        return best_application

    return None
