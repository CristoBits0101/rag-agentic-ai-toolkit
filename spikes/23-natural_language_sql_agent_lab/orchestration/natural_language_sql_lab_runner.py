# --- DEPENDENCIAS ---
from config.natural_language_sql_agent_config import LAB_INTRODUCTION
from config.natural_language_sql_agent_config import SAMPLE_QUERIES
from orchestration.natural_language_sql_agent_orchestration import (
    build_natural_language_sql_agent,
)
from orchestration.natural_language_sql_agent_orchestration import (
    invoke_natural_language_sql_query,
)
from orchestration.natural_language_sql_database_orchestration import count_table_rows
from orchestration.natural_language_sql_database_orchestration import ensure_chinook_database
from orchestration.natural_language_sql_database_orchestration import list_chinook_tables


def print_divider(title: str) -> None:
    print(f"\n=== {title} ===")


def print_result(result) -> None:
    print(f"Question: {result.query}")
    print(f"Answer: {result.output}")
    print(f"Tools: {list(result.tools_called)}")
    if result.sql_statements:
        print("SQL:")
        for statement in result.sql_statements:
            print(statement)


def run_natural_language_sql_lab() -> None:
    database_path = ensure_chinook_database()
    table_names = list_chinook_tables(database_path)
    album_count = count_table_rows("Album", database_path)
    agent = build_natural_language_sql_agent()

    print(LAB_INTRODUCTION)

    print_divider("Database")
    print(f"Path: {database_path}")
    print(f"Tables: {table_names}")
    print(f"Album rows: {album_count}")

    print_divider("Queries")
    for task in SAMPLE_QUERIES:
        result = invoke_natural_language_sql_query(task["query"], agent=agent)
        print(f"\nTitle: {task['title']}")
        print_result(result)
