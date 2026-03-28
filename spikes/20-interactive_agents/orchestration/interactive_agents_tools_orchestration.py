# --- DEPENDENCIAS ---
from typing import Any

from langchain_core.tools import BaseTool
from langchain_core.tools import tool


@tool
def add(a: int, b: int) -> int:
    """
    Add a and b.

    Args:
        a: First integer to add.
        b: Second integer to add.

    Returns:
        The sum of both integers.
    """
    return a + b


@tool
def subtract(a: int, b: int) -> int:
    """
    Subtract b from a.

    Args:
        a: Base integer.
        b: Integer to subtract.

    Returns:
        The subtraction result.
    """
    return a - b


@tool
def multiply(a: int, b: int) -> int:
    """
    Multiply a and b.

    Args:
        a: First integer to multiply.
        b: Second integer to multiply.

    Returns:
        The multiplication result.
    """
    return a * b


@tool
def calculate_tip(total_bill: float, tip_percent: float) -> dict[str, float]:
    """
    Calculate the tip amount for a bill.

    Args:
        total_bill: Total bill before tip.
        tip_percent: Tip percentage to apply.

    Returns:
        A payload with the tip amount and total with tip.
    """
    tip_amount = round(total_bill * tip_percent / 100, 2)
    total_with_tip = round(total_bill + tip_amount, 2)
    return {
        "total_bill": round(total_bill, 2),
        "tip_percent": round(tip_percent, 2),
        "tip_amount": tip_amount,
        "total_with_tip": total_with_tip,
    }


def build_interactive_math_tools() -> list[BaseTool]:
    return [add, subtract, multiply]


def build_tip_tools() -> list[BaseTool]:
    return [calculate_tip]


def build_interactive_tools() -> list[BaseTool]:
    return [*build_interactive_math_tools(), *build_tip_tools()]


def build_tool_map(tools: list[BaseTool] | None = None) -> dict[str, BaseTool]:
    selected_tools = tools or build_interactive_tools()
    return {tool.name: tool for tool in selected_tools}


def normalize_tool_result(raw_result: Any) -> dict[str, Any]:
    if isinstance(raw_result, dict):
        return raw_result

    return {"result": raw_result}


def describe_tool_schemas(tools: list[BaseTool] | None = None) -> list[dict[str, Any]]:
    selected_tools = tools or build_interactive_tools()
    return [
        {
            "name": tool.name,
            "description": tool.description,
            "args": tool.args,
        }
        for tool in selected_tools
    ]
