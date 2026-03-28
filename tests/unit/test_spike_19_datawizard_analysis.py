# --- DEPENDENCIAS ---
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPIKE = ROOT / "spikes" / "19-datawizard_analysis"

if str(SPIKE) not in sys.path:
    sys.path.insert(0, str(SPIKE))

from models.datawizard_baseline_chat import answer_without_tools
from models.datawizard_demo_chat_model import build_datawizard_demo_chat_model
from models.datawizard_ollama_gateway import select_best_available_ollama_model
from orchestration.datawizard_agent_orchestration import execute_datawizard_query
from orchestration.datawizard_tools_orchestration import DATAFRAME_CACHE
from orchestration.datawizard_tools_orchestration import call_dataframe_method
from orchestration.datawizard_tools_orchestration import describe_tool_schemas
from orchestration.datawizard_tools_orchestration import evaluate_classification_dataset
from orchestration.datawizard_tools_orchestration import evaluate_regression_dataset
from orchestration.datawizard_tools_orchestration import get_dataset_summaries
from orchestration.datawizard_tools_orchestration import list_csv_files
from orchestration.datawizard_tools_orchestration import preload_datasets


def clear_cache() -> None:
    DATAFRAME_CACHE.clear()


def test_list_csv_files_returns_local_datasets():
    result = list_csv_files.invoke({})

    assert result["count"] == 2
    assert result["files"] == [
        "classification-dataset.csv",
        "regression-dataset.csv",
    ]


def test_preload_datasets_reports_loaded_then_cached():
    clear_cache()

    first_result = preload_datasets.invoke(
        {"paths": ["classification-dataset.csv", "regression-dataset.csv"]}
    )
    second_result = preload_datasets.invoke(
        {"paths": ["classification-dataset.csv"]}
    )

    assert first_result["loaded"] == [
        "classification-dataset.csv",
        "regression-dataset.csv",
    ]
    assert second_result["cached"] == ["classification-dataset.csv"]


def test_get_dataset_summaries_infers_problem_type():
    clear_cache()
    summaries = get_dataset_summaries.invoke(
        {"dataset_paths": ["classification-dataset.csv", "regression-dataset.csv"]}
    )
    summaries_by_name = {summary["file_name"]: summary for summary in summaries}

    assert summaries_by_name["classification-dataset.csv"]["suggested_problem_type"] == "classification"
    assert summaries_by_name["classification-dataset.csv"]["target_column"] == "will_buy"
    assert summaries_by_name["regression-dataset.csv"]["suggested_problem_type"] == "regression"
    assert summaries_by_name["regression-dataset.csv"]["target_column"] == "weekly_sales_k"


def test_call_dataframe_method_head_returns_preview_text():
    clear_cache()
    preload_datasets.invoke({"paths": ["classification-dataset.csv"]})
    result = call_dataframe_method.invoke(
        {"file_name": "classification-dataset.csv", "method": "head"}
    )

    assert result["file_name"] == "classification-dataset.csv"
    assert "customer_age" in result["result"]
    assert "22" in result["result"]


def test_evaluate_classification_dataset_returns_accuracy():
    clear_cache()
    result = evaluate_classification_dataset.invoke(
        {"file_name": "classification-dataset.csv", "target_column": "will_buy"}
    )

    assert result["task_type"] == "classification"
    assert result["accuracy"] >= 0.8


def test_evaluate_regression_dataset_returns_metrics():
    clear_cache()
    result = evaluate_regression_dataset.invoke(
        {"file_name": "regression-dataset.csv", "target_column": "weekly_sales_k"}
    )

    assert result["task_type"] == "regression"
    assert result["r2_score"] >= 0.9
    assert result["mean_squared_error"] >= 0.0


def test_answer_without_tools_reports_limitation_for_csv_queries():
    response = answer_without_tools(
        "Can you summarize the datasets and tell me which one is classification or regression?"
    )

    assert "no puedo inspeccionar archivos csv locales" in response.lower()


def test_select_best_available_ollama_model_prefers_ranked_candidate():
    selected_model = select_best_available_ollama_model(
        ["llama3.2:3b", "qwen2.5:7b", "mistral"],
    )

    assert selected_model == "qwen2.5:7b"


def test_describe_tool_schemas_exposes_expected_arguments():
    schemas = describe_tool_schemas()
    schema_by_name = {schema["name"]: schema for schema in schemas}

    assert "paths" in schema_by_name["preload_datasets"]["args"]
    assert "target_column" in schema_by_name["evaluate_regression_dataset"]["args"]


def test_execute_datawizard_query_summarizes_and_classifies_datasets():
    clear_cache()
    result = execute_datawizard_query(
        "Can you summarize the datasets and tell me which one is classification or regression?",
        model=build_datawizard_demo_chat_model(),
    )

    assert [step.tool_name for step in result.steps] == [
        "list_csv_files",
        "preload_datasets",
        "get_dataset_summaries",
    ]
    assert "classification-dataset.csv" in result.final_answer
    assert "classification task" in result.final_answer
    assert "regression-dataset.csv" in result.final_answer
    assert "regression task" in result.final_answer


def test_execute_datawizard_query_evaluates_classification_workflow():
    clear_cache()
    result = execute_datawizard_query(
        "Evaluate classification-dataset.csv using target column will_buy.",
        model=build_datawizard_demo_chat_model(),
    )

    assert [step.tool_name for step in result.steps] == [
        "preload_datasets",
        "evaluate_classification_dataset",
    ]
    assert result.steps[1].result["accuracy"] >= 0.8
    assert "accuracy" in result.final_answer.lower()


def test_execute_datawizard_query_evaluates_regression_workflow():
    clear_cache()
    result = execute_datawizard_query(
        "Evaluate regression-dataset.csv using target column weekly_sales_k.",
        model=build_datawizard_demo_chat_model(),
    )

    assert [step.tool_name for step in result.steps] == [
        "preload_datasets",
        "evaluate_regression_dataset",
    ]
    assert result.steps[1].result["r2_score"] >= 0.9
    assert "r2" in result.final_answer.lower()
