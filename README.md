# 📚 Agentic AI Research Assistant

> A production-style multi-agent research pipeline with a **FastAPI backend** and a **Vanilla JS frontend**, powered by arXiv, LangChain, ChromaDB, and Ollama (Mistral).

---

## 1. Overview

This project implements an agent-based research assistant that analyzes academic literature in a structured, systematic way. Given a research question, the system:

1. Retrieves relevant papers from **arXiv**
2. Builds a **semantic vector database** over paper abstracts
3. Classifies the **research intent**
4. Decomposes the question into **focused sub-questions**
5. Retrieves and **analyzes** papers per sub-question (RAG)
6. **Verifies** findings across papers (agreements / disagreements / gaps)
7. **Synthesizes** results into a structured research report

Each stage is a dedicated, independent agent — modular, testable, and extensible.

---

## 2. Architecture

```
┌─────────────────────────────────────────┐
│           Frontend (Vanilla JS)          │
│   index.html  ·  style.css  ·  script.js │
└──────────────────┬──────────────────────┘
                   │  POST /research (JSON)
                   ▼
┌─────────────────────────────────────────┐
│         FastAPI Backend (main.py)        │
│    CORS · Pydantic · asyncio.to_thread   │
└──────────────────┬──────────────────────┘
                   │  run_research_pipeline()
                   ▼
┌─────────────────────────────────────────────────────────────┐
│                   pipeline.py (Orchestrator)                  │
│                                                               │
│  arxiv_api_exploration  →  abstract_embedding_retrieval       │
│         ↓                           ↓                         │
│      intent.py              research_executor.py              │
│         ↓                           ↓                         │
│      planner.py              rag_retriever.py                 │
│                                     ↓                         │
│                          verification_agent.py                │
│                                     ↓                         │
│                           synthesis_agent.py                  │
│                                     ↓                         │
│                           report_assembler.py                 │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Key Capabilities

| Feature | Description |
|---|---|
| arXiv Retrieval | Fetches top-N papers via the arXiv API |
| Semantic Search | ChromaDB + HuggingFace `all-MiniLM-L6-v2` |
| Intent Classification | Categorises query: SUMMARY / COMPARISON / METHODS / LIMITATIONS / DATASETS |
| Sub-Question Planning | Breaks research question into 3–5 focused sub-questions |
| RAG Analysis | Per-sub-question abstract-level reasoning |
| Cross-Paper Verification | Identifies agreements, disagreements, and gaps |
| Synthesis | Coherent narrative per sub-question |
| Structured Report | Typed Pydantic output: overview · findings · limitations · conclusion |
| REST API | FastAPI — `POST /research`, CORS-enabled |
| Rich Frontend | Dark glassmorphism UI, no frameworks, no build step |

---

## 4. Repository Structure

```
Agentic-AI-Research-Assistant/
│
├── backend/
│   └── main.py                     FastAPI app — exposes POST /research
│
├── frontend/
│   ├── index.html                  Single-page UI shell
│   ├── style.css                   Dark glassmorphism theme (Inter font)
│   └── script.js                   fetch() API call + structured rendering
│
├── abstract_embedding_retrieval.py  Embedding & ChromaDB vector store
├── arxiv_api_exploration.py         arXiv API paper fetching
├── intent.py                        Research intent classification (Mistral)
├── planner.py                       Sub-question generation (Mistral)
├── research_executor.py             Per-sub-question retrieval
├── rag_retriever.py                 Abstract-level RAG analysis (Mistral)
├── verification_agent.py            Cross-paper verification (Mistral)
├── synthesis_agent.py               Reasoned synthesis (Mistral)
├── report_assembler.py              Structured Pydantic report assembly
├── pipeline.py                      End-to-end orchestrator
├── app.py                           Legacy Streamlit UI (still functional)
├── requirements.txt
└── README.md
```

---

## 5. Quick Start

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/) running locally with the **Mistral** model pulled:
  ```bash
  ollama pull mistral
  ```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the backend

```bash
cd backend
uvicorn main:app --reload
```

Backend starts at **http://localhost:8000**  
Interactive API docs: **http://localhost:8000/docs**

### Open the frontend

Simply open `frontend/index.html` in any modern browser (no build step needed).

---

## 6. API Reference

### `POST /research`

**Request**
```json
{
  "question": "Compare CNN and transformer based deepfake detection methods"
}
```

**Response**
```json
{
  "intent": "COMPARISON",
  "sub_questions": ["...", "...", "..."],
  "synthesis": {
    "sub_question_1": "synthesized paragraph...",
    "sub_question_2": "synthesized paragraph..."
  },
  "report": {
    "research_question": "...",
    "overview": "...",
    "detailed_findings": { "sub_question": "finding..." },
    "limitations": "...",
    "conclusion": "..."
  }
}
```

---

## 7. Core Design Principles

### Separation of Concerns
Backend (`main.py`) is purely a transport layer — it receives a question and returns a JSON response. All research logic lives in the pipeline and its agents.

### Pipeline as a First-Class Abstraction
`pipeline.py` is the single entry point for all research logic. It can be called from the FastAPI backend, the legacy Streamlit UI, scripts, or tests — without any modification.

### Structured Output Generation
Every agent produces typed output via Pydantic models. This eliminates ambiguity and makes the system's reasoning inspectable at each stage.

### Verification Before Synthesis
Papers are compared for agreements, disagreements, and gaps *before* synthesis. This prevents the LLM from producing overconfident summaries.

---

## 8. Tech Stack

| Layer | Technology |
|---|---|
| LLM | Ollama · Mistral (local, no API key needed) |
| Embeddings | `sentence-transformers/all-MiniLM-L6-v2` |
| Vector Store | ChromaDB |
| LLM Framework | LangChain (core · community · ollama · huggingface) |
| Backend | FastAPI · Uvicorn |
| Frontend | HTML5 · CSS3 · Vanilla JS |
| Paper Source | arXiv API (feedparser) |
| Schema | Pydantic v2 |
