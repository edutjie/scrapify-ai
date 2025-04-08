# Scrapify AI - Cohesive AI Sheets Extension Clone

## How to run?

1. Install requirements

```shell
pip install -r .\requirements.txt
```

2. Fill in the .env(s)
3. Run FastAPI

```shell
fastapi dev app/main.py
```

4. Open the docs at `/docs` to learn about the endpoints

## Overview

This project is a functional and upgraded clone of the Cohesive AI Google Sheets Extension. It integrates AI-powered features directly into Google Sheets, enabling users to interact with ChatGPT and perform web/data scraping tasks without leaving the spreadsheet interface. The backend is built using **FastAPI**, and the frontend leverages **Google Apps Script**, connecting to the API endpoints. The project uses **GPT-4o-mini**, with optional model customization in the settings. I chose **Quantity-Driven Development Focus**, resulting in a robust MVP that mirrors and enhances key functionalities.

## Feature Replication & Improvement

| Feature                             | Original                      | Description                                                                                                                                                                                                                                                                                                                  |
| ----------------------------------- | ----------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `=CHAT(query)`                      | `=COHESIVE_GPT`               | Sends a prompt to ChatGPT and returns an intelligent response directly in the sheet. Ideal for writing help, summarization, brainstorming, or quick Q&A. Example: =CHAT("Hello") → "Hello! How can I assist you today?"                                                                                                      |
| `=WEBSEARCH(query, [instructions])` | `=COHESIVE_WEBSEARCH`         | Performs a live Google search through AI and extracts relevant insights from top results. Unlike the original, this version is agentic, it autonomously follows links, refines its search, and uses custom instructions to find accurate answers.                                                                            |
| `=SCRAPE_WEB(url, query)`           | `=COHESIVE_AGENT`             | Uses AI to visit the given URL and answer questions based on the page content. It is agentic, meaning it can navigate across multiple linked pages to locate the most relevant information, not just the initial URL.                                                                                                        |
| `=COMPANY_LINKEDIN(linkedin_url)`   | `=COHESIVE_BUSINESS_LINKEDIN` | Scrapes structured data from a LinkedIn company profile, including name, description, industry, size, headquarters, specialties, and more. Powered by Proxycurl for accurate and reliable extraction.                                                                                                                        |
| `=PERSON_LOOKUP(company_url, role)` | `=COHESIVE_PERSON_LOOKUP`     | Searches for the most relevant LinkedIn profile of someone in a specific role at the given company. Uses an agentic AI search to explore the web and return the best match based on job title and organization. Example: =PERSON_LOOKUP("https://maknadata.ai", "AI Engineer") → Returns: https://id.linkedin.com/in/edutjie |

## Why These Features?

These functionalities reflect high-impact use cases in real-world business scenarios:

- **Sales prospecting** – Finding company and personnel info without switching tools.
- **Market research** – Fast AI-powered summarization and web intelligence.
- **Automation & productivity** – Replaces manual tasks with smart, in-context AI queries.

## Design Choices

- **FastAPI backend**: Ensures scalability and modular integration with external APIs.
- **GPT-4o-mini**: Balances speed, cost, and performance for everyday tasks.
- **Agentic AI architecture**: Powers recursive searching, decision-making, and web exploration.
- **Serper.dev & Proxycurl**: Provide reliable search and LinkedIn data scraping, reducing friction and enhancing data fidelity.
- **Customizable models**: Allows advanced users to optimize for different AI models per task.
