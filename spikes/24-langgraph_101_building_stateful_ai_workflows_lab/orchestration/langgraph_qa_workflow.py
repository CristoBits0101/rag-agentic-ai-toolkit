# --- DEPENDENCIAS ---
from langgraph.graph import END
from langgraph.graph import StateGraph

from config.langgraph_workflows_config import LANGGRAPH_GUIDED_PROJECT_CONTEXT
from config.langgraph_workflows_config import QA_RELEVANT_KEYWORDS
from models.langgraph_workflows_entities import QAWorkflowResult
from models.langgraph_workflows_ollama_gateway import build_langgraph_ollama_chat_model
from models.langgraph_workflows_state import QAState


def input_validation_node(state: QAState) -> QAState:
    question = state.get("question", "").strip()

    if not question:
        return {
            "valid": False,
            "error": "Question cannot be empty.",
        }

    return {
        "question": question,
        "valid": True,
        "error": "",
    }


def validation_router(state: QAState) -> str:
    return "context" if state.get("valid", False) else "invalid"


def invalid_question_node(state: QAState) -> QAState:
    return {"answer": state.get("error", "Question cannot be empty.")}


def context_provider_node(state: QAState) -> QAState:
    question = state.get("question", "").lower()
    if any(keyword in question for keyword in QA_RELEVANT_KEYWORDS):
        return {"context": LANGGRAPH_GUIDED_PROJECT_CONTEXT}
    return {"context": None}


def build_qa_prompt(question: str, context: str) -> str:
    return (
        "You are answering a question about a guided project. "
        "Use only the provided context. "
        f"Context: {context}\n"
        f"Question: {question}\n"
        "Answer in a concise teaching style."
    )


def llm_qa_node(state: QAState, model) -> QAState:
    question = state.get("question", "")
    context = state.get("context")

    if not context:
        return {
            "answer": (
                "I don't have enough context to answer your question. "
                "Please ask about the guided project."
            )
        }

    prompt = build_qa_prompt(question=question, context=context)

    try:
        response = model.invoke(prompt)
    except Exception as exc:
        return {"answer": f"An error occurred while querying the model: {exc}"}

    content = getattr(response, "content", response)
    return {"answer": str(content).strip()}


def build_qa_workflow(model=None):
    workflow = StateGraph(QAState)
    qa_model = model or build_langgraph_ollama_chat_model()

    def qa_node(state: QAState) -> QAState:
        return llm_qa_node(state, model=qa_model)

    workflow.add_node("InputNode", input_validation_node)
    workflow.add_node("InvalidInputNode", invalid_question_node)
    workflow.add_node("ContextNode", context_provider_node)
    workflow.add_node("QANode", qa_node)

    workflow.add_conditional_edges(
        "InputNode",
        validation_router,
        {
            "invalid": "InvalidInputNode",
            "context": "ContextNode",
        },
    )
    workflow.add_edge("InvalidInputNode", END)
    workflow.add_edge("ContextNode", "QANode")
    workflow.add_edge("QANode", END)
    workflow.set_entry_point("InputNode")
    return workflow.compile()


def invoke_qa_workflow(question: str, model=None) -> QAWorkflowResult:
    app = build_qa_workflow(model=model)
    result = app.invoke({"question": question})
    return QAWorkflowResult(
        question=result.get("question", question),
        context=result.get("context"),
        answer=result.get("answer", ""),
        valid=result.get("valid", False),
        error=result.get("error") or None,
    )