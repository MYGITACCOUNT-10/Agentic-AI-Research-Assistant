# “Which papers (abstracts) are relevant to this specific sub-question?”
# Abstract-level retrieval is for trends, agreement, disagreement, and gaps — NOT exact answers.

# # “Given these papers, read their abstracts and reason about them for ONE sub-question.”
# Given these abstracts, what information relevant to THIS sub-question is stated?”
from typing import List
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document


# -----------------------------
# LLM
# -----------------------------
llm = ChatOllama(
    model="mistral",
    temperature=0.2,
    max_tokens=800
)


# -----------------------------
# Prompt
# -----------------------------
prompt = PromptTemplate(
    template="""
You are an academic research assistant.

Use ONLY the information in the provided abstracts.
Do NOT add external knowledge.
If the answer is not present, say "Not found in the given papers".

ABSTRACTS:
{context}

SUB-QUESTION:
{sub_question}

RESPONSE:
""",
    input_variables=["context", "sub_question"]
)



# Analyzer function (PURE)
def analyze_subquestion(
    sub_question: str,
    documents: List[Document]
) -> str:
    """
    Runs controlled analysis for ONE sub-question
    using ONLY its corresponding papers.
    """

    if not documents:
        return "No relevant papers retrieved for this sub-question."

    context = "\n\n".join(
        f"Title: {doc.metadata.get('title', 'N/A')}\n"
        f"arXiv ID: {doc.metadata.get('arxiv_id', 'N/A')}\n"
        f"Abstract: {doc.page_content}"
        for doc in documents
    )

    response = llm.invoke(
        prompt.format(
            sub_question=sub_question,
            context=context
        )
    )

    return response.content

