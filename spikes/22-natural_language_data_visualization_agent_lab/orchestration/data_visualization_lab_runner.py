# --- DEPENDENCIAS ---
from config.data_visualization_agent_config import AGE_FILTER_QUERY
from config.data_visualization_agent_config import EXERCISE_QUERIES
from config.data_visualization_agent_config import LAB_INTRODUCTION
from config.data_visualization_agent_config import ROW_COUNT_QUERY
from config.data_visualization_agent_config import VISUALIZATION_QUERIES
from orchestration.data_visualization_agent_orchestration import (
    build_data_visualization_agent,
)
from orchestration.data_visualization_agent_orchestration import (
    invoke_data_visualization_query,
)
from orchestration.data_visualization_dataset_orchestration import build_artifact_path
from orchestration.data_visualization_dataset_orchestration import clear_generated_artifacts
from orchestration.data_visualization_dataset_orchestration import load_student_dataframe


def print_divider(title: str) -> None:
    print(f"\n=== {title} ===")


def print_result(result) -> None:
    print(f"Output: {result.output}")
    if result.artifact_path is not None:
        print(f"Artifact: {result.artifact_path}")
        print(f"Artifact exists: {result.artifact_exists}")
    if result.generated_code:
        print("Code:")
        print(result.generated_code)


def run_natural_language_data_visualization_lab() -> None:
    dataframe = load_student_dataframe()
    clear_generated_artifacts()
    print(LAB_INTRODUCTION)

    print_divider("Dataset")
    print(f"Rows: {dataframe.shape[0]}")
    print(f"Columns: {dataframe.shape[1]}")
    print(f"First columns: {dataframe.columns[:5].tolist()}")

    print_divider("Talk To Your Data")
    row_result = invoke_data_visualization_query(
        ROW_COUNT_QUERY,
        agent=build_data_visualization_agent(dataframe=dataframe),
    )
    print_result(row_result)
    age_result = invoke_data_visualization_query(
        AGE_FILTER_QUERY,
        agent=build_data_visualization_agent(dataframe=dataframe),
    )
    print_result(age_result)

    print_divider("Plot Your Data")
    for task in VISUALIZATION_QUERIES:
        artifact_path = build_artifact_path(task["slug"])
        result = invoke_data_visualization_query(
            task["query"],
            artifact_path=artifact_path,
            agent=build_data_visualization_agent(dataframe=dataframe),
        )
        print(f"Title: {task['title']}")
        print_result(result)

    print_divider("Exercises")
    for task in EXERCISE_QUERIES:
        artifact_path = build_artifact_path(task["slug"])
        result = invoke_data_visualization_query(
            task["query"],
            artifact_path=artifact_path,
            agent=build_data_visualization_agent(dataframe=dataframe),
        )
        print(f"Title: {task['title']}")
        print_result(result)
