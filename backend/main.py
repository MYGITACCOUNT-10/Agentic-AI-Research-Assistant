"""
backend/main.py
================
FastAPI application that exposes the Agentic Research Pipeline via REST API.

Architecture:
  Frontend (HTML/JS)  →  POST /research  →  run_research_pipeline()
                                              └── All agents (unchanged)

Run with:
  cd backend/
  uvicorn main:app --reload
"""

import sys
import os
import asyncio

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ---------------------------------------------------------------------------
# Path fix: add the project root to sys.path so we can import pipeline.py
# and all agent modules without moving any files.
# ---------------------------------------------------------------------------
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Import the orchestrating pipeline (all agents are called inside this)
from pipeline import run_research_pipeline  # noqa: E402

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Agentic Research Assistant API",
    description="REST API wrapper around the multi-agent arXiv research pipeline.",
    version="1.0.0",
)

# ---------------------------------------------------------------------------
# CORS — allow all origins so the plain HTML frontend (opened via file://)
# can reach the API without browser CORS errors.
# In production, restrict origins to your actual domain.
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Pydantic request schema
# ---------------------------------------------------------------------------
class ResearchRequest(BaseModel):
    """Schema for the POST /research request body."""
    question: str


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@app.get("/", tags=["Health"])
async def root():
    """Health-check endpoint."""
    return {"status": "ok", "message": "Agentic Research Assistant API is running."}


@app.post("/research", tags=["Research"])
async def run_research(request: ResearchRequest):
    """
    Run the full multi-agent research pipeline for the given question.

    - Fetches arXiv papers
    - Builds a Chroma vector DB
    - Classifies intent
    - Generates sub-questions
    - Retrieves and analyzes papers per sub-question
    - Verifies cross-paper agreement / disagreements / gaps
    - Synthesizes findings
    - Assembles final report

    Returns a JSON object with keys:
      intent, sub_questions, synthesis, report
    """
    question = request.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Research question cannot be empty.")

    try:
        # run_research_pipeline() is synchronous (blocking I/O + LLM calls).
        # We offload it to a thread pool so FastAPI's async event loop is not blocked.
        result = await asyncio.to_thread(run_research_pipeline, question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # The `report` field is a Pydantic ResearchReport model — serialize it to dict.
    # All other fields (intent: str, sub_questions: list, synthesis: dict[str,str])
    # are already JSON-serializable.
    serialized = {
        "intent": result["intent"],
        "sub_questions": result["sub_questions"],
        "synthesis": result["synthesis"],
        "report": result["report"].model_dump(),   # Pydantic v2
    }

    return serialized
