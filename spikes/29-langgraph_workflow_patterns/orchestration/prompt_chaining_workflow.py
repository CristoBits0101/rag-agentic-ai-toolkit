# --- DEPENDENCIAS ---
from langgraph.graph import StateGraph

from models.workflow_patterns_state import ChainState


def generate_resume_summary(state: ChainState, model) -> ChainState:
    prompt = (
        "You are a resume assistant. Read the job description and write a concise resume summary "
        "for an ideal applicant. Focus on capabilities achievements and business impact.\n\n"
        f"Job Description:\n{state['job_description']}"
    )
    response = model.invoke(prompt)
    content = getattr(response, "content", response)
    return {**state, "resume_summary": str(content).strip()}


def generate_cover_letter(state: ChainState, model) -> ChainState:
    prompt = (
        "You are a cover letter writing assistant. Use the resume summary and job description "
        "to write a professional personalized cover letter.\n\n"
        f"Resume Summary:\n{state['resume_summary']}\n\n"
        f"Job Description:\n{state['job_description']}"
    )
    response = model.invoke(prompt)
    content = getattr(response, "content", response)
    return {**state, "cover_letter": str(content).strip()}


def build_prompt_chaining_workflow(model):
    workflow = StateGraph(ChainState)
    workflow.add_node("generate_resume_summary", lambda state: generate_resume_summary(state, model))
    workflow.add_node("generate_cover_letter", lambda state: generate_cover_letter(state, model))
    workflow.set_entry_point("generate_resume_summary")
    workflow.add_edge("generate_resume_summary", "generate_cover_letter")
    workflow.set_finish_point("generate_cover_letter")
    return workflow.compile()


def invoke_job_application_workflow(job_description: str, model) -> ChainState:
    app = build_prompt_chaining_workflow(model)
    return app.invoke({"job_description": job_description, "resume_summary": "", "cover_letter": ""})