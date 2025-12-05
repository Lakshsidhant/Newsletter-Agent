# Daily Insights Automation (Tech · Healthcare · Finance)

This project is an automated daily newsletter generator built using **Google ADK**. It uses multiple agents to collect news, summarize it, format it into a newsletter, convert it into an image, and post it to LinkedIn — all autonomously.

## ⭐ What It Does

- Collects the latest **Tech**, **Healthcare**, and **Finance** updates  
- Summarizes each category using domain‑specific agents  
- Combines them into one polished Markdown newsletter  
- Saves it as `newsletter.md`  
- Converts it into a PNG image  
- Posts the newsletter to LinkedIn automatically

## 🧠 Agents Involved

- **tech_agent** — Technology news summarizer  
- **healthcare_agent** — Healthcare news summarizer  
- **finance_agent** — Finance news summarizer  
- **aggregator_agent** — Merges all summaries  
- **markdown_agent** — Saves markdown + converts to PNG  
- **linkedin_agent** — Publishes to LinkedIn  
- **root_agent** — Runs the pipeline

## 🛠️ Tech Stack

- Google ADK  
- Gemini 2.5 Flash  
- Google Search Tool  
- MCP Remote (LinkedIn automation)  
- markdown2 + html2image  
- Python asyncio  

## ▶️ How to Run

```bash
python main.py
```

This triggers the full pipeline:  
**research → summarize → compile → save → convert → publish**

## 📄 Outputs

- `newsletter.md` — generated newsletter  
- `newsletter.png` — rendered image  
- LinkedIn post — automatically published
