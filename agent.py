from typing import TypedDict, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import GoogleSearchAPIWrapper
from langchain.tools import tool
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv
from markdown2 import markdown
import tempfile
import os
import subprocess
from pdf2image import convert_from_path
import smtplib
from email.message import EmailMessage
from pathlib import Path
from datetime import date

load_dotenv()

class NewsletterState(TypedDict):
    tech_news: Optional[str]
    finance_news: Optional[str]
    healthcare_news: Optional[str]
    newsletter: Optional[str]
    markdown_path: Optional[str]
    image_paths: Optional[list[str]]
    recipients: Optional[list[str]]
    
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2
)

search = GoogleSearchAPIWrapper()

@tool
def google_search_tool(query: str) -> str:
    """Search Google for recent news."""
    return search.run(query)

def tech_node(state: NewsletterState):
    prompt = """
        Summarize top 2–3 technology stories today.
        Categories:
        - AI & ML
        - Software
        - Hardware
        - Cybersecurity
        - Policy & Startups

        Max 80 words. Markdown.
        """
    response = llm.invoke(prompt, tools=[google_search_tool])
    return {"tech_news": response.content}

def finance_node(state: NewsletterState):
    prompt = """
        Summarize top 2–3 finance stories today.
        Categories:
        - Markets
        - Macro
        - Banking
        - M&A
        - Crypto

        Max 80 words.
        """
    response = llm.invoke(prompt, tools=[google_search_tool])
    return {"finance_news": response.content}

def healthcare_node(state: NewsletterState):
    prompt = """
        Summarize top 2–3 healthcare stories today.
        Categories:
        - Medical Research
        - Public Health
        - Pharma
        - HealthTech

        Max 80 words.
        """
    response = llm.invoke(prompt, tools=[google_search_tool])
    return {"healthcare_news": response.content}

def aggregator_node(state: NewsletterState):
    prompt = f"""
        # Daily Insights: Tech, Healthcare & Finance Digest

        Write a professional newsletter.

        ## Technology Highlights
        {state['tech_news']}

        ## Healthcare Highlights
        {state['healthcare_news']}

        ## Finance Highlights
        {state['finance_news']}

        Add:
        - Short intro
        - Closing paragraph
        - Optional CTA

        Markdown only.
        """
    response = llm.invoke(prompt)
    return {"newsletter": response.content}

def save_markdown(state: NewsletterState):

    path = "Newsletter(" + date.today().strftime("%d-%m-%Y") + ").md"
    with open(path, "w", encoding="utf-8") as f:
        f.write(state["newsletter"])
    return {"markdown_path": path}

def markdown_to_image_node(state: NewsletterState):
    markdown_path = state.get("markdown_path")

    with open(markdown_path, "r", encoding="utf-8") as f:
        md = f.read()

    html = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                background: white;
            }}
            .container {{
                width: 900px;
                margin: 40px auto;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            {markdown(md)}
        </div>
    </body>
    </html>
    """

    with tempfile.TemporaryDirectory() as tmpdir:
        html_path = os.path.join(tmpdir, "newsletter.html")
        pdf_path = os.path.join(tmpdir, "newsletter.pdf")

        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)

        # HTML → PDF
        subprocess.run(
            ["wkhtmltopdf", html_path, pdf_path],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        # PDF → images
        images = convert_from_path(pdf_path, dpi=200)

        image_paths = []
        for i, img in enumerate(images):
            path = f"Newsletter(" + date.today().strftime("%d-%m-%Y") + f")_{i+1}.png"
            img.save(path, "PNG")
            image_paths.append(path)

    return {
        "markdown_path": markdown_path,
        "image_paths": image_paths
    }

def send_newsletter_email_node(state: NewsletterState):
    """
    Expected state:
    {
        "image_paths": [list of PNG paths],
        "recipients": [list of email addresses]
    }
    """

    smtp_host = os.environ["SMTP_HOST"]
    smtp_port = int(os.environ["SMTP_PORT"])
    smtp_user = os.environ["SMTP_USER"]
    smtp_pass = os.environ["SMTP_PASS"]

    # recipients = state["recipients"]
    # image_paths = state["image_paths"]

    recipients = ["lakshsidhant@gmail.com"]
    image_paths = state["image_paths"]

    msg = EmailMessage()
    msg["From"] = smtp_user
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = "Daily Newsletter"

    # Build HTML body
    html_body = "<html><body>"
    html_body += "<h2>Today's Newsletter</h2>"

    for i, img_path in enumerate(image_paths):
        cid = f"image{i}"
        html_body += f'<img src="cid:{cid}" style="width:100%; max-width:900px;"><br><br>'

    html_body += "</body></html>"

    msg.set_content("Reader's Digest for " + date.today().strftime("%d-%m-%Y"))
    msg.add_alternative(html_body, subtype="html")

    # Attach images inline
    for i, img_path in enumerate(image_paths):
        path = Path(img_path)
        with open(path, "rb") as f:
            img_data = f.read()

        msg.get_payload()[1].add_related(
            img_data,
            maintype="image",
            subtype="png",
            cid=f"image{i}",
            filename=path.name,
        )

    # Send email
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)

    return {}

graph = StateGraph(NewsletterState)

graph.set_entry_point("start")

graph.add_node("start", lambda state: {})
graph.add_node("tech", tech_node)
graph.add_node("finance", finance_node)
graph.add_node("healthcare", healthcare_node)
graph.add_node("aggregate", aggregator_node)
graph.add_node("save_md", save_markdown)
graph.add_node("md_to_img", markdown_to_image_node)
graph.add_node("send_email", send_newsletter_email_node)


graph.add_edge("start", "tech")
graph.add_edge("start", "finance")
graph.add_edge("start", "healthcare")

graph.add_edge("tech", "aggregate")
graph.add_edge("finance", "aggregate")
graph.add_edge("healthcare", "aggregate")

graph.add_edge("aggregate", "save_md")
graph.add_edge("save_md", "md_to_img")
graph.add_edge("md_to_img", "send_email")
graph.add_edge("send_email", END)

app = graph.compile()

result = app.invoke({})
