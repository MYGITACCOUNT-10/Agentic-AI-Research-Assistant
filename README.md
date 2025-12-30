Agentic AI Research Assistant

A Modular, Agent-Based System for Automated Literature Analysis

1. Overview

This repository implements an agentic research assistant that performs structured literature analysis over arXiv papers using a multi-stage, agent-based pipeline.

Rather than functioning as a conversational chatbot, the system models research as a reproducible workflow in which each stage—retrieval, planning, verification, and synthesis—is handled by a dedicated agent with a clearly defined responsibility.

The project emphasizes modular design, explainability, and structured outputs suitable for research and system-level evaluation.

2. Key Capabilities

Automated retrieval of relevant research papers from arXiv

Research intent classification based on user query

Decomposition of the research objective into sub-questions

Vector-based retrieval over paper abstracts using RAG

Cross-paper verification identifying agreements, disagreements, and gaps

Reasoned synthesis of findings across multiple sources

Generation of a structured research report using typed data models

Optional Streamlit-based interface for paper inspection and result visualization

3. System Architecture

The system follows a deterministic, multi-stage research workflow:

User Query
   ↓
arXiv Paper Retrieval
   ↓
Embedding and Vector Database Construction
   ↓
Intent Classification
   ↓
Sub-Question Planning
   ↓
RAG-Based Retrieval per Sub-Question
   ↓
Verification Across Papers
   ↓
Synthesis of Findings
   ↓
Structured Research Report


Each stage is implemented as an independent module, enabling isolation, testing, and future extensibility.

4. Repository Structure
.
├── frontend/                       Optional Streamlit interface
│   └── app.py
├── screenshots/                    UI screenshots for documentation
├── abstract_embedding_retrieval.py Embedding and vector database construction
├── arxiv_api_exploration.py        arXiv paper retrieval logic
├── intent.py                       Research intent classification
├── planner.py                      Sub-question generation
├── research_executor.py            Retrieval per sub-question
├── rag_retriever.py                Abstract-level RAG analysis
├── verification_agent.py           Cross-paper verification
├── synthesis_agent.py              Reasoned synthesis
├── report_assembler.py             Structured report generation
├── pipeline.py                     End-to-end research pipeline
├── workflow_graph.ipynb            Workflow visualization and experimentation
├── requirements.txt
└── README.md

5. Core Design Principles
5.1 Separation of Concerns

Each agent is responsible for a single research function, reducing coupling and improving explainability.

5.2 Pipeline as a First-Class Abstraction

The research workflow is explicitly defined in run_research_pipeline, ensuring deterministic execution and reproducibility.

5.3 Structured Output

The final research artifact is a typed object rather than unstructured text. This enables validation, serialization, and downstream integration.

5.4 Verification Before Synthesis

Findings are verified across multiple papers before synthesis, aligning with standard academic literature review practices.

6. Example Usage
from pipeline import run_research_pipeline

result = run_research_pipeline(
    "Deep fake image detection"
)

print(result["report"])

7. Frontend (Optional)

A Streamlit-based interface is included for optional visualization purposes. It allows users to inspect retrieved papers, read abstracts, and view the final structured report.

The frontend is intentionally treated as a secondary component. The primary contribution of this project lies in the agentic research pipeline and reasoning workflow.

8. Limitations

Analysis is restricted to abstract-level information

Full-paper PDF parsing is not included

Experimental metrics are not extracted

arXiv retrieval relies on keyword-based search

These limitations are explicitly acknowledged and represent areas for future extension.

9. Future Extensions

Full-paper PDF parsing and section-level analysis

Semantic re-ranking of retrieved papers

Citation and influence graph analysis

Persistent research memory across sessions

Human-in-the-loop verification

Extended orchestration using LangGraph

10. Technology Stack

Python 3.10 or higher

Pydantic for structured data modeling

arXiv API for literature retrieval

Vector databases such as FAISS or Chroma

Large language models for reasoning and synthesis

Streamlit for optional visualization

LangGraph for optional orchestration
