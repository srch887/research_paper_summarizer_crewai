#!/usr/bin/env uv run

# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "crewai",
#     "crewai-tools",
#     "python-dotenv",
#     "youtube-transcript-api",
# ]
# ///

from crewai.tools import BaseTool
from crewai import Agent, LLM, Task, Crew, Process
from pypdf import PdfReader
import os
import io
import re
import requests
from dotenv import load_dotenv

load_dotenv()

gemini_api_key = os.getenv('GEMINI_API_KEY')

# Use Gemini 2.5 Pro Experimental model
gemini_llm = LLM(
    model='gemini/gemini-2.0-flash',
    api_key=gemini_api_key,
    provider='google',
    temperature=0.1  # Lower temperature for more consistent results.
)

class fetchAndParseResearchPaper(BaseTool):
    name: str = "Fetch and Parse Research Paper"
    description: str = "Fetch and Parse a research paper in PDF format from Arxiv/IEEE"
    
    def _run(self, link: str) -> str:
        response = requests.get(url= link)
        
        reader = PdfReader(io.BytesIO(response.content))
        
        text_raw = ""      
        for page in reader.pages:
            text_raw += page.extract_text() or ""
            
        text_clean = " ".join(text_raw.split())
        
        return text_clean

read_research_paper = fetchAndParseResearchPaper()

# 1. Content Planner
content_planner = Agent(
    role="Content Planner",
    goal="Create a clear outline of the Research Paper with relevant headings and subheadings.",
    backstory=(
        "You are an expert content strategist who specializes in extracting "
        "the structure and key talking points from transcripts to make them "
        "easy to digest as outlines."
    ),
    verbose=False,
    allow_delegation=False,
    llm=gemini_llm
)

# 2. Video Summarizer
paper_summarizer = Agent(
    role="Research Paper Summarizer",
    goal="Summarize the Research Paper into a clear, structured summary with required headings and subheadings.",
    backstory=(
        "You specialize in condensing long Research Papers into readable "
        "summaries. You emphasize clarity, brevity, and proper formatting."
    ),
    verbose=False,
    allow_delegation=False,
    tools=[read_research_paper],
    llm=gemini_llm
)

# 3. Editor (Fact Checker)
editor = Agent(
    role="Editor & Fact Checker",
    goal=(
        "Proofread and fact-check the final summary against the paper. "
        "Ensure grammar, spelling, and structure are correct, and validate "
        "that all key points in the transcript are accurately represented."
    ),
    backstory=(
        "You are a meticulous editor with a keen eye for detail. "
        "You check not only for readability but also for accuracy, ensuring "
        "the summary faithfully reflects the contents of the research paper."
    ),
    verbose=False,
    allow_delegation=False,
    llm=gemini_llm
)

# 1. Fetch Transcript
fetch_transcript_task = Task(
    description=(
        "Fetch the pdf from the provided research paper link: {research_paper_link}. "
        "Return only the raw text."
    ),
    expected_output="The complete transcript text of the research paper.",
    agent=paper_summarizer,
    tools=[read_research_paper],
)

# 2. Content Outline
content_planner_task = Task(
    description=(
        "Using the raw text, create an outline of the research paper. "
        "The outline must contain clear headings and subheadings "
        "that represent the main topics and sections of the research paper."
    ),
    expected_output="An organized outline with relevant headings and subheadings.",
    agent=content_planner,
)

# 3. Summarization
summarization_task = Task(
    description=(
        "Using the raw text, write a structured summary of the research paper. "
        "Include headings and subheadings as appropriate, and keep it concise "
        "while preserving key details. Make sure to markdown the output"
    ),
    expected_output="A clear, structured summary of the research paper.",
    agent=paper_summarizer,
)

# 4. Editing & Fact Checking
editing_task = Task(
    description=(
        "Proofread and fact-check the structured summary against the raw text. "
        "Ensure grammar, spelling, and readability are excellent. "
        "Verify that all important points in the research paper are covered accurately. "
        "Your final answer MUST be the polished, fact-checked summary."
    ),
    expected_output="A polished and fact-checked final summary.",
    agent=editor,
)


crew = Crew(
    agents=[content_planner, paper_summarizer, editor],
    tasks=[fetch_transcript_task, content_planner_task, summarization_task, editing_task],
    process=Process.sequential,
)


if __name__ == '__main__':
    # url = input()
    result = crew.kickoff(inputs={'research_paper_link': "https://arxiv.org/pdf/1504.00113"})

    with open("research_paper_summary.md", "w", encoding="utf-8") as f:
        f.write(result.raw)