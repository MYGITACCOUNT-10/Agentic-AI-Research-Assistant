from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, START, END

from arxiv_api_exploration import fetch_arxiv_papers
from abstract_embedding_retrieval import build_vector_db
from intent import classify_intent
from planner import generate_subquestions
from research_executor import execute_research
from rag_retriever import analyze_subquestion
from verification_agent import verify_research
from synthesis_agent import synthesize_subquestion
from report_assembler import assemble_report
from database import save_report_to_db

# -------------------- LangGraph State Definition --------------------

class ResearchState(TypedDict):
    research_question: str
    papers: List[Any]
    vector_db: Any
    intent: str
    sub_questions: List[str]
    papers_per_subq: Dict[str, Any]
    analysis_results: Dict[str, Any]
    verification_results: Dict[str, Any]
    synthesis_results: Dict[str, Any]
    report: str

# -------------------- LangGraph Nodes --------------------

def node_fetch_papers(state: ResearchState):
    papers = fetch_arxiv_papers(state["research_question"], max_results=5)
    return {"papers": papers}

def node_build_db(state: ResearchState):
    vector_db = build_vector_db(state["papers"])
    return {"vector_db": vector_db}

def node_planning(state: ResearchState):
    intent = classify_intent(state["research_question"])
    sub_questions = generate_subquestions(state["research_question"], intent)
    return {"intent": intent, "sub_questions": sub_questions}

def node_retrieval(state: ResearchState):
    papers_per_subq = execute_research(state["sub_questions"], state["vector_db"])
    return {"papers_per_subq": papers_per_subq}

def node_analysis(state: ResearchState):
    analysis_results = {}
    for sq, docs in state["papers_per_subq"].items():
        analysis_results[sq] = analyze_subquestion(sq, docs)
    return {"analysis_results": analysis_results}

def node_verification(state: ResearchState):
    verification_results = {}
    for sq, docs in state["papers_per_subq"].items():
        verification_results[sq] = verify_research(sq, docs)
    return {"verification_results": verification_results}

def node_synthesis(state: ResearchState):
    synthesis_results = {}
    for sq, v in state["verification_results"].items():
        synthesis_results[sq] = synthesize_subquestion(
            sub_question=sq,
            agreements=v.agreements,
            disagreements=v.disagreements,
            gaps=v.gaps
        )
    return {"synthesis_results": synthesis_results}

def node_assembly(state: ResearchState):
    report = assemble_report(state["research_question"], state["synthesis_results"])
    
    # Securely save to PostgreSQL
    save_report_to_db(
        query=state["research_question"],
        intent=state.get("intent", "general"),
        sub_questions=state.get("sub_questions", []),
        synthesis=state.get("synthesis_results", {}),
        report_text=report
    )
    
    return {"report": report}

# -------------------- LangGraph Orchestration --------------------

workflow = StateGraph(ResearchState)

workflow.add_node("fetch_papers", node_fetch_papers)
workflow.add_node("build_db", node_build_db)
workflow.add_node("planning", node_planning)
workflow.add_node("retrieval", node_retrieval)
workflow.add_node("analysis", node_analysis)
workflow.add_node("verification", node_verification)
workflow.add_node("synthesis", node_synthesis)
workflow.add_node("assembly", node_assembly)

workflow.add_edge(START, "fetch_papers")
workflow.add_edge("fetch_papers", "build_db")
workflow.add_edge("build_db", "planning")
workflow.add_edge("planning", "retrieval")
workflow.add_edge("retrieval", "analysis")
workflow.add_edge("analysis", "verification")
workflow.add_edge("verification", "synthesis")
workflow.add_edge("synthesis", "assembly")
workflow.add_edge("assembly", END)

research_app = workflow.compile()

# -------------------- Public API --------------------

def run_research_pipeline(research_question: str):
    """
    Executes the multi-agent LangGraph workflow.
    """
    final_state = research_app.invoke({"research_question": research_question})
    return {
        "intent": final_state["intent"],
        "sub_questions": final_state["sub_questions"],
        "synthesis": final_state["synthesis_results"],
        "report": final_state["report"]
    }
