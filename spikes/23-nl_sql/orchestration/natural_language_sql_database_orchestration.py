# --- DEPENDENCIAS ---
from pathlib import Path
import sqlite3

from langchain_community.utilities.sql_database import SQLDatabase

from config.natural_language_sql_agent_config import ARTIFACTS_DIR
from config.natural_language_sql_agent_config import DATABASE_PATH
from config.natural_language_sql_agent_config import SQL_SEED_PATH


def ensure_artifacts_dir(artifacts_dir: Path = ARTIFACTS_DIR) -> Path:
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    return artifacts_dir


def database_contains_table(database_path: Path, table_name: str = "Album") -> bool:
    if not database_path.exists():
        return False

    try:
        connection = sqlite3.connect(database_path)
        try:
            row = connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table' AND name = ?",
                (table_name,),
            ).fetchone()
        finally:
            connection.close()
    except sqlite3.DatabaseError:
        return False

    return row is not None


def initialize_sqlite_database_from_seed(seed_path: Path, database_path: Path) -> Path:
    if not seed_path.exists():
        raise FileNotFoundError(f"SQL seed not found at {seed_path}.")

    ensure_artifacts_dir(database_path.parent)
    seed_sql = seed_path.read_text(encoding="utf-8")
    connection = sqlite3.connect(database_path)
    try:
        connection.executescript(seed_sql)
        connection.commit()
    finally:
        connection.close()

    return database_path


def ensure_chinook_database(
    seed_path: Path = SQL_SEED_PATH,
    database_path: Path = DATABASE_PATH,
    force_rebuild: bool = False,
) -> Path:
    if force_rebuild and database_path.exists():
        database_path.unlink()

    if database_contains_table(database_path):
        return database_path

    if database_path.exists():
        database_path.unlink()

    return initialize_sqlite_database_from_seed(seed_path, database_path)


def build_sqlite_database_uri(database_path: Path) -> str:
    resolved_path = Path(database_path).resolve()
    return f"sqlite:///{resolved_path.as_posix()}"


def build_chinook_sql_database(database_path: Path | None = None) -> SQLDatabase:
    resolved_database_path = ensure_chinook_database(database_path=database_path or DATABASE_PATH)
    database_uri = build_sqlite_database_uri(resolved_database_path)
    return SQLDatabase.from_uri(database_uri)


def list_chinook_tables(database_path: Path | None = None) -> list[str]:
    resolved_database_path = ensure_chinook_database(database_path=database_path or DATABASE_PATH)
    connection = sqlite3.connect(resolved_database_path)
    try:
        rows = connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name"
        ).fetchall()
    finally:
        connection.close()

    return [str(row[0]) for row in rows]


def count_table_rows(table_name: str, database_path: Path | None = None) -> int:
    resolved_database_path = ensure_chinook_database(database_path=database_path or DATABASE_PATH)
    connection = sqlite3.connect(resolved_database_path)
    try:
        row = connection.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()
    finally:
        connection.close()

    return int(row[0]) if row is not None else 0
