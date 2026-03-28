# --- DEPENDENCIAS ---
import json
from collections.abc import Sequence

from langchain_core.messages import AIMessage
from langchain_core.messages import BaseMessage
from langchain_core.messages import HumanMessage
from langchain_core.messages import ToolMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langgraph.graph import END
from langgraph.graph import MessageGraph
from pydantic import BaseModel
from pydantic import Field

from config.external_reflection_agent_config import MAX_ITERATIONS
from config.external_reflection_agent_config import RESPONDER_PROMPT_TEMPLATE
from config.external_reflection_agent_config import REVISOR_INSTRUCTIONS
from models.external_knowledge_gateway import ExternalKnowledgeResearchTool
from models.external_reflection_agent_entities import ExternalReflectionAgentResult
from models.external_reflection_ollama_gateway import build_external_reflection_ollama_chat_model


class Reflection(BaseModel):
    missing: str = Field(description="What information is missing")
    superfluous: str = Field(description="What information is unnecessary")


class AnswerQuestion(BaseModel):
    answer: str = Field(description="Main response to the question")
    reflection: Reflection = Field(description="Self critique of the answer")
    search_queries: list[str] = Field(description="Queries for additional research")


class ReviseAnswer(AnswerQuestion):
    references: list[str] = Field(description="Citations motivating the updated answer")


def build_prompt_template() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages(
        [
            ("system", RESPONDER_PROMPT_TEMPLATE),
            MessagesPlaceholder(variable_name="messages"),
            (
                "system",
                "Answer the user's question above using the required format. Be practical, evidence based, and medically cautious.",
            ),
        ]
    )


def build_responder_chain(model):
    prompt = build_prompt_template().partial(first_instruction="Provide a detailed answer under 250 words.")
    return prompt | model.bind_tools(tools=[AnswerQuestion])


def build_revisor_chain(model):
    prompt = build_prompt_template().partial(first_instruction=REVISOR_INSTRUCTIONS)
    return prompt | model.bind_tools(tools=[ReviseAnswer])


def ensure_ai_message(response) -> AIMessage:
    if isinstance(response, AIMessage):
        return response

    tool_calls = getattr(response, "tool_calls", None)
    content = getattr(response, "content", "")
    if tool_calls is not None:
        return AIMessage(content=str(content), tool_calls=tool_calls)

    raise TypeError("Structured chain output must be an AIMessage or expose tool_calls.")


def respond_node(state: Sequence[BaseMessage], responder_chain) -> list[BaseMessage]:
    response = responder_chain.invoke({"messages": list(state)})
    return [ensure_ai_message(response)]


def execute_tools(state: Sequence[BaseMessage], research_tool: ExternalKnowledgeResearchTool) -> list[BaseMessage]:
    last_ai_message = state[-1]
    if not getattr(last_ai_message, "tool_calls", None):
        return []

    tool_messages = []
    for tool_call in last_ai_message.tool_calls:
        if tool_call.get("name") not in {"AnswerQuestion", "ReviseAnswer"}:
            continue

        call_id = tool_call["id"]
        search_queries = tool_call.get("args", {}).get("search_queries", [])
        query_results = research_tool.search_many(search_queries)
        tool_messages.append(
            ToolMessage(
                content=json.dumps(query_results),
                tool_call_id=call_id,
            )
        )

    return tool_messages


def revise_node(state: Sequence[BaseMessage], revisor_chain) -> list[BaseMessage]:
    response = revisor_chain.invoke({"messages": list(state)})
    return [ensure_ai_message(response)]


def has_actionable_search_queries(message) -> bool:
    for tool_call in getattr(message, "tool_calls", []) or []:
        if tool_call.get("name") not in {"AnswerQuestion", "ReviseAnswer"}:
            continue
        search_queries = tool_call.get("args", {}).get("search_queries", [])
        if search_queries:
            return True
    return False


def event_loop(state: Sequence[BaseMessage], max_iterations: int = MAX_ITERATIONS):
    last_message = state[-1] if state else None
    if not isinstance(last_message, AIMessage):
        return END

    if not has_actionable_search_queries(last_message):
        return END

    tool_message_count = sum(isinstance(item, ToolMessage) for item in state)
    if tool_message_count >= max_iterations:
        return END
    return "execute_tools"


