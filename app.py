from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
from research_paper_summarizer import crew

app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict to your frontend later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SummarizeRequest(BaseModel):
    research_paper_link: str
    
@app.get("/")
def home():
    return {"message": "Research Paper summarizer API is running"}


@app.post("/summarize")
async def summarize(req: SummarizeRequest):
    try:
        result = crew.kickoff(inputs={'research_paper_link': req.research_paper_link})
        return {"summary": result.raw}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
