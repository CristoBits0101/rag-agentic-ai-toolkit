# --- DEPENDENCIAS ---
from collections import OrderedDict

from config.daily_dish_chatbot_config import CALCULATOR_PROMPTS
from config.daily_dish_chatbot_config import DEFAULT_CUSTOMER_QUERY
from config.daily_dish_chatbot_config import SUPPLEMENTARY_QUERY
from models.crewai_compat import Agent
from models.crewai_compat import Crew
from models.crewai_compat import Process
from models.crewai_compat import Task
from models.daily_dish_entities import CalculatorDemoResult
from models.daily_dish_entities import ToolingComparisonSummary
from models.daily_dish_llm_gateway import build_daily_dish_model
from models.daily_dish_tools import LocalFaqSearchTool
from models.daily_dish_tools import LocalWebSearchTool
from models.daily_dish_tools import add_numbers
from models.daily_dish_tools import multiply_numbers


def _invoke_model(agent: Agent, prompt: str) -> str:
    response = agent.llm.invoke(prompt)
    return str(getattr(response, "content", response)).strip()


def _find_tool(agent: Agent, name_fragment: str):
    for tool in agent.tools:
        tool_name = getattr(tool, "name", "")
        if name_fragment in tool_name:
            return tool
    raise ValueError(f"Tool with fragment {name_fragment} was not found.")


def _should_search_web(query: str, faq_result: dict) -> bool:
    lowered = query.lower()
    if any(keyword in lowered for keyword in ["parking", "nearby", "map", "directions", "station", "online"]):
        return True
    return faq_result.get("score", 0) <= 1


def _format_source_line(result: dict) -> str:
    label = result.get("question") or result.get("title") or result.get("tool")
    return f"- {label}: {result.get('answer', 'No result')}"


def _extract_tool_names(task_outputs) -> list[str]:
    ordered = OrderedDict()
    for output in task_outputs:
        for line in output.raw.splitlines():
            if not line.startswith("Tools used:"):
                continue
            payload = line.split(":", 1)[1].strip()
            if payload.lower() == "none":
                continue
            for tool_name in [item.strip() for item in payload.split(",") if item.strip()]:
                ordered[tool_name] = True
    return list(ordered.keys())


def execute_agent_centric_inquiry(agent: Agent, description: str, context_text: str, inputs: dict) -> str:
    query = inputs["customer_query"]
    faq_result = _find_tool(agent, "faq").run(query)
    web_result = _find_tool(agent, "web").run(query)
    selected_lines = [_format_source_line(faq_result)]
    if _should_search_web(query, faq_result) or web_result.get("score", 0) > faq_result.get("score", 0):
        selected_lines.append(_format_source_line(web_result))
    evidence_text = "\n".join(selected_lines)

    prompt = (
        f"Role: {agent.role}. Goal: {agent.goal}.\n\n"
        f"Customer query: {query}\n"
        "Use the gathered evidence to answer in a warm customer service tone.\n"
        f"Evidence:\n{evidence_text}"
    )
    answer = _invoke_model(agent, prompt)
    return f"Tools used: faq_search_tool, web_search_tool\n{answer}"


def execute_faq_search(agent: Agent, description: str, context_text: str, inputs: dict) -> str:
    query = inputs["customer_query"]
    faq_result = _find_tool(agent, "faq").run(query)
    return (
        "Tools used: faq_search_tool\n"
        f"FAQ answer: {faq_result['answer']}\n"
        f"FAQ score: {faq_result['score']}"
    )


def execute_web_search(agent: Agent, description: str, context_text: str, inputs: dict) -> str:
    query = inputs["customer_query"]
    faq_result = _find_tool(Agent(role="temp", goal="", backstory="", tools=[LocalFaqSearchTool()]), "faq").run(query)
    if not _should_search_web(query, faq_result):
        return "Tools used: none\nWeb search skipped because the FAQ answer is already sufficient."

    web_result = _find_tool(agent, "web").run(query)
    return f"Tools used: web_search_tool\nWeb answer: {web_result['answer']}"


def execute_response_drafting(agent: Agent, description: str, context_text: str, inputs: dict) -> str:
    prompt = (
        f"Role: {agent.role}. Goal: {agent.goal}.\n\n"
        f"Customer query: {inputs['customer_query']}\n"
        "Draft the final response using the step outputs below.\n"
        f"Context:\n{context_text}"
    )
    answer = _invoke_model(agent, prompt)
    return f"Tools used: none\n{answer}"


def execute_calculation(agent: Agent, description: str, context_text: str, inputs: dict) -> str:
    instruction = inputs["numbers"]
    lowered = instruction.lower()
    chosen_tool = multiply_numbers if "multiply" in lowered or "product" in lowered else add_numbers
    result = chosen_tool.run(instruction)
    return f"Tools used: {chosen_tool.name}\nResult: {result}"


