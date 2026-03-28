# --- DEPENDENCIAS ---
from config.docchat_config import EXAMPLES
from config.docchat_config import LAB_INTRODUCTION
from orchestration.retriever_builder import RetrieverBuilder
from orchestration.workflow import AgentWorkflow
from pipeline.file_handler import DocumentProcessor


def print_divider(title: str) -> None:
    print(f"\n=== {title} ===")


class LocalFile:
    def __init__(self, name: str):
        self.name = name


def run_docchat_cli_demo() -> None:
    processor = DocumentProcessor()
    retriever_builder = RetrieverBuilder()
    workflow = AgentWorkflow()

    print(LAB_INTRODUCTION)
    for title, payload in EXAMPLES.items():
        print_divider(title)
        files = [LocalFile(path) for path in payload["file_paths"]]
        chunks = processor.process(files)
        retriever = retriever_builder.build_hybrid_retriever(chunks)
        result = workflow.full_pipeline(payload["question"], retriever)
        print(f"Question: {result.question}")
        print(f"Relevance: {result.relevance_label}")
        print(f"Answer: {result.final_answer}")
        print(f"Sources: {list(result.sources)}")
        print(result.verification_report)