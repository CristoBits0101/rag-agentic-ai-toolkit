# --- DEPENDENCIAS ---
from langgraph.graph import END
from langgraph.graph import START
from langgraph.graph import StateGraph

from models.workflow_patterns_state import TranslationState


def translate_french(state: TranslationState, model) -> dict:
    response = model.invoke(f"Translate the following text to French.\n\n{state['text']}")
    return {"french": str(getattr(response, 'content', response)).strip()}


def translate_spanish(state: TranslationState, model) -> dict:
    response = model.invoke(f"Translate the following text to Spanish.\n\n{state['text']}")
    return {"spanish": str(getattr(response, 'content', response)).strip()}


def translate_japanese(state: TranslationState, model) -> dict:
    response = model.invoke(f"Translate the following text to Japanese.\n\n{state['text']}")
    return {"japanese": str(getattr(response, 'content', response)).strip()}


def aggregator(state: TranslationState) -> dict:
    combined = f"Original Text: {state['text']}\n\n"
    combined += f"French: {state.get('french', '')}\n\n"
    combined += f"Spanish: {state.get('spanish', '')}\n\n"
    combined += f"Japanese: {state.get('japanese', '')}\n"
    return {"combined_output": combined}


def build_parallel_translation_workflow(model):
    graph = StateGraph(TranslationState)
    graph.add_node("translate_french", lambda state: translate_french(state, model))
    graph.add_node("translate_spanish", lambda state: translate_spanish(state, model))
    graph.add_node("translate_japanese", lambda state: translate_japanese(state, model))
    graph.add_node("aggregator", aggregator)
    graph.add_edge(START, "translate_french")
    graph.add_edge(START, "translate_spanish")
    graph.add_edge(START, "translate_japanese")
    graph.add_edge("translate_french", "aggregator")
    graph.add_edge("translate_spanish", "aggregator")
    graph.add_edge("translate_japanese", "aggregator")
    graph.add_edge("aggregator", END)
    return graph.compile()


def invoke_parallel_translation(text: str, model) -> TranslationState:
    app = build_parallel_translation_workflow(model)
    return app.invoke({"text": text, "french": "", "spanish": "", "japanese": "", "combined_output": ""})