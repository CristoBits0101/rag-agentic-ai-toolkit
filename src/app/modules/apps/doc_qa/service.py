from app.modules.apps.doc_qa.schemas import ChatRequest, ChatResponse


def run_doc_qa(payload: ChatRequest) -> ChatResponse:
    return ChatResponse(answer=f"doc_qa placeholder: {payload.message}")
