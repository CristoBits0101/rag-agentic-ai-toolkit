# --- DEPENDENCIAS ---
import sys
from pathlib import Path

from langchain_core.documents import Document

ROOT = Path(__file__).resolve().parents[2]
SPIKE = ROOT / "spikes" / "28-docchat_multi_agent_rag_system"

if str(SPIKE) not in sys.path:
    sys.path.insert(0, str(SPIKE))

from agents.relevance_checker import RelevanceChecker
from agents.research_agent import ResearchAgent
from agents.verification_agent import VerificationAgent
from models.docchat_embedding_gateway import build_docchat_embeddings
from orchestration.workflow import AgentWorkflow
from pipeline.file_handler import DocumentProcessor


class TempFileWrapper:
    def __init__(self, name: str):
        self.name = name


class FakeRetriever:
    def __init__(self, docs):
        self.docs = docs

    def invoke(self, question):
        return self.docs


class FakeResponse:
    def __init__(self, content: str):
        self.content = content


class FakeModel:
    def __init__(self, outputs: list[str]):
        self.outputs = outputs

    def invoke(self, prompt):
        return FakeResponse(self.outputs.pop(0))


def test_document_processor_processes_markdown_file(tmp_path):
    file_path = tmp_path / "report.md"
    file_path.write_text("# Report\n\nThe Singapore facility PUE is 1.10.", encoding="utf-8")
    processor = DocumentProcessor()

    chunks = processor.process([TempFileWrapper(str(file_path))])

    assert chunks
    assert any("1.10" in chunk.page_content for chunk in chunks)


def test_local_hash_embeddings_return_fixed_dimension():
    embeddings = build_docchat_embeddings()
    vector = embeddings.embed_query("hello world")

    assert len(vector) == 128


def test_relevance_checker_detects_answerable_question():
    docs = [Document(page_content="The Singapore facility PUE is 1.10.")]
    checker = RelevanceChecker()

    label, top_docs = checker.check("What is the Singapore facility PUE?", FakeRetriever(docs))

    assert label in {"CAN_ANSWER", "PARTIAL"}
    assert top_docs


def test_research_agent_builds_answer_from_context():
    docs = [Document(page_content="Asia Pacific reached 64 percent carbon free energy.")]
    agent = ResearchAgent(model=FakeModel(["Asia Pacific reached 64 percent carbon free energy."]))

    result = agent.run("What is Asia Pacific CFE?", docs)

    assert "64 percent" in result["draft_answer"]


def test_verification_agent_flags_unsupported_claims():
    docs = [Document(page_content="The report states the value is 1.10.")]
    agent = VerificationAgent()

    result = agent.verify("What is the value?", "The value is 1.20.", docs)

    assert result["verification"]["Supported"] == "NO"


def test_agent_workflow_returns_answer_for_relevant_question():
    docs = [Document(page_content="DeepSeek R1 scored 79.8 pass@1 on AIME 2024.", metadata={"source": "deepseek.md"})]
    workflow = AgentWorkflow(model=FakeModel(["DeepSeek R1 scored 79.8 pass@1 on AIME 2024."]))

    result = workflow.full_pipeline("What score is mentioned for DeepSeek R1?", FakeRetriever(docs))

    assert "79.8" in result.final_answer or "79.8" in result.draft_answer
    assert result.sources == ("deepseek.md",)