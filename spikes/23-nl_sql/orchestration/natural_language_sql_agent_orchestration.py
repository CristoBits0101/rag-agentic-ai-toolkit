# --- DEPENDENCIAS ---
from langchain_community.agent_toolkits import create_sql_agent

from config.natural_language_sql_agent_config import SQL_AGENT_PREFIX
from models.natural_language_sql_entities import NaturalLanguageSQLAgentResult
from models.natural_language_sql_ollama_gateway import (
    build_natural_language_sql_ollama_chat_model,
)
from orchestration.natural_language_sql_database_orchestration import (
    build_chinook_sql_database,
)


def build_natural_language_sql_agent(model=None, database=None):
    selected_model = model or build_natural_language_sql_ollama_chat_model()
    selected_database = database or build_chinook_sql_database()
    return create_sql_agent(
        selected_model,
        db=selected_database,
        agent_type="tool-calling",
        verbose=False,
        top_k=5,
        prefix=SQL_AGENT_PREFIX,
        handle_parsing_errors=True,
        agent_executor_kwargs={"return_intermediate_steps": True},
    )


def extract_sql_statements(response: dict) -> tuple[str, ...]:
    sql_statements: list[str] = []
    for step in response.get("intermediate_steps", []):
        action = step[0]
        tool_input = getattr(action, "tool_input", {})
        if not isinstance(tool_input, dict):
            continue

        query = str(tool_input.get("query", "")).strip()
        if query and query not in sql_statements:
            sql_statements.append(query)

    return tuple(sql_statements)


def extract_tools_called(response: dict) -> tuple[str, ...]:
    tools_called: list[str] = []
    for step in response.get("intermediate_steps", []):
        action = step[0]
        tool_name = str(getattr(action, "tool", "")).strip()
        if tool_name and tool_name not in tools_called:
            tools_called.append(tool_name)

    return tuple(tools_called)


def invoke_natural_language_sql_query(
    query: str,
    agent=None,
) -> NaturalLanguageSQLAgentResult:
    selected_agent = agent or build_natural_language_sql_agent()
    response = selected_agent.invoke({"input": query})
    return NaturalLanguageSQLAgentResult(
        query=query,
        output=str(response.get("output", "")),
        sql_statements=extract_sql_statements(response),
        tools_called=extract_tools_called(response),
    )
