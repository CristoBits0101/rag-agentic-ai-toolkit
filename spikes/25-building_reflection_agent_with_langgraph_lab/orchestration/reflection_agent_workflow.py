# --- DEPENDENCIAS ---
from collections.abc import Sequence

from langchain_core.messages import AIMessage
from langchain_core.messages import BaseMessage
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langgraph.graph import END
from langgraph.graph import MessageGraph

from config.reflection_agent_config import GENERATION_SYSTEM_PROMPT
from config.reflection_agent_config import MAX_REFLECTION_MESSAGES
from config.reflection_agent_config import REFLECTION_SYSTEM_PROMPT
from models.reflection_agent_entities import ReflectionAgentRunResult
from models.reflection_agent_ollama_gateway import build_reflection_agent_ollama_chat_model


def build_generation_prompt() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages(
        [
            ("system", GENERATION_SYSTEM_PROMPT),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )


def build_reflection_prompt() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages(
        [
            ("system", REFLECTION_SYSTEM_PROMPT),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )


def build_generation_chain(model):
    return build_generation_prompt() | model


def build_reflection_chain(model):
    return build_reflection_prompt() | model


def generation_node(state: Sequence[BaseMessage], generate_chain) -> list[BaseMessage]:
    generated_post = generate_chain.invoke({"messages": state})
    content = getattr(generated_post, "content", generated_post)
    return [AIMessage(content=str(content).strip())]


def reflection_node(messages: Sequence[BaseMessage], reflect_chain) -> list[BaseMessage]:
    critique = reflect_chain.invoke({"messages": messages})
    content = getattr(critique, "content", critique)
    return [HumanMessage(content=str(content).strip())]


def should_continue(state: Sequence[BaseMessage], max_messages: int = MAX_REFLECTION_MESSAGES):
    if len(state) >= max_messages:
        return END
    return "reflect"


def build_reflection_agent_workflow(
    model=None,
    max_messages: int = MAX_REFLECTION_MESSAGES,
    generate_chain=None,
    reflect_chain=None,
):
    llm = model
    if generate_chain is None or reflect_chain is None:
        llm = llm or build_reflection_agent_ollama_chat_model()

    active_generate_chain = generate_chain or build_generation_chain(llm)
    active_reflect_chain = reflect_chain or build_reflection_chain(llm)

    graph = MessageGraph()

    def generate(state: Sequence[BaseMessage]) -> list[BaseMessage]:
        return generation_node(state, generate_chain=active_generate_chain)

    def reflect(state: Sequence[BaseMessage]) -> list[BaseMessage]:
        return reflection_node(state, reflect_chain=active_reflect_chain)

    def router(state: Sequence[BaseMessage]):
        return should_continue(state, max_messages=max_messages)

    graph.add_node("generate", generate)
    graph.add_node("reflect", reflect)
    graph.add_edge("reflect", "generate")
    graph.add_conditional_edges(
        "generate",
        router,
        {
            "reflect": "reflect",
            END: END,
        },
    )
    graph.set_entry_point("generate")
    return graph.compile()


def normalize_message_sequence(output) -> list[BaseMessage]:
    if isinstance(output, list):
        return list(output)

    if isinstance(output, dict) and "messages" in output:
        return list(output["messages"])

    raise TypeError("Unexpected reflection workflow output format.")


def extract_generated_posts(messages: Sequence[BaseMessage]) -> tuple[str, ...]:
    return tuple(message.content for message in messages if isinstance(message, AIMessage))


def extract_critiques(messages: Sequence[BaseMessage]) -> tuple[str, ...]:
    human_messages = [message.content for message in messages if isinstance(message, HumanMessage)]
    return tuple(human_messages[1:])


def get_workflow_mermaid(workflow) -> str:
    try:
        return workflow.get_graph().draw_mermaid()
    except Exception:
        return ""


def invoke_reflection_agent(
    request: str,
    workflow=None,
    model=None,
    max_messages: int = MAX_REFLECTION_MESSAGES,
) -> ReflectionAgentRunResult:
    active_workflow = workflow or build_reflection_agent_workflow(
        model=model,
        max_messages=max_messages,
    )
    output = active_workflow.invoke([HumanMessage(content=request)])
    messages = normalize_message_sequence(output)
    generated_posts = extract_generated_posts(messages)
    critiques = extract_critiques(messages)
    final_post = generated_posts[-1] if generated_posts else ""
    return ReflectionAgentRunResult(
        request=request,
        generated_posts=generated_posts,
        critiques=critiques,
        final_post=final_post,
        total_messages=len(messages),
        mermaid_graph=get_workflow_mermaid(active_workflow),
    )