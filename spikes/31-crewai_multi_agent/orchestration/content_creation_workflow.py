# --- DEPENDENCIAS ---
from config.content_pipeline_config import DEFAULT_TOPIC
from models.content_llm_gateway import build_content_model
from models.content_pipeline_entities import ContentPipelineSummary
from models.crewai_compat import Agent
from models.crewai_compat import Crew
from models.crewai_compat import Process
from models.crewai_compat import Task
from models.search_tooling import LocalTopicSearchTool


def _invoke_model(agent: Agent, prompt: str) -> str:
    response = agent.llm.invoke(prompt)
    return str(getattr(response, "content", response)).strip()


def execute_research_task(agent: Agent, description: str, context_text: str, inputs: dict) -> str:
    topic = inputs["topic"]
    search_results = agent.tools[0].run(topic) if agent.tools else {"insights": []}
    prompt = (
        f"Role: {agent.role}. Goal: {agent.goal}.\n\n"
        f"Topic: {topic}\n"
        f"Task: {description}\n"
        f"Insights: {search_results['insights']}\n"
        "Write a detailed report with trends technologies and likely impact for practitioners."
    )
    return _invoke_model(agent, prompt)


def execute_writer_task(agent: Agent, description: str, context_text: str, inputs: dict) -> str:
    prompt = (
        f"Role: {agent.role}. Goal: {agent.goal}.\n\n"
        f"Task: {description}\n"
        f"Research Context:\n{context_text}\n\n"
        "Write a four paragraph blog post for a tech savvy audience. Keep it clear and engaging."
    )
    return _invoke_model(agent, prompt)


def execute_social_task(agent: Agent, description: str, context_text: str, inputs: dict) -> str:
    prompt = (
        f"Role: {agent.role}. Goal: {agent.goal}.\n\n"
        f"Task: {description}\n"
        f"Blog Content:\n{context_text}\n\n"
        "Generate three short social posts suitable for LinkedIn or X."
    )
    return _invoke_model(agent, prompt)


def build_agents(model=None):
    llm = model or build_content_model()
    research_agent = Agent(
        role="Senior Research Analyst",
        goal="Uncover cutting edge information and insights on any subject with comprehensive analysis",
        backstory="An expert researcher who gathers signals separates hype from substance and summarizes trends clearly.",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=[LocalTopicSearchTool()],
    )
    writer_agent = Agent(
        role="Tech Content Strategist",
        goal="Craft well structured and engaging content based on research findings",
        backstory="A skilled content strategist who turns complex technical findings into narratives that busy engineers can scan quickly.",
        verbose=True,
        allow_delegation=True,
        llm=llm,
    )
    social_agent = Agent(
        role="Social Media Strategist",
        goal="Generate engaging social media snippets based on the full article",
        backstory="A digital storyteller who converts long form insights into short posts that drive attention and clicks.",
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )
    return research_agent, writer_agent, social_agent


def build_tasks(research_agent: Agent, writer_agent: Agent, social_agent: Agent):
    research_task = Task(
        description="Analyze the major {topic} identifying key trends and technologies. Provide a detailed report on their potential impact.",
        agent=research_agent,
        expected_output="A detailed report on {topic} including trends emerging technologies and impact.",
        executor=execute_research_task,
    )
    writer_task = Task(
        description="Create an engaging blog post based on the research findings about {topic}. Tailor the content for a tech savvy audience and ensure clarity.",
        agent=writer_agent,
        expected_output="A four paragraph blog post on {topic} written clearly and engagingly for tech enthusiasts.",
        context=[research_task],
        executor=execute_writer_task,
    )
    social_task = Task(
        description="Summarize the blog post about {topic} into three engaging social posts suitable for LinkedIn or X.",
        agent=social_agent,
        expected_output="Three concise social posts highlighting the key insights from the article.",
        context=[writer_task],
        executor=execute_social_task,
    )
    return research_task, writer_task, social_task


def build_content_creation_crew(model=None):
    research_agent, writer_agent, social_agent = build_agents(model=model)
    research_task, writer_task, social_task = build_tasks(research_agent, writer_agent, social_agent)
    crew = Crew(
        agents=[research_agent, writer_agent, social_agent],
        tasks=[research_task, writer_task, social_task],
        process=Process.sequential,
        verbose=True,
    )
    return crew, research_task, writer_task, social_task


def run_content_pipeline(topic: str = DEFAULT_TOPIC, model=None) -> ContentPipelineSummary:
    crew, _, _, _ = build_content_creation_crew(model=model)
    result = crew.kickoff(inputs={"topic": topic})
    return ContentPipelineSummary(
        topic=topic,
        research_report=result.tasks_output[0].raw,
        blog_post=result.tasks_output[1].raw,
        social_posts=result.tasks_output[2].raw,
    )


def run_crewai_content_demo() -> None:
    summary = run_content_pipeline()
    print("=== Research Report ===")
    print(summary.research_report)
    print("\n=== Blog Post ===")
    print(summary.blog_post)
    print("\n=== Social Posts ===")
    print(summary.social_posts)