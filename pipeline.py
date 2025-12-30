from arxiv_api_exploration import fetch_arxiv_papers
from abstract_embedding_retrieval import build_vector_db
from intent import classify_intent
from planner import generate_subquestions
from research_executor import execute_research
from rag_retriever import analyze_subquestion
from verification_agent import verify_research
from synthesis_agent import synthesize_subquestion
from report_assembler import assemble_report


def run_research_pipeline(research_question: str):
    # 1. Fetch papers
    papers = fetch_arxiv_papers(research_question, max_results=5)

    # 2. Build vector DB
    vector_db = build_vector_db(papers)

    # 3. Intent
    intent = classify_intent(research_question)

    # 4. Planning
    sub_questions = generate_subquestions(research_question, intent)


    # 5. Retrieval
    papers_per_subq = execute_research(sub_questions, vector_db)

    # 6. RAG analysis (paper-level understanding)
    analysis_results = {}
    for sq, docs in papers_per_subq.items():
        analysis_results[sq] = analyze_subquestion(sq, docs)

    # 7. Verification (cross-paper comparison)
    verification_results = {}
    for sq, docs in papers_per_subq.items():
        verification_results[sq] = verify_research(sq, docs)

    # 8. Synthesis (reasoned summary)
    synthesis_results = {}
    for sq, v in verification_results.items():
        synthesis_results[sq] = synthesize_subquestion(
        sub_question=sq,
        agreements=v.agreements,
        disagreements=v.disagreements,
        gaps=v.gaps
    )
        
    # 9. Assemble report
    report = assemble_report(research_question, synthesis_results)

    return {
        "intent": intent,
        "sub_questions": sub_questions,
        "synthesis": synthesis_results,
        "report": report
    }
