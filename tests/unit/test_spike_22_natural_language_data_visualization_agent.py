# --- DEPENDENCIAS ---
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPIKE = ROOT / "spikes" / "22-natural_language_data_visualization_agent_lab"

if str(SPIKE) not in sys.path:
    sys.path.insert(0, str(SPIKE))

from models.data_visualization_ollama_gateway import select_best_available_ollama_model
from orchestration.data_visualization_agent_orchestration import build_data_visualization_agent
from orchestration.data_visualization_agent_orchestration import build_query_with_artifact_path
from orchestration.data_visualization_agent_orchestration import extract_generated_code
from orchestration.data_visualization_agent_orchestration import invoke_data_visualization_query
from orchestration.data_visualization_dataset_orchestration import build_artifact_path
from orchestration.data_visualization_dataset_orchestration import load_student_dataframe


class FakeAgentAction:
    def __init__(self, tool_input: str):
        self.tool_input = tool_input


class FakeAgentExecutor:
    def __init__(self, response: dict):
        self._response = response
        self.queries: list[str] = []

    def invoke(self, query: str) -> dict:
        self.queries.append(query)
        return self._response


def test_load_student_dataframe_returns_expected_shape():
    dataframe = load_student_dataframe()

    assert dataframe.shape == (395, 33)
    assert "sex" in dataframe.columns
    assert "G3" in dataframe.columns


def test_build_artifact_path_sanitizes_slug():
    artifact_path = build_artifact_path("internet access vs grades")

    assert artifact_path.name == "internet_access_vs_grades.png"


def test_build_query_with_artifact_path_adds_save_instruction(tmp_path):
    artifact_path = tmp_path / "gender_count.png"

    final_query = build_query_with_artifact_path(
        "Generate a bar chart to plot the gender count.",
        artifact_path,
    )

    assert "Save the chart to" in final_query
    assert str(artifact_path) in final_query
    assert "do not call plt.show()" in final_query


def test_extract_generated_code_reads_last_tool_input():
    response = {
        "output": "Done.",
        "intermediate_steps": [
            (FakeAgentAction("len(df)"), 395),
            (FakeAgentAction("df['sex'].value_counts()"), "M 208 F 187"),
        ],
    }

    assert extract_generated_code(response) == "df['sex'].value_counts()"


def test_invoke_data_visualization_query_returns_output_code_and_artifact(tmp_path):
    artifact_path = tmp_path / "gender_count.png"
    artifact_path.write_text("fake image")
    fake_agent = FakeAgentExecutor(
        {
            "output": "The chart has been saved.",
            "intermediate_steps": [
                (
                    FakeAgentAction("plt.savefig(r'gender_count.png')"),
                    "",
                )
            ],
        }
    )

    result = invoke_data_visualization_query(
        "Generate a bar chart to plot the gender count.",
        artifact_path=artifact_path,
        agent=fake_agent,
    )

    assert "Save the chart to" in fake_agent.queries[0]
    assert result.output == "The chart has been saved."
    assert result.generated_code == "plt.savefig(r'gender_count.png')"
    assert result.artifact_path == artifact_path
    assert result.artifact_exists is True


def test_build_data_visualization_agent_uses_expected_factory_arguments(monkeypatch):
    captured = {}

    def fake_factory(llm, df, **kwargs):
        captured["llm"] = llm
        captured["df_shape"] = df.shape
        captured["kwargs"] = kwargs
        return "fake-agent"

    monkeypatch.setattr(
        "orchestration.data_visualization_agent_orchestration.create_pandas_dataframe_agent",
        fake_factory,
    )

    agent = build_data_visualization_agent(
        model="fake-model",
        dataframe=load_student_dataframe(),
    )

    assert agent == "fake-agent"
    assert captured["llm"] == "fake-model"
    assert captured["df_shape"] == (395, 33)
    assert captured["kwargs"]["agent_type"] == "zero-shot-react-description"
    assert captured["kwargs"]["return_intermediate_steps"] is True
    assert captured["kwargs"]["allow_dangerous_code"] is True


def test_select_best_available_ollama_model_prefers_ranked_candidate():
    selected_model = select_best_available_ollama_model(
        ["llama3.2:3b", "qwen2.5:7b", "mistral"],
    )

    assert selected_model == "qwen2.5:7b"
