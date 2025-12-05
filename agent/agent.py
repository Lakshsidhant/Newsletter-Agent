from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.agents import Agent, SequentialAgent
from google.adk.runners import InMemoryRunner
from google.adk.tools import AgentTool, google_search
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters
import asyncio
from dotenv import load_dotenv
from markdown2 import markdown
from html2image import Html2Image
import tempfile
import os

load_dotenv()

tech_agent = Agent(
    model='gemini-2.5-flash',
    name='tech_agent',
    instruction='''
    You are the Technology Research Agent. Your task is to extract and summarize the most important technology news and developments from today.

    Given a set of tech news articles, generate:

    1. A summary of the top 2-3 tech stories of today.
    2. They should fall under the following categories:
    - AI & Machine Learning
    - Software & Apps
    - Hardware & Devices
    - Cybersecurity
    - Tech Policy, Funding & Startups

    Focus only on technology-related topics. The output shouldn't be more than 80 words. 
    Write in clean, structured markdown UTF-8 encoding format.

    ''',
    tools=[google_search],
    output_key="tech_news",
)

finance_agent = Agent(
    model='gemini-2.5-flash',
    name='finance_agent',
    instruction='''
    You are the Finance Research Agent. Your role is to review and summarize key financial and economic developments of today.

    Given financial news or market data, produce:

    1. A structured summary of the top 2-3 finance and economic stories.
    2. They should fall under the following categories:
    - Markets & Indices
    - Macro & Economic Policy
    - Banking & Regulations
    - Mergers, Acquisitions & Corporate Moves
    - Crypto & Digital Assets

    Keep it factual, neutral, and strictly finance-focused.  The output shouldn't be more than 80 words. 
    Return the output in clean UTF-8 encoding format.
    ''',
    tools=[google_search],
    output_key="finance_news",
)

healthcare_agent = Agent(
    model='gemini-2.5-flash',
    name='healthcare_agent',
    instruction='''
    You are the Healthcare Research Agent. Your job is to analyze and summarize the most important healthcare-related developments from today.

    Given a collection of healthcare news articles, research papers, regulatory announcements, and clinical updates, produce:

    1. A concise summary of the top 2-3 healthcare stories of today.  
    2. They should fall under the following categories:
    - Medical Research & Clinical Trials
    - Public Health & Policy
    - Pharmaceutical Developments
    - Healthcare Technology & MedTech

    Keep the writing factual, neutral, and easy to read. The output shouldn't be more than 80 words.
    Return the output in clean UTF-8 encoding format.
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

    Get today's news in healtchcare, technology, and finance from three domain-specific tools:
    - Healthcare News : "healthcare_agent"
    - Tech News : "tech_agent"
    - Finance News : "finance_agent"
    
    Your task is to combine their outputs into a single, cohesive daily newsletter.

    REQUIREMENTS:

    1. Create a newsletter titled:  
    Daily Insights: Tech, Healthcare & Finance Digest

    2. Provide a short, engaging introduction (2–3 sentences).

    3. Include the following sections in this exact order:
    - Technology Highlights
    - Healthcare Highlights
    - Finance Highlights

    4. For each section:
    - Integrate the summaries from the three domain agents.
    - Preserve structure and clarity.
    - Optionally add transitions or connective commentary, but do not alter factual content.

    5. Conclude with:
    - A closing paragraph
    - Optional call-to-action or preview for tomorrow's edition.

    6. Style guidelines:
    - Clean, polished writing suitable for a professional newsletter
    - Markdown formatting
    - No duplication
    - No commentary outside the newsletter

    Your final output should be a complete ready-to-publish newsletter.

    The output should be in UTF-8 encoding format.
    """,
    tools=[AgentTool(tech_agent), AgentTool(healthcare_agent), AgentTool(finance_agent)],
    output_key="newsletter",
)

def download_md(filename="newsletter.md", content=""):
        with open(filename, "w") as f:
            f.write(content)
        return {"file_path": filename}

def markdown_to_image(md_path: str, output_path: str):
    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    html_body = markdown(md_text)

    html = f"""
    <html>
    <head>
    <style>
        html, body {{
            background: white !important;
            margin: 0;
            padding: 0;
        }}
        .container {{
            width: 900px;
            margin: 40px auto;
            font-family: Arial, sans-serif;
            font-size: 16px;
            line-height: 1.6;
            color: black;
        }}
        pre {{
            background: #1e1e1e;
            color: #dcdcdc;
            padding: 12px;
            border-radius: 8px;
            overflow-x: auto;
        }}
        code {{
            background: #f4f4f4;
            padding: 2px 4px;
            border-radius: 5px;
        }}
    </style>
    </head>
    <body>
        <div class="container">
            {html_body}
        </div>
    </body>
    </html>
    """

    hti = Html2Image()

    # Create temp HTML file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as temp:
        temp.write(html.encode("utf-8"))
        temp_path = temp.name

    # Take screenshot WITHOUT size parameter
    hti.screenshot(
        html_file=temp_path,
        save_as=os.path.basename(output_path)
    )

    os.replace(os.path.basename(output_path), output_path)
    os.remove(temp_path)

    return output_path

markdown_agent = Agent(
    name="MarkdownAgent",
    model=Gemini(
        model="gemini-2.5-flash",
    ),
    instruction="""
    
    You are the Markdown Agent.

    You are given a markdown file : {newsletter}
    
    Download it as newsletter.md using the "download_md" tool, then convert the markdown content to a PNG image using "markdown_to_image" tool.
    """,
    tools=[download_md, markdown_to_image]
)

linkedin_agent = Agent(
    model="gemini-2.5-flash",
    name="linkedin_agent",
    instruction="Post the given article to LinkedIn using the MCP tool : {newsletter}",
    tools=[
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params = StdioServerParameters(
                    command="npx",
                    args=[
                        "mcp-remote",
                        "https://mcp.zapier.com/api/mcp/s/Y2E1NzU0OGYtODg2Ny00N2IxLWFmNzQtNTRhZGIxOGYxOTBiOjQwMjViNDk5LTY1NzUtNDYwYi04YzAzLWE5NjZiNTcxMjEyZQ==/mcp",
                    ],
                ),
                timeout=30,
            ),
        )
    ],
)

root_agent = SequentialAgent(
    name="root_agent",
    sub_agents=[aggregator_agent, markdown_agent, linkedin_agent]
)

async def response():
    runner = InMemoryRunner(agent=root_agent)
    response = await runner.run_debug(
        "Run the daily executive briefing on Tech, Health, and Finance using 'aggregator_agent' and Download the newsletter markdown file and convert it to image using 'markdown_agent'. Also, post the newsletter to LinkedIn using 'linkedin_agent'.",
    )

    return response

asyncio.run(response())