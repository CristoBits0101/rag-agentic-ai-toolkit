# --- DEPENDENCIAS ---
import re
from typing import Any

from langchain_core.tools import BaseTool
from langchain_core.tools import tool

from data.tool_calling_fact_catalog import LOCAL_REFERENCE_FACTS

NUMBER_WORDS = {
    "zero": 0.0,
    "one": 1.0,
    "two": 2.0,
    "three": 3.0,
    "four": 4.0,
    "five": 5.0,
    "six": 6.0,
    "seven": 7.0,
    "eight": 8.0,
    "nine": 9.0,
    "ten": 10.0,
    "eleven": 11.0,
    "twelve": 12.0,
}


def normalize_whitespace(text: str) -> str:
    return " ".join(text.split())


def extract_numbers_from_text(text: str) -> list[float]:
    normalized = normalize_whitespace(text.lower())
    word_pattern = "|".join(NUMBER_WORDS)
    token_pattern = rf"(?<![A-Za-z])-?\d+(?:\.\d+)?|\b(?:{word_pattern})\b"
    extracted: list[float] = []

    for match in re.finditer(token_pattern, normalized):
        token = match.group(0)
        if token in NUMBER_WORDS:
            extracted.append(NUMBER_WORDS[token])
        else:
            extracted.append(float(token))

    return extracted


def coerce_tool_result(value: float) -> float | int:
    if float(value).is_integer():
        return int(value)

    return round(value, 6)


def build_result_payload(numbers: list[float], result: float | str) -> dict[str, Any]:
    return {
        "numbers": [coerce_tool_result(number) for number in numbers],
        "result": result,
    }


@tool
def add_numbers(inputs: str) -> dict[str, Any]:
    """
    Add all numeric values found in the input text.

    Args:
        inputs: Text that contains integers decimals or small number words.

    Returns:
        A payload with the extracted numbers and the final sum.
    """
    numbers = extract_numbers_from_text(inputs)
    if not numbers:
        return {"result": "No numbers found in input.", "numbers": []}

    return build_result_payload(numbers, coerce_tool_result(sum(numbers)))


@tool
def subtract_numbers(inputs: str) -> dict[str, Any]:
    """
    Subtract numeric values from left to right using the first number as the base value.

    Args:
        inputs: Text that contains integers decimals or small number words.

    Returns:
        A payload with the extracted numbers and the final subtraction result.
    """
    numbers = extract_numbers_from_text(inputs)
    if not numbers:
        return {"result": "No numbers found in input.", "numbers": []}

    result = numbers[0]
    for number in numbers[1:]:
        result -= number

    return build_result_payload(numbers, coerce_tool_result(result))


@tool
def multiply_numbers(inputs: str) -> dict[str, Any]:
    """
    Multiply all numeric values found in the input text.

    Args:
        inputs: Text that contains integers decimals or small number words.

    Returns:
        A payload with the extracted numbers and the final product.
    """
    numbers = extract_numbers_from_text(inputs)
    if not numbers:
        return {"result": "No numbers found in input.", "numbers": []}

    result = 1.0
    for number in numbers:
        result *= number

    return build_result_payload(numbers, coerce_tool_result(result))


@tool
def divide_numbers(inputs: str) -> dict[str, Any]:
    """
    Divide numeric values from left to right using the first number as the numerator.

    Args:
        inputs: Text that contains integers decimals or small number words.

    Returns:
        A payload with the extracted numbers and the final quotient.
    """
    numbers = extract_numbers_from_text(inputs)
    if not numbers:
        return {"result": "No numbers found in input.", "numbers": []}

    result = numbers[0]
    for number in numbers[1:]:
        if number == 0:
            return build_result_payload(numbers, "Division by zero is not allowed.")
        result /= number

    return build_result_payload(numbers, coerce_tool_result(result))


@tool
def calculate_power(inputs: str) -> dict[str, Any]:
    """
    Raise the first number in the text to the power of the second number.

    Args:
        inputs: Text that contains the base value and the exponent.

    Returns:
        A payload with the extracted numbers and the power result.
    """
    numbers = extract_numbers_from_text(inputs)
    if len(numbers) < 2:
        return {"result": "At least two numbers are required.", "numbers": numbers}

    result = numbers[0] ** numbers[1]
    return build_result_payload(numbers[:2], coerce_tool_result(result))


@tool
def search_local_reference_fact(query: str) -> dict[str, Any]:
    """
    Search a small local fact catalog for reference values used by the lab.

    Args:
        query: Topic to search in the local catalog.

    Returns:
        A payload with the matched topic and its numeric value.
    """
    normalized_query = normalize_whitespace(query.lower())

    for topic_key, payload in LOCAL_REFERENCE_FACTS.items():
        aliases = payload["aliases"]
        if any(alias in normalized_query for alias in aliases):
            return {
                "topic": topic_key,
                "result": coerce_tool_result(payload["value"]),
                "unit": payload["unit"],
                "source": payload["source"],
                "reference_date": payload["reference_date"],
            }

    return {
        "result": "Topic not found in local fact catalog.",
        "topic": "unknown",
        "source": "local_fact_catalog",
    }


def build_math_assistant_tools() -> list[BaseTool]:
    return [
        add_numbers,
        subtract_numbers,
        multiply_numbers,
        divide_numbers,
        calculate_power,
        search_local_reference_fact,
    ]


def describe_tool_schemas(tools: list[BaseTool] | None = None) -> list[dict[str, Any]]:
    selected_tools = tools or build_math_assistant_tools()
    return [
        {
            "name": tool.name,
            "description": tool.description,
            "args": tool.args,
        }
        for tool in selected_tools
    ]
