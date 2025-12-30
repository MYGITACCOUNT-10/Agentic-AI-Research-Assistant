## 1. Overview

This project implements an agent-based research assistant that helps analyze academic literature in a structured and systematic way. Instead of treating research as a conversational task, the system models it as a clear, step-by-step workflow, similar to how a human researcher would approach a literature review.

Given a research question, the system retrieves relevant papers from arXiv, identifies the intent of the query, breaks the problem into smaller sub-questions, and analyzes the literature for each sub-question. It then compares findings across multiple papers to identify areas of agreement, disagreement, and gaps before synthesizing the results into a consolidated report.

Each stage of this process is handled by a dedicated agent with a specific responsibility. This design keeps the system modular and transparent, making it easier to understand how conclusions are formed and how individual components contribute to the final outcome.

Rather than producing a free-form text response, the system generates a structured research report that includes synthesized findings, limitations, and conclusions in a consistent, machine-readable format. This makes the output easier to inspect, validate, and reuse.

Overall, the project demonstrates how agent-based system design can be applied to research-oriented tasks, emphasizing clarity, reproducibility, and thoughtful reasoning over surface-level interaction.

---

## 2. Key Capabilities

* Automated retrieval of relevant research papers from arXiv
* Research intent classification based on user queries
* Decomposition of research objectives into focused sub-questions
* Vector-based retrieval over paper abstracts using Retrieval-Augmented Generation (RAG)
* Cross-paper verification identifying agreements, disagreements, and gaps
* Reasoned synthesis of findings across multiple sources
* Generation of a structured research report using typed data models
* Optional Streamlit-based interface for paper inspection and result visualization

---

## 3. System Architecture

The system follows a deterministic, multi-stage research workflow:

```
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
```

Each stage is implemented as an independent module, enabling isolation, testing, and future extensibility.

---

## 4. Repository Structure

```
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
```

---

## 5. Core Design Principles

### 5.1 Separation of Concerns

Each agent is responsible for a single research function. This design reduces coupling between components and improves explainability, maintainability, and testability.

---

### 5.2 Pipeline as a First-Class Abstraction

The complete research workflow is explicitly defined within a single pipeline function. This ensures deterministic execution, reproducibility of results, and clarity in system behavior.

---

### 5.3 Structured Output Generation

The final research output is produced as a structured, typed object rather than free-form text. This enables validation, serialization, and seamless downstream integration.

---

### 5.4 Verification Before Synthesis

Findings from individual papers are verified and compared before synthesis. Agreements, disagreements, and gaps are explicitly identified prior to generating consolidated insights, aligning the system with standard academic literature review practices.

---
