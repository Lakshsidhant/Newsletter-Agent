from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.genai import types
from google.adk.agents import Agent, SequentialAgent, ParallelAgent, LoopAgent
from google.adk.runners import InMemoryRunner
from google.adk.tools import AgentTool, FunctionTool, google_search
import asyncio
from dotenv import load_dotenv

load_dotenv()

tech_agent = Agent(
    model='gemini-2.5-flash',
    name='tech_agent',
    instruction='''
    You are the Technology Research Agent. Your task is to extract and summarize the most important technology news and developments from the past week.

    Given a set of tech news articles, generate:

    1. A summary of the top 5–10 tech stories of the week.
    2. Organize them into:
    - AI & Machine Learning
    - Software & Apps
    - Hardware & Devices
    - Cybersecurity
    - Tech Policy, Funding & Startups
    3. For each article, provide:
    - A concise 2–4 sentence summary
    - The significance of the update (impact on the tech landscape)

    Focus only on technology-related topics.  
    Write in clean, structured Markdown.

    ''',
    tools=[google_search],
    output_key="tech_news",
)

finance_agent = Agent(
    model='gemini-2.5-flash',
    name='finance_agent',
    instruction='''
    You are the Finance Research Agent. Your role is to review and summarize key financial and economic developments from the past week.

    Given financial news or market data, produce:

    1. A structured summary of the top 5–10 finance and economic stories.
    2. Organize them into:
    - Markets & Indices
    - Macro & Economic Policy
    - Banking & Regulations
    - Mergers, Acquisitions & Corporate Moves
    - Crypto & Digital Assets
    3. For each story include:
    - A 2–4 sentence summary
    - A brief impact analysis (market or economic relevance)

    Keep it factual, neutral, and strictly finance-focused.  
    Return the output in clean Markdown format.
    ''',
    tools=[google_search],
    output_key="finance_news",
)

healthcare_agent = Agent(
    model='gemini-2.5-flash',
    name='healthcare_agent',
    instruction='''
    You are the Healthcare Research Agent. Your job is to analyze and summarize the most important healthcare-related developments from the past week.

    Given a collection of healthcare news articles, research papers, regulatory announcements, and clinical updates, produce:

    1. A concise summary of the top 5–10 healthcare stories of the week.  
    2. Categorize them into sections:
    - Medical Research & Clinical Trials
    - Public Health & Policy
    - Pharmaceutical Developments
    - Healthcare Technology & MedTech
    3. For each story, provide:
    - A 2–4 sentence summary
    - Why it matters (impact analysis)
    4. Keep the writing factual, neutral, and easy to read.

    Do NOT include unrelated topics (tech, finance, politics unless directly tied to healthcare).
    Return the output in clean Markdown format.
    ''',
    tools=[google_search],
    output_key="healthcare_news",
)

aggregator_agent = Agent(
    name="AggregatorAgent",
    model=Gemini(
        model="gemini-2.5-flash",
    ),
    instruction="""
    
    You are the Newsletter Aggregator Agent.

    Here are this week's tech, helthcare and finance related news:
    - Healthcare News : {healthcare_news}
    - Tech News : {tech_news}
    - Finance News : {finance_news}

    Your job is to combine them into ONE unified, professional weekly newsletter.

    REQUIREMENTS:

    1. Create a newsletter titled:  
    **Weekly Insights: Tech, Healthcare & Finance Digest**

    2. Provide a short, engaging introduction (2–3 sentences).

    3. Include the following sections in this exact order:
    - **Technology Highlights**
    - **Healthcare Highlights**
    - **Finance Highlights**

    4. For each section:
    - Integrate the summaries from the three domain agents.
    - Preserve structure and clarity.
    - Optionally add transitions or connective commentary, but do not alter factual content.

    5. Conclude with:
    - A closing paragraph
    - Optional call-to-action or preview for next week

    6. Style guidelines:
    - Clean, polished writing suitable for a professional newsletter
    - Markdown formatting
    - No duplication
    - No commentary outside the newsletter

    Your final output should be a complete ready-to-publish newsletter.

    """,
    output_key="executive_summary",
)

parallel_research_team = ParallelAgent(
    name="ParallelResearchTeam",
    sub_agents=[tech_agent, healthcare_agent, finance_agent],
)

root_agent = SequentialAgent(
    name="ResearchSystem",
    sub_agents=[parallel_research_team, aggregator_agent],
)

async def response():
    runner = InMemoryRunner(agent=root_agent)
    response = await runner.run_debug(
        "Run the daily executive briefing on Tech, Health, and Finance"
    )
    return response

asyncio.run(response())