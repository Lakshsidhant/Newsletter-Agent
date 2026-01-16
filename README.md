# 📰 Agentic Daily Newsletter Generator (LangGraph + Gemini)

An **agentic Python pipeline** that automatically:
- Fetches daily **Technology, Finance, and Healthcare** news
- Summarizes them using **Gemini (Google Generative AI)**
- Compiles a professional **Markdown newsletter**
- Converts it into **images**
- Sends it via **email** using SMTP

Built using **LangGraph**, **LangChain**, and **Google Search Tooling**.

---

## 🔧 Architecture Overview

This project uses a **stateful agent graph** (LangGraph) with parallel execution and deterministic flow.

### Flow
```
Start
 ├─ Tech News Agent
 ├─ Finance News Agent
 ├─ Healthcare News Agent
        ↓
 Aggregator Agent
        ↓
 Markdown Saver
        ↓
 Markdown → PDF → Image Converter
        ↓
 Email Sender
        ↓
 End
```

### Core Technologies
- **LangGraph** – Agent orchestration
- **LangChain** – LLM & tool abstraction
- **Gemini 2.5 Flash** – Content generation
- **Google Search API** – Live news retrieval
- **wkhtmltopdf + pdf2image** – Markdown → Image
- **SMTP** – Email delivery

---

## ✨ Features

- Parallel news fetching across domains
- Tool-augmented LLM calls (Google Search)
- Deterministic agent pipeline (no spaghetti code)
- Markdown-first content generation
- Email-ready inline images
- Date-stamped outputs for traceability

---

## 📦 Requirements

### Python
- Python **3.10+**

### System Dependencies (Mandatory)

#### wkhtmltopdf
Used for HTML → PDF conversion.

- Windows: https://wkhtmltopdf.org/downloads.html
- Linux:
```bash
sudo apt install wkhtmltopdf
```

#### Poppler (for pdf2image)
- Windows: Download Poppler and add `bin/` to PATH
- Linux:
```bash
sudo apt install poppler-utils
```

---

## 📚 Python Dependencies

```bash
pip install \
  langgraph \
  langchain \
  langchain-google-genai \
  langchain-community \
  google-search-results \
  python-dotenv \
  markdown2 \
  pdf2image
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root.

### Google APIs
```env
GOOGLE_API_KEY=your_gemini_api_key
GOOGLE_CSE_ID=your_custom_search_engine_id
```

---

### SMTP (Email Sending)

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASS=your_app_password
```

⚠️ Gmail users must use an App Password.

---

## ▶️ How to Run

```bash
python newsletter.py
```

---

## 📤 Email Behavior

- Images are embedded inline
- HTML email body auto-generated
- Subject: Daily Newsletter

---

## 🚨 Known Limitations

- No retry logic
- No scheduler
- Hardcoded email recipient
- Images only (no PDF attachment)

---

## 🛣️ Recommended Extensions

- Cron / EventBridge scheduling
- S3 storage
- Observability (LangSmith)
- AWS deployment

---

## 📜 License

MIT