def build_agent_centric_crew(model=None):
    llm = model or build_daily_dish_model()
    specialist = Agent(
        role="The Daily Dish Inquiry Specialist",
        goal="Answer customer questions and decide which information source to consult.",
        backstory="A restaurant support assistant who can inspect the FAQ and supplemental local web snippets.",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=[LocalFaqSearchTool(), LocalWebSearchTool()],
    )
    inquiry_task = Task(
        description="Answer the customer query {customer_query} using the tools available to the agent.",
        expected_output="A polished answer to the customer query.",
        agent=specialist,
        executor=execute_agent_centric_inquiry,
    )
    return Crew(agents=[specialist], tasks=[inquiry_task], process=Process.sequential, verbose=True)


def build_task_centric_crew(model=None):
    llm = model or build_daily_dish_model()
    specialist = Agent(
        role="Customer Service Specialist",
        goal="Follow a deterministic multi step workflow and use only the tools attached to each task.",
        backstory="A disciplined support agent that executes search and response tasks one at a time.",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=[],
    )
    faq_task = Task(
        description="Search the Daily Dish FAQ for the query {customer_query}.",
        expected_output="The best FAQ match or a not found notice.",
        agent=specialist,
        executor=execute_faq_search,
        tools=[LocalFaqSearchTool()],
    )
    web_task = Task(
        description="Search for supplemental information if the FAQ is not sufficient for {customer_query}.",
        expected_output="Supplemental parking transit or website information when needed.",
        agent=specialist,
        executor=execute_web_search,
        context=[faq_task],
        tools=[LocalWebSearchTool()],
    )
    drafting_task = Task(
        description="Draft the final customer response for {customer_query} using the gathered evidence.",
        expected_output="A friendly final answer.",
        agent=specialist,
        executor=execute_response_drafting,
        context=[faq_task, web_task],
        tools=[],
    )
    return Crew(
        agents=[specialist],
        tasks=[faq_task, web_task, drafting_task],
        process=Process.sequential,
        verbose=True,
    )


def build_calculator_crew(model=None):
    llm = model or build_daily_dish_model()
    calculator = Agent(
        role="Calculator",
        goal="Use custom arithmetic tools to answer natural language math requests.",
        backstory="An operations assistant that can parse integer instructions and apply the correct arithmetic tool.",
        llm=llm,
        tools=[add_numbers, multiply_numbers],
        allow_delegation=False,
    )
    task = Task(
        description="Compute the result for {numbers}.",
        expected_output="A numeric result.",
        agent=calculator,
        executor=execute_calculation,
    )
    return Crew(agents=[calculator], tasks=[task], process=Process.sequential, verbose=False)


def compare_tool_assignment(query: str = DEFAULT_CUSTOMER_QUERY, model=None) -> ToolingComparisonSummary:
    agent_centric = build_agent_centric_crew(model=model)
    agent_centric_result = agent_centric.kickoff(inputs={"customer_query": query})
    task_centric = build_task_centric_crew(model=model)
    task_centric_result = task_centric.kickoff(inputs={"customer_query": query})
    agent_tools = _extract_tool_names(agent_centric_result.tasks_output)
    task_tools = _extract_tool_names(task_centric_result.tasks_output)
    key_difference = (
        "The agent centric flow inspects every available tool before answering while the task centric flow exposes only the tool required at each step."
    )
    return ToolingComparisonSummary(
        query=query,
        agent_centric_answer=agent_centric_result.raw,
        task_centric_answer=task_centric_result.raw,
        agent_centric_tools=agent_tools,
        task_centric_tools=task_tools,
        key_difference=key_difference,
    )


def run_custom_tools_demo(model=None) -> CalculatorDemoResult:
    crew = build_calculator_crew(model=model)
    addition_result = crew.kickoff(inputs={"numbers": CALCULATOR_PROMPTS["addition"]})
    multiplication_result = crew.kickoff(inputs={"numbers": CALCULATOR_PROMPTS["multiplication"]})
    return CalculatorDemoResult(
        addition_result=int(addition_result.raw.split("Result:", 1)[1].strip()),
        multiplication_result=int(multiplication_result.raw.split("Result:", 1)[1].strip()),
    )


def run_daily_dish_demo() -> None:
    summary = compare_tool_assignment(DEFAULT_CUSTOMER_QUERY)
    print("=== Agent Centric Comparison ===")
    print(summary.agent_centric_answer)
    print("\n=== Task Centric Comparison ===")
    print(summary.task_centric_answer)
    print("\n=== Supplementary Query ===")
    extra_summary = compare_tool_assignment(SUPPLEMENTARY_QUERY)
    print(extra_summary.task_centric_answer)
    print("\n=== Custom Tools Demo ===")
    calculator = run_custom_tools_demo()
    print(f"Addition result: {calculator.addition_result}")
    print(f"Multiplication result: {calculator.multiplication_result}")