# --- DEPENDENCIAS ---
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPIKE = ROOT / "spikes" / "23-natural_language_sql_agent_lab"

if str(SPIKE) not in sys.path:
    sys.path.insert(0, str(SPIKE))

from models.natural_language_sql_ollama_gateway import select_best_available_ollama_model
from orchestration.natural_language_sql_agent_orchestration import build_natural_language_sql_agent
from orchestration.natural_language_sql_agent_orchestration import extract_sql_statements
from orchestration.natural_language_sql_agent_orchestration import extract_tools_called
from orchestration.natural_language_sql_agent_orchestration import invoke_natural_language_sql_query
from orchestration.natural_language_sql_database_orchestration import build_sqlite_database_uri
from orchestration.natural_language_sql_database_orchestration import count_table_rows
from orchestration.natural_language_sql_database_orchestration import ensure_chinook_database
from orchestration.natural_language_sql_database_orchestration import list_chinook_tables


class FakeToolAction:
    def __init__(self, tool: str, tool_input):
        self.tool = tool
        self.tool_input = tool_input


class FakeAgentExecutor:
    def __init__(self, response: dict):
        self._response = response
        self.inputs: list[dict] = []

    def invoke(self, input_data: dict) -> dict:
        self.inputs.append(input_data)
        return self._response


def test_ensure_chinook_database_builds_sqlite_database_from_seed(tmp_path):
    seed_path = tmp_path / "seed.sql"
    database_path = tmp_path / "chinook.db"
    seed_path.write_text(
        "CREATE TABLE Album (AlbumId INTEGER PRIMARY KEY, Title TEXT);"
        "INSERT INTO Album (Title) VALUES ('A');"
        "INSERT INTO Album (Title) VALUES ('B');",
        encoding="utf-8",
    )

    resolved_path = ensure_chinook_database(seed_path=seed_path, database_path=database_path)

    assert resolved_path == database_path
    assert count_table_rows("Album", database_path) == 2
    assert list_chinook_tables(database_path) == ["Album"]


def test_ensure_chinook_database_uses_real_seed_with_expected_album_count(tmp_path):
    database_path = tmp_path / "chinook.db"

    ensure_chinook_database(database_path=database_path)

    assert count_table_rows("Album", database_path) == 347
    assert "Track" in list_chinook_tables(database_path)


def test_build_sqlite_database_uri_uses_absolute_path(tmp_path):
    database_path = tmp_path / "chinook.db"

    uri = build_sqlite_database_uri(database_path)

    assert uri.startswith("sqlite:///")
    assert database_path.resolve().as_posix() in uri


def test_extract_sql_statements_reads_query_inputs_in_order():
    response = {
        "output": "Done.",
        "intermediate_steps": [
            (FakeToolAction("sql_db_list_tables", {}), "Album, Artist"),
            (
                FakeToolAction("sql_db_query_checker", {"query": "SELECT COUNT(*) FROM Album"}),
                "ok",
            ),
            (
                FakeToolAction("sql_db_query", {"query": "SELECT COUNT(*) AS album_count FROM Album"}),
                "[(347,)]",
            ),
        ],
    }

    assert extract_sql_statements(response) == (
        "SELECT COUNT(*) FROM Album",
        "SELECT COUNT(*) AS album_count FROM Album",
    )


def test_extract_tools_called_reads_unique_tool_names():
    response = {
        "output": "Done.",
        "intermediate_steps": [
            (FakeToolAction("sql_db_list_tables", {}), "Album, Artist"),
            (FakeToolAction("sql_db_query_checker", {"query": "SELECT COUNT(*) FROM Album"}), "ok"),
            (FakeToolAction("sql_db_query", {"query": "SELECT COUNT(*) FROM Album"}), "[(347,)]"),
        ],
    }

    assert extract_tools_called(response) == (
        "sql_db_list_tables",
        "sql_db_query_checker",
        "sql_db_query",
    )


def test_invoke_natural_language_sql_query_returns_output_sql_and_tools():
    fake_agent = FakeAgentExecutor(
        {
            "output": "There are 347 albums.",
            "intermediate_steps": [
                (FakeToolAction("sql_db_list_tables", {}), "Album, Artist"),
                (
                    FakeToolAction("sql_db_query", {"query": "SELECT COUNT(*) AS album_count FROM Album"}),
                    "[(347,)]",
                ),
            ],
        }
    )

    result = invoke_natural_language_sql_query("How many albums are there?", agent=fake_agent)

    assert fake_agent.inputs == [{"input": "How many albums are there?"}]
    assert result.output == "There are 347 albums."
    assert result.sql_statements == ("SELECT COUNT(*) AS album_count FROM Album",)
    assert result.tools_called == ("sql_db_list_tables", "sql_db_query")


def test_build_natural_language_sql_agent_uses_expected_factory_arguments(monkeypatch):
    captured = {}

    def fake_factory(llm, **kwargs):
        captured["llm"] = llm
        captured["kwargs"] = kwargs
        return "fake-agent"

    monkeypatch.setattr(
        "orchestration.natural_language_sql_agent_orchestration.create_sql_agent",
        fake_factory,
    )

    agent = build_natural_language_sql_agent(model="fake-model", database="fake-db")

    assert agent == "fake-agent"
    assert captured["llm"] == "fake-model"
    assert captured["kwargs"]["db"] == "fake-db"
    assert captured["kwargs"]["agent_type"] == "tool-calling"
    assert captured["kwargs"]["handle_parsing_errors"] is True
    assert captured["kwargs"]["agent_executor_kwargs"]["return_intermediate_steps"] is True


def test_select_best_available_ollama_model_prefers_ranked_candidate():
    selected_model = select_best_available_ollama_model(
        ["llama3.2:3b", "qwen2.5:7b", "mistral"],
    )

    assert selected_model == "qwen2.5:7b"
