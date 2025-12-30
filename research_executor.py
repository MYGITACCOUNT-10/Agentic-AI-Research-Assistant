#For each sub-question, you must first find papers (evidence) — NOT answers.
# Then, based on the evidence, you can provide an answer.

# “From the already fetched papers, select which papers are relevant to each sub-question.”

from typing import List, Dict
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma


def execute_research(
    sub_questions: List[str],
    research_vector_db: Chroma,
    k: int = 3
) -> Dict[str, List[Document]]:
    """
    For each sub-question, retrieve relevant research papers (abstracts).

    Returns:
        {
          sub_question_1: [Document, Document, ...],
          sub_question_2: [Document, Document, ...]
        }
    """

    papers_per_subquestion = {}

    for sub_question in sub_questions:
        papers_per_subquestion[sub_question] = research_vector_db.similarity_search(
            sub_question,
            k=k
        )

    return papers_per_subquestion


# for key,value in list_of_papers_per_subquestion.items():
#     print(f"Sub-question: {key}")
#     for doc in value:
#         print(f"Title: {doc.metadata['title']}, arXiv ID: {doc.metadata['arxiv_id']}")
#     print("\n")
      

