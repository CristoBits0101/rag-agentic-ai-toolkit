# --- DEPENDENCIAS ---
from pathlib import Path
import random
from typing import Annotated

from config.ag2_tutorial_config import BUGS
from config.ag2_tutorial_config import DEFAULT_LLM_CONFIG
from config.ag2_tutorial_config import LESSON_TOPIC
from config.ag2_tutorial_config import SUPPORT_TICKET
from models.ag2_compat import AssistantAgent
from models.ag2_compat import ConversableAgent
from models.ag2_compat import GroupChat
from models.ag2_compat import GroupChatManager
from models.ag2_compat import LocalCommandLineCodeExecutor
from models.ag2_compat import UserProxyAgent
from models.ag2_compat import register_function
from models.ag2_entities import TicketSummary


def conversational_agent_demo():
    llm_config = DEFAULT_LLM_CONFIG
    student = ConversableAgent(
        name="student",
        system_message="You are a curious student. You ask clear specific questions to learn new concepts.",
        human_input_mode="NEVER",
        llm_config=llm_config,
    )
    tutor = ConversableAgent(
        name="tutor",
        system_message="You are a helpful tutor who provides clear and concise explanations suitable for a beginner.",
        human_input_mode="NEVER",
        llm_config=llm_config,
    )
    return student.initiate_chat(tutor, "Can you explain what a neural network is?", max_turns=2, summary_method="reflection_with_llm")


def build_specialized_agents():
    llm_config = DEFAULT_LLM_CONFIG
    tech_expert = ConversableAgent(
        name="tech_expert",
        system_message="You are a senior software engineer with expertise in Python AI and system design.",
        llm_config=llm_config,
    )
    creative_writer = ConversableAgent(
        name="creative_writer",
        system_message="You are a creative writer and storyteller.",
        llm_config=llm_config,
    )
    business_analyst = ConversableAgent(
        name="business_analyst",
        system_message="You are a business analyst focused on ROI efficiency and strategic planning.",
        llm_config=llm_config,
    )
    return [tech_expert, creative_writer, business_analyst]


def built_in_agent_demo():
    llm_config = DEFAULT_LLM_CONFIG
    assistant = AssistantAgent(
        name="assistant",
        system_message="You are a helpful assistant who writes and explains Python code clearly.",
        llm_config=llm_config,
    )
    user_proxy = UserProxyAgent(
        name="user_proxy",
        human_input_mode="NEVER",
        code_execution_config={"executor": LocalCommandLineCodeExecutor(work_dir="coding", timeout=30)},
    )
    result = user_proxy.initiate_chat(
        recipient=assistant,
        message="Plot a sine wave using a local file and save it as sine_wave.svg.",
        max_turns=2,
        summary_method="reflection_with_llm",
    )
    return result, Path("coding/sine_wave.svg")


def human_in_the_loop_demo():
    triage_bot = ConversableAgent(
        name="triage_bot",
        system_message="You are a bug triage assistant.",
        llm_config=DEFAULT_LLM_CONFIG,
    )
    human = ConversableAgent(name="human", human_input_mode="ALWAYS", scripted_responses=["Yes escalate it.", "Closing this makes sense.", "Keep this one medium priority."])
    selected_bugs = BUGS[:3]
    outputs = []
    for bug in selected_bugs:
        assistant_message = triage_bot._generate_reply(bug, sender=human)
        human_message = human._generate_reply(assistant_message, sender=triage_bot)
        outputs.append({"bug": bug, "assistant": assistant_message, "human": human_message})
    return outputs


def group_chat_lesson_planning_demo():
    llm_config = DEFAULT_LLM_CONFIG
    lesson_planner = ConversableAgent(name="planner_agent", system_message="Create a short lesson plan for 4th graders.", description="Makes lesson plans.", llm_config=llm_config)
    lesson_reviewer = ConversableAgent(name="reviewer_agent", system_message="Review a plan and suggest up to 3 brief edits.", description="Reviews lesson plans.", llm_config=llm_config)
    teacher = ConversableAgent(name="teacher_agent", system_message="Suggest a topic and reply DONE when satisfied.", llm_config=llm_config, is_termination_msg=lambda x: "DONE" in (x.get("content", "") or "").upper())
    groupchat = GroupChat(agents=[teacher, lesson_planner, lesson_reviewer], messages=[], max_round=6, speaker_selection_method="auto")
    manager = GroupChatManager(name="group_manager", groupchat=groupchat, llm_config=llm_config)
    return teacher.initiate_chat(manager, LESSON_TOPIC, max_turns=6, summary_method="reflection_with_llm")


def tools_and_extensions_demo():
    def is_prime(n: Annotated[int, "Positive integer"]) -> str:
        if n < 2:
            return "No"
        for divisor in range(2, int(n ** 0.5) + 1):
            if n % divisor == 0:
                return "No"
        return "Yes"

    math_asker = ConversableAgent(name="math_asker", system_message="Ask whether a number is prime.", llm_config=DEFAULT_LLM_CONFIG)
    math_checker = ConversableAgent(name="math_checker", human_input_mode="NEVER", llm_config=DEFAULT_LLM_CONFIG)
    register_function(is_prime, caller=math_asker, executor=math_checker, description="Check if a number is prime.")
    return math_checker.initiate_chat(math_asker, "Is 72 a prime number?", max_turns=2)


def structured_outputs_demo():
    support_agent = ConversableAgent(
        name="support_agent",
        system_message="You are a support assistant.",
        llm_config={**DEFAULT_LLM_CONFIG, "response_format": TicketSummary},
    )
    return support_agent.generate_structured_output(SUPPORT_TICKET)


def run_ag2_tutorial_demo() -> None:
    chat_result = conversational_agent_demo()
    print("=== Conversable Agent ===")
    print(chat_result.summary)
    print("\n=== Specialized Agents ===")
    for agent in build_specialized_agents():
        print(f"- {agent.name}: {agent._generate_reply('Summarize your angle.')}")
    print("\n=== Assistant and UserProxy ===")
    built_in_result, artifact_path = built_in_agent_demo()
    print(built_in_result.summary)
    print(f"Artifact created: {artifact_path}")
    print("\n=== Human in the Loop ===")
    print(human_in_the_loop_demo())
    print("\n=== Group Chat ===")
    print(group_chat_lesson_planning_demo().summary)
    print("\n=== Tools ===")
    print(tools_and_extensions_demo().summary)
    print("\n=== Structured Output ===")
    print(structured_outputs_demo())