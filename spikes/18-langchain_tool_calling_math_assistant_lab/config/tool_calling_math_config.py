# --- DEPENDENCIAS ---

DEMO_INTRODUCTION = (
    "Practica 18 adapta el lab de tool calling de LangChain con un modelo demo "
    "determinista y un catalogo factual local."
)

DEFAULT_TOOL_CALLING_QUERIES = [
    "Add 25 and 15.",
    "Add 25 and 15 then multiply by 2.",
    "Subtract 100, 20 and 10.",
    "Divide 100 by 5 and then by 2.",
    "Raise 3 to the power of 4.",
    "What is the population of Canada. Multiply it by 0.75.",
]

MAX_TOOL_CALLING_STEPS = 4
