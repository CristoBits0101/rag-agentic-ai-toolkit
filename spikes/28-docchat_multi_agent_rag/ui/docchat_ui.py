# --- DEPENDENCIAS ---
import hashlib

import gradio as gr

from config.docchat_config import EXAMPLES
from models.docchat_entities import ExampleSelectionResult
from orchestration.retriever_builder import RetrieverBuilder
from orchestration.workflow import AgentWorkflow
from pipeline.file_handler import DocumentProcessor

processor = DocumentProcessor()
retriever_builder = RetrieverBuilder()
workflow = AgentWorkflow()


def _get_file_hashes(uploaded_files: list) -> frozenset:
    hashes = set()
    for file in uploaded_files:
        with open(file.name, "rb") as handle:
            hashes.add(hashlib.sha256(handle.read()).hexdigest())
    return frozenset(hashes)


def load_example(example_name: str):
    payload = EXAMPLES[example_name]
    return ExampleSelectionResult(
        question=payload["question"],
        file_paths=tuple(payload["file_paths"]),
    )


def handle_submit(uploaded_files, question_text, state):
    if not uploaded_files:
        return "Please upload at least one document.", "", state
    if not question_text.strip():
        return "Please enter a question.", "", state

    current_hashes = _get_file_hashes(uploaded_files)
    if state["retriever"] is None or current_hashes != state["file_hashes"]:
        chunks = processor.process(uploaded_files)
        retriever = retriever_builder.build_hybrid_retriever(chunks)
        state.update({
            "file_hashes": current_hashes,
            "retriever": retriever,
        })

    result = workflow.full_pipeline(question_text, state["retriever"])
    return result.final_answer, result.verification_report, state


def build_demo():
    css = """
    .subtitle { font-size: 1.25rem; }
    .text { color: #444; }
    """
    with gr.Blocks(title="DocChat", css=css) as demo:
        session_state = gr.State({"file_hashes": frozenset(), "retriever": None})
        gr.Markdown("## DocChat: multi-agent RAG with verification", elem_classes="subtitle")
        gr.Markdown("Upload document(s), ask a question, and inspect the verification report.", elem_classes="text")

        with gr.Row():
            file_input = gr.Files(label="Upload documents", file_count="multiple")
            example_selector = gr.Dropdown(choices=list(EXAMPLES), label="Load example question")

        question_input = gr.Textbox(label="Question")
        submit_button = gr.Button("Submit")
        answer_output = gr.Textbox(label="Answer", interactive=False, lines=8)
        verification_output = gr.Textbox(label="Verification report", interactive=False, lines=8)

        def apply_example(example_name: str):
            if not example_name:
                return ""
            selected = load_example(example_name)
            return selected.question

        example_selector.change(
            fn=apply_example,
            inputs=example_selector,
            outputs=question_input,
        )

        submit_button.click(
            fn=handle_submit,
            inputs=[file_input, question_input, session_state],
            outputs=[answer_output, verification_output, session_state],
        )

    return demo