def build_external_reflection_graph(
    model=None,
    research_tool=None,
    responder_chain=None,
    revisor_chain=None,
    max_iterations: int = MAX_ITERATIONS,
):
    llm = model
    if responder_chain is None or revisor_chain is None:
        llm = llm or build_external_reflection_ollama_chat_model()

    active_responder_chain = responder_chain or build_responder_chain(llm)
    active_revisor_chain = revisor_chain or build_revisor_chain(llm)
    active_research_tool = research_tool or ExternalKnowledgeResearchTool()

    graph = MessageGraph()

    def respond(state: Sequence[BaseMessage]) -> list[BaseMessage]:
        return respond_node(state, responder_chain=active_responder_chain)

    def tool_node(state: Sequence[BaseMessage]) -> list[BaseMessage]:
        return execute_tools(state, research_tool=active_research_tool)

    def revise(state: Sequence[BaseMessage]) -> list[BaseMessage]:
        return revise_node(state, revisor_chain=active_revisor_chain)

    def router(state: Sequence[BaseMessage]):
        return event_loop(state, max_iterations=max_iterations)

    graph.add_node("respond", respond)
    graph.add_node("execute_tools", tool_node)
    graph.add_node("revisor", revise)
    graph.add_edge("respond", "execute_tools")
    graph.add_edge("execute_tools", "revisor")
    graph.add_conditional_edges(
        "revisor",
        router,
        {
            "execute_tools": "execute_tools",
            END: END,
        },
    )
    graph.set_entry_point("respond")
    return graph.compile()


def normalize_message_sequence(output) -> list[BaseMessage]:
    if isinstance(output, list):
        return list(output)

    if isinstance(output, dict) and "messages" in output:
        return list(output["messages"])

    raise TypeError("Unexpected external reflection workflow output format.")


def extract_structured_tool_args(messages: Sequence[BaseMessage]) -> tuple[dict, ...]:
    extracted = []
    for message in messages:
        for tool_call in getattr(message, "tool_calls", []) or []:
            args = tool_call.get("args", {})
            if "answer" in args:
                extracted.append(args)
    return tuple(extracted)


def extract_plain_ai_contents(messages: Sequence[BaseMessage]) -> tuple[str, ...]:
    contents = []
    for message in messages:
        if isinstance(message, AIMessage) and message.content:
            normalized_content = str(message.content).strip()
            if normalized_content:
                contents.append(normalized_content)
    return tuple(contents)


def get_workflow_mermaid(workflow) -> str:
    try:
        return workflow.get_graph().draw_mermaid()
    except Exception:
        return ""


def invoke_external_reflection_agent(
    question: str,
    workflow=None,
    model=None,
    research_tool=None,
    max_iterations: int = MAX_ITERATIONS,
) -> ExternalReflectionAgentResult:
    active_workflow = workflow or build_external_reflection_graph(
        model=model,
        research_tool=research_tool,
        max_iterations=max_iterations,
    )
    output = active_workflow.invoke([HumanMessage(content=question)])
    messages = normalize_message_sequence(output)
    structured_args = extract_structured_tool_args(messages)
    plain_ai_contents = extract_plain_ai_contents(messages)

    initial_answer = structured_args[0].get("answer", "") if structured_args else (
        plain_ai_contents[0] if plain_ai_contents else ""
    )
    revised_answers = tuple(item.get("answer", "") for item in structured_args[1:])
    final_answer = structured_args[-1].get("answer", "") if structured_args else (
        plain_ai_contents[-1] if plain_ai_contents else ""
    )
    reflections = tuple(item.get("reflection", {}) for item in structured_args)
    references = tuple(structured_args[-1].get("references", [])) if structured_args else tuple()
    search_queries = tuple(tuple(item.get("search_queries", [])) for item in structured_args)

    return ExternalReflectionAgentResult(
        question=question,
        initial_answer=initial_answer,
        revised_answers=revised_answers,
        final_answer=final_answer,
        reflections=reflections,
        references=references,
        search_queries=search_queries,
        total_messages=len(messages),
        mermaid_graph=get_workflow_mermaid(active_workflow),
    )