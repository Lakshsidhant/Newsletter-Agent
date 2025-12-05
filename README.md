# Weekly Insights Multi-Agent Newsletter System

## Overview

This project is an **AI-powered Multi-Agent Research & Newsletter Generation System** designed to automatically gather, analyze, and summarize weekly updates across three major domains: **Technology**, **Finance**, and **Healthcare**. The system acts as an autonomous research team—each agent specializing in a specific domain—and produces a polished, ready-to-publish **Weekly Insights Newsletter** without human intervention.

The motivation behind the project is simple:  
**Staying updated with cross-industry news is time-consuming, fragmented, and often overwhelming.**  
Professionals, founders, analysts, and students frequently check dozens of websites and reports—yet still struggle to synthesize everything into concise insights. This project solves that problem by using multi-agent collaboration, real-time search, and automated content generation.

---

## What I Built

### 1. Multi-Agent Research Architecture

The system uses the **Google ADK (Agent Development Kit)** and **Gemini 2.5 Flash LLM** to build an intelligent network of specialized agents, including:

- Tech Research Agent  
- Finance Research Agent  
- Healthcare Research Agent  
- Aggregator Agent  
- Parallel Execution Layer  
- Sequential Orchestration Layer  

Each agent is assigned a domain, search tools, strict formatting, and clear output expectations. Together, they emulate a real-world research and editorial workflow.

---

### 2. Domain-Specialized Research Agents

#### Technology Agent
Extracts the top tech updates categorized into:
- AI & Machine Learning  
- Software & Apps  
- Hardware & Devices  
- Cybersecurity  
- Tech Policy, Funding & Startups  

Each story includes:
- A short summary  
- Impact analysis  

#### Finance Agent
Summarizes:
- Markets & Indices  
- Macroeconomic Policy  
- Banking & Regulations  
- Mergers & Acquisitions  
- Crypto & Digital Assets  

#### Healthcare Agent
Analyzes:
- Medical Research & Clinical Trials  
- Public Health & Policy  
- Pharmaceutical Developments  
- MedTech & Innovation  

Each output is structured, factual, and domain-focused.

---

## 3. Parallel Research Execution

A **ParallelAgent** runs all three domain agents simultaneously, resulting in:
- Faster execution  
- Real-time industry insights  
- Scalability  

---

## 4. Aggregator & Newsletter Generator

The **Aggregator Agent** combines outputs into a unified newsletter.  
It produces:

- Title  
- Engaging introduction  
- Technology Highlights  
- Healthcare Highlights  
- Finance Highlights  
- Closing paragraph  

The writing is clean, professional, and immediately ready to publish.

---

## 5. End-to-End Processing Pipeline

A **SequentialAgent** handles:
1. Triggering parallel agents  
2. Collecting domain outputs  
3. Passing data to the Aggregator Agent  
4. Returning the final newsletter  

An **InMemoryRunner** executes the entire sequence on demand.

---

## 6. Automated Weekly Research System

This system automates:
- Research  
- Summarization  
- Categorization  
- Editorial work  
- Newsletter generation  

The only user input needed is a single instruction, such as:  
**“Run the daily executive briefing on Tech, Health, and Finance.”**

---

## 7. Why This Project is Valuable

- Saves time for professionals  
- Provides structured, reliable insights  
- Scalable across more domains  
- Uses real-time Google Search  
- Produces publication-ready content  

---

## 8. Technical Stack

- Google ADK (Agent Development Kit)  
- Gemini 2.5 Flash  
- Python + asyncio  
- Parallel & Sequential Agents  
- Google Search API Integration  

---

## 9. Key Innovations

- Multi-agent collaboration  
- Automatic structured formatting  
- Fully automated research pipeline  
- Fast and scalable processing  

---

## 10. Real-World Applications

- Weekly newsletters  
- Market intelligence  
- Startup research  
- Healthcare/tech trend tracking  
- Executive briefings  
- Student research assistance  

---

## Conclusion

This project showcases the power of multi-agent AI systems, structured workflows, and real-time data. It recreates the workflow of a full research and editorial team, delivering polished weekly insights across Technology, Finance, and Healthcare with a single command.

It is fast, scalable, and impactful—ideal for anyone who needs professional-grade insights generated automatically.

