# --- DEPENDENCIAS ---
import json
import re
from typing import Any

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage
from langchain_core.messages import BaseMessage
from langchain_core.messages import HumanMessage
from langchain_core.messages import ToolMessage
from langchain_core.messages.tool import tool_call
from langchain_core.outputs import ChatGeneration
from langchain_core.outputs import ChatResult
from langchain_core.runnables import RunnableLambda
from langchain_core.tools import BaseTool


def normalize_query_text(text: str) -> str:
    return " ".join(text.lower().split())


def parse_tool_message_content(message: ToolMessage) -> dict[str, Any]:
    try:
        return json.loads(message.content)
    except json.JSONDecodeError:
        return {"result": message.content}


def build_tool_call_message(tool_name: str, arguments: dict[str, Any], call_id: str) -> AIMessage:
    return AIMessage(
        content="",
        tool_calls=[
            tool_call(
                name=tool_name,
                args=arguments,
                id=call_id,
            )
        ],
    )


def find_original_query(messages: list[BaseMessage]) -> str:
    for message in messages:
        if isinstance(message, HumanMessage):
            return str(message.content)

    return ""


def extract_tool_messages(messages: list[BaseMessage]) -> list[ToolMessage]:
    return [message for message in messages if isinstance(message, ToolMessage)]


def extract_dataset_name_from_query(query: str) -> str | None:
    match = re.search(r"([a-z0-9_-]+\.csv)", query.lower())
    if match:
        return match.group(1)

    if "classification dataset" in query.lower():
        return "classification-dataset.csv"

    if "regression dataset" in query.lower():
        return "regression-dataset.csv"

    return None


def extract_target_column(query: str) -> str | None:
    match = re.search(r"target column ([a-zA-Z_][a-zA-Z0-9_]*)", query)
    if match:
        return match.group(1)

    return None


def is_dataset_listing_query(query: str) -> bool:
    normalized_query = normalize_query_text(query)
    return "what datasets are available" in normalized_query or (
        "list" in normalized_query and "dataset" in normalized_query
    )


def is_summary_query(query: str) -> bool:
    normalized_query = normalize_query_text(query)
    return any(
        marker in normalized_query
        for marker in [
            "summarize the datasets",
            "tell me about the dataset",
            "classification or regression",
        ]
    )


def is_preview_query(query: str) -> bool:
    normalized_query = normalize_query_text(query)
    return "first rows" in normalized_query or "preview" in normalized_query


def is_classification_evaluation_query(query: str) -> bool:
    normalized_query = normalize_query_text(query)
    return "evaluate classification-dataset" in normalized_query


def is_regression_evaluation_query(query: str) -> bool:
    normalized_query = normalize_query_text(query)
    return "evaluate regression-dataset" in normalized_query


def build_initial_tool_message(query: str) -> AIMessage:
    if is_dataset_listing_query(query) or is_summary_query(query):
        return build_tool_call_message("list_csv_files", {}, "call_list_1")

    if is_preview_query(query):
        dataset_name = extract_dataset_name_from_query(query) or "classification-dataset.csv"
        return build_tool_call_message(
            "preload_datasets",
            {"paths": [dataset_name]},
            "call_preload_preview_1",
        )

    if is_classification_evaluation_query(query):
        dataset_name = extract_dataset_name_from_query(query) or "classification-dataset.csv"
        return build_tool_call_message(
            "preload_datasets",
            {"paths": [dataset_name]},
            "call_preload_classification_1",
        )

    if is_regression_evaluation_query(query):
        dataset_name = extract_dataset_name_from_query(query) or "regression-dataset.csv"
        return build_tool_call_message(
            "preload_datasets",
            {"paths": [dataset_name]},
            "call_preload_regression_1",
        )

    return AIMessage(
        content=(
            "I can inspect local CSV datasets summarize them preview cached frames and "
            "evaluate classification or regression models."
        )
    )


