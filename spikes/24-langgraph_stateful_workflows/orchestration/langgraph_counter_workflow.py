# --- DEPENDENCIAS ---
import random
import string

from langgraph.graph import END
from langgraph.graph import StateGraph

from config.langgraph_workflows_config import COUNTER_INITIAL_STATE
from models.langgraph_workflows_entities import CounterWorkflowResult
from models.langgraph_workflows_state import ChainState


def add(state: ChainState, letter_picker=None) -> ChainState:
    pick_letter = letter_picker or (lambda: random.choice(string.ascii_lowercase))
    return {
        **state,
        "n": state["n"] + 1,
        "letter": pick_letter(),
    }


def print_out(state: ChainState) -> ChainState:
    print(f"Current n: {state['n']} Letter: {state['letter']}")
    return state


def stop_condition(state: ChainState) -> bool:
    return state["n"] >= 13


def build_counter_workflow(letter_picker=None, printer=print_out):
    workflow = StateGraph(ChainState)

    def add_node(state: ChainState) -> ChainState:
        return add(state, letter_picker=letter_picker)

    workflow.add_node("add", add_node)
    workflow.add_node("print", printer)
    workflow.add_edge("add", "print")
    workflow.add_conditional_edges(
        "print",
        stop_condition,
        {
            True: END,
            False: "add",
        },
    )
    workflow.set_entry_point("add")
    return workflow.compile()


def invoke_counter_workflow(initial_state: ChainState | None = None, letter_picker=None) -> CounterWorkflowResult:
    app = build_counter_workflow(letter_picker=letter_picker)
    result = app.invoke(initial_state or COUNTER_INITIAL_STATE)
    return CounterWorkflowResult(n=result["n"], letter=result["letter"])