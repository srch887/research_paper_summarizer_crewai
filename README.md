# Research Paper Summarizer

A FastAPI-based application powered by CrewAI and Google Gemini LLM that fetches research papers (Arxiv/IEEE), parses their PDFs, and generates clear, structured summaries with outlines and fact-checked content.

## Features

- Fetches and parses research papers in PDF format (Arxiv/IEEE).
- Uses a multi-agent system for:
  - Content planning
  - Summarization
  - Editing and fact-checking
- Exposes a REST API built with FastAPI.
- Returns structured summaries in Markdown format, ready for frontend rendering.
- CORS enabled for integration with frontend applications.

## Tech Stack

- **Python 3.10+**
- **FastAPI** for the API
- **CrewAI** for agent orchestration
- **Gemini LLM** via Google API
- **pypdf** for PDF parsing
- **dotenv** for environment variable management

## Project Structure
```bash
research_paper_summarizer.py # Main script
app.py # FastAPI server
.env # Environment variables (API keys)
README.md # Documentation
```


---

## Features

- Fetches and parses research papers in PDF format (Arxiv/IEEE).
- Uses a multi-agent system for:
  - Content planning
  - Summarization
  - Editing and fact-checking
- Exposes a REST API built with FastAPI.
- Returns structured summaries in Markdown format, ready for frontend rendering.
- CORS enabled for integration with frontend applications.

---

## Agents

### 1. **Content Planner**
- **Role:** Extracts structure & main points from the paper
- **Output:** Outline with headings and subheadings  

### 2. **Video Summarizer**
- **Role:** Condenses full paper into a structured summary
- **Output:** Clear, readable summary with logical formatting  

### 3. **Editor & Fact Checker**
- **Role:** Proofreads, checks grammar/style, and validates summary against paper  
- **Output:** Polished, accurate, fact-checked summary  

---

##  Tasks

1. **Fetch Transcript Task** → Downloads and extracts raw PDF text
2. **Content Planner Task** → Creates structured outline  
3. **Summarization Task** → Generates structured summary  
4. **Editing Task** → Proofreads + fact-checks final summary  

---

## Usage

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```
### 2. Set Environment Variables

Create a .env file:
```bash
GEMINI_API_KEY="your_api_key_here"
```
### 3. Run the local server
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 
```
### 4. Send a POST request with a research paper link:
```
curl -X POST "http://localhost:8000/summarize" \
  -H "Content-Type: application/json" \
  -d '{
    "research_paper_link": "https://arxiv.org/pdf/1504.00113.pdf"
  }'
```
### 5. Run the script locally (Optional)
```bash
python research_paper_summarizer.py <RESEARCH_PAPER_URL>
```
