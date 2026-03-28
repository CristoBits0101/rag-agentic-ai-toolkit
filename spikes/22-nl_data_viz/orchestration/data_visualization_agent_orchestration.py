# --- DEPENDENCIAS ---
import os
from pathlib import Path
import time
import warnings

os.environ.setdefault("MPLBACKEND", "Agg")
warnings.filterwarnings("ignore")

from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent

from config.data_visualization_agent_config import DATASET_DESCRIPTION
from models.data_visualization_entities import VisualizationAgentResult
from models.data_visualization_ollama_gateway import build_data_visualization_ollama_chat_model
from orchestration.data_visualization_dataset_orchestration import load_student_dataframe


def build_data_visualization_agent(model=None, dataframe=None):
    selected_model = model or build_data_visualization_ollama_chat_model()
    selected_dataframe = dataframe if dataframe is not None else load_student_dataframe()
    return create_pandas_dataframe_agent(
        selected_model,
        selected_dataframe,
        agent_type="zero-shot-react-description",
        verbose=False,
        return_intermediate_steps=True,
        allow_dangerous_code=True,
        prefix=DATASET_DESCRIPTION,
    )


def build_query_with_artifact_path(query: str, artifact_path: Path | None = None) -> str:
    if artifact_path is None:
        return query

    return (
        f"{query} Save the chart to r'{artifact_path}' and do not call plt.show(). "
        "Return a short confirmation with the saved path."
    )


def extract_generated_code(response: dict) -> str:
    intermediate_steps = response.get("intermediate_steps", [])
    if not intermediate_steps:
        return ""

    last_step = intermediate_steps[-1][0]
    return str(getattr(last_step, "tool_input", ""))


def artifact_exists_with_retry(artifact_path: Path | None) -> bool:
    if artifact_path is None:
        return False

    for _ in range(5):
        if artifact_path.exists():
            return True
        time.sleep(0.2)

    return artifact_path.exists()


def invoke_data_visualization_query(
    query: str,
    artifact_path: Path | None = None,
    agent=None,
) -> VisualizationAgentResult:
    selected_agent = agent or build_data_visualization_agent()
    final_query = build_query_with_artifact_path(query, artifact_path)
    response = selected_agent.invoke(final_query)
    generated_code = extract_generated_code(response)
    resolved_artifact_path = artifact_path if artifact_path is None else Path(artifact_path)
    artifact_exists = artifact_exists_with_retry(resolved_artifact_path)
    return VisualizationAgentResult(
        query=final_query,
        output=str(response.get("output", "")),
        generated_code=generated_code,
        artifact_path=resolved_artifact_path,
        artifact_exists=artifact_exists,
    )