def build_follow_up_tool_message(query: str, tool_messages: list[ToolMessage]) -> AIMessage | None:
    last_message = tool_messages[-1]
    last_payload = parse_tool_message_content(last_message)

    if last_message.name == "list_csv_files" and is_summary_query(query):
        return build_tool_call_message(
            "preload_datasets",
            {"paths": last_payload["files"]},
            "call_preload_summary_2",
        )

    if last_message.name == "preload_datasets" and is_summary_query(query):
        return build_tool_call_message(
            "get_dataset_summaries",
            {"dataset_paths": last_payload["active"]},
            "call_summaries_3",
        )

    if last_message.name == "preload_datasets" and is_preview_query(query):
        dataset_name = extract_dataset_name_from_query(query) or last_payload["active"][0]
        return build_tool_call_message(
            "call_dataframe_method",
            {"file_name": dataset_name, "method": "head"},
            "call_dataframe_2",
        )

    if last_message.name == "preload_datasets" and is_classification_evaluation_query(query):
        dataset_name = extract_dataset_name_from_query(query) or last_payload["active"][0]
        target_column = extract_target_column(query) or "will_buy"
        return build_tool_call_message(
            "evaluate_classification_dataset",
            {"file_name": dataset_name, "target_column": target_column},
            "call_evaluate_classification_2",
        )

    if last_message.name == "preload_datasets" and is_regression_evaluation_query(query):
        dataset_name = extract_dataset_name_from_query(query) or last_payload["active"][0]
        target_column = extract_target_column(query) or "weekly_sales_k"
        return build_tool_call_message(
            "evaluate_regression_dataset",
            {"file_name": dataset_name, "target_column": target_column},
            "call_evaluate_regression_2",
        )

    return None


def build_summary_text(summary_payload: dict[str, Any] | list[dict[str, Any]]) -> str:
    if isinstance(summary_payload, dict):
        summaries = summary_payload.get("result", [])
    else:
        summaries = summary_payload

    lines = []
    for summary in summaries:
        lines.append(
            f"{summary['file_name']} has {summary['row_count']} rows and {summary['column_count']} columns. "
            f"Its target column is {summary['target_column']} and it looks like a {summary['suggested_problem_type']} task."
        )
    return " ".join(lines)


def build_final_message(query: str, tool_messages: list[ToolMessage]) -> AIMessage:
    last_message = tool_messages[-1]
    last_payload = parse_tool_message_content(last_message)

    if "error" in last_payload:
        return AIMessage(content=last_payload["error"])

    if last_message.name == "list_csv_files":
        return AIMessage(
            content="Available datasets: " + ", ".join(last_payload["files"]) + "."
        )

    if last_message.name == "get_dataset_summaries":
        return AIMessage(content=build_summary_text(last_payload))

    if last_message.name == "call_dataframe_method":
        return AIMessage(
            content=(
                f"Here is the {last_payload['method']} output for {last_payload['file_name']}:\n"
                f"{last_payload['result']}"
            )
        )

    if last_message.name == "evaluate_classification_dataset":
        return AIMessage(
            content=(
                f"The classification evaluation for {last_payload['file_name']} using "
                f"{last_payload['target_column']} reached accuracy {last_payload['accuracy']}."
            )
        )

    if last_message.name == "evaluate_regression_dataset":
        return AIMessage(
            content=(
                f"The regression evaluation for {last_payload['file_name']} using "
                f"{last_payload['target_column']} reached r2 {last_payload['r2_score']} "
                f"with mean squared error {last_payload['mean_squared_error']}."
            )
        )

    return AIMessage(content="I have completed the requested data analysis workflow.")


def coerce_messages_input(messages_input: Any) -> list[BaseMessage]:
    if isinstance(messages_input, dict) and "messages" in messages_input:
        return messages_input["messages"]

    return messages_input


class DataWizardDemoChatModel(BaseChatModel):
    @property
    def _llm_type(self) -> str:
        return "datawizard_demo_chat_model"

    @property
    def _identifying_params(self) -> dict[str, str]:
        return {"model_name": "datawizard_demo_chat_model"}

    def _generate(
        self,
        messages: list[BaseMessage],
        stop: list[str] | None = None,
        run_manager=None,
        **kwargs,
    ) -> ChatResult:
        response = self.build_response(messages, {})
        return ChatResult(generations=[ChatGeneration(message=response)])

    def bind_tools(
        self,
        tools: list[dict[str, Any] | type | Any | BaseTool],
        *,
        tool_choice: str | None = None,
        **kwargs: Any,
    ):
        tool_map = {
            tool.name: tool
            for tool in tools
            if hasattr(tool, "name")
        }
        return RunnableLambda(
            lambda messages_input: self.build_response(
                coerce_messages_input(messages_input),
                tool_map,
            )
        )

    def build_response(
        self,
        messages: list[BaseMessage],
        tool_map: dict[str, BaseTool],
    ) -> AIMessage:
        query = find_original_query(messages)
        tool_messages = extract_tool_messages(messages)

        if not tool_map or not tool_messages:
            return build_initial_tool_message(query)

        follow_up_message = build_follow_up_tool_message(query, tool_messages)
        if follow_up_message is not None:
            return follow_up_message

        return build_final_message(query, tool_messages)


def build_datawizard_demo_chat_model() -> DataWizardDemoChatModel:
    return DataWizardDemoChatModel()
