# --- DEPENDENCIAS ---
from langgraph.graph import END
from langgraph.graph import StateGraph

from agents.relevance_checker import RelevanceChecker
from agents.research_agent import ResearchAgent
from agents.verification_agent import VerificationAgent
from config.docchat_config import MAX_CORRECTION_LOOPS
from models.docchat_entities import WorkflowResult
from models.docchat_ollama_gateway import build_docchat_chat_model
from models.docchat_state import AgentState


class AgentWorkflow:
    def __init__(self, model=None):
        llm = model or build_docchat_chat_model()
        self.relevance_checker = RelevanceChecker(model=llm)
        self.research_agent = ResearchAgent(model=llm)
        self.verification_agent = VerificationAgent(model=llm)
        self.workflow = self._build_workflow()

    def _build_workflow(self):
        workflow = StateGraph(AgentState)
        workflow.add_node("check_relevance", self._check_relevance_step)
        workflow.add_node("research", self._research_step)
        workflow.add_node("verify", self._verification_step)
        workflow.set_entry_point("check_relevance")
        workflow.add_conditional_edges(
            "check_relevance",
            self._decide_after_relevance_check,
            {
                "relevant": "research",
                "irrelevant": END,
            },
        )
        workflow.add_edge("research", "verify")
        workflow.add_conditional_edges(
            "verify",
            self._decide_next_step,
            {
                "re_research": "research",
                "end": END,
            },
        )
        return workflow.compile()

    def _check_relevance_step(self, state: AgentState) -> AgentState:
        label, docs = self.relevance_checker.check(state["question"], state["retriever"])
        sources = list(dict.fromkeys(doc.metadata.get("source", "unknown") for doc in docs))
        return {
            "relevance_label": label,
            "retrieved_docs": docs,
            "sources": sources,
        }

    def _research_step(self, state: AgentState) -> AgentState:
        docs = state.get("retrieved_docs") or state["retriever"].invoke(state["question"])
        research_result = self.research_agent.run(state["question"], docs)
        loop_count = state.get("loop_count", 0) + 1
        return {
            "retrieved_docs": docs,
            "draft_answer": research_result["draft_answer"],
            "context_used": research_result["context_used"],
            "loop_count": loop_count,
        }

    def _verification_step(self, state: AgentState) -> AgentState:
        verification = self.verification_agent.verify(
            state["question"],
            state.get("draft_answer", ""),
            state.get("retrieved_docs", []),
        )
        final_answer = state.get("draft_answer", "")
        if verification["verification"]["Supported"] != "YES":
            final_answer = "I could not fully verify the answer against the provided documents yet."
        return {
            "verification_report": verification["report"],
            "final_answer": final_answer,
        }

    def _decide_after_relevance_check(self, state: AgentState) -> str:
        return "relevant" if state.get("relevance_label") in {"CAN_ANSWER", "PARTIAL"} else "irrelevant"

    def _decide_next_step(self, state: AgentState) -> str:
        report = state.get("verification_report", "")
        supported = "**Supported:** YES" in report
        if supported or state.get("loop_count", 0) >= MAX_CORRECTION_LOOPS:
            return "end"
        return "re_research"

    def full_pipeline(self, question: str, retriever) -> WorkflowResult:
        result = self.workflow.invoke(
            {
                "question": question,
                "retriever": retriever,
                "loop_count": 0,
            }
        )
        final_answer = result.get("final_answer") or (
            "Your question is not sufficiently supported by the uploaded documents."
            if result.get("relevance_label") == "NO_MATCH"
            else result.get("draft_answer", "")
        )
        return WorkflowResult(
            question=question,
            relevance_label=result.get("relevance_label", "NO_MATCH"),
            draft_answer=result.get("draft_answer", ""),
            final_answer=final_answer,
            verification_report=result.get("verification_report", ""),
            context_used=result.get("context_used", ""),
            loop_count=result.get("loop_count", 0),
            sources=tuple(result.get("sources", [])),
        )