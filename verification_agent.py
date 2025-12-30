# For each sub-question:
# Looks at multiple papers
# Identifies:
# common claims
# disagreements
# missing evidence
# Flags weak or unsupported claims
#-_-_-_-_-_-_-_-_-_-_-Example output format:-_-_-_-_-_-_-_-_-_-_-
# Agreements:
# - Most papers report CNN-based methods using X architecture
# Disagreements:
# - Paper A reports higher accuracy than Paper B
# Gaps:
# - Limited discussion on real-world robustness

# Every sub-question must own its own agreements, disagreements, and gaps.
# When I look at ALL these papers TOGETHER, what patterns exist?”

from typing import List
from pydantic import BaseModel, Field
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.documents import Document


# -----------------------------
# Output schema
# -----------------------------
class ResearchVerificationOutput(BaseModel):
    agreements: List[str] = Field(
        description="Claims supported by multiple documents"
    )
    disagreements: List[str] = Field(
        description="Conflicting findings across documents"
    )
    gaps: List[str] = Field(
        description="Missing or insufficiently studied aspects"
    )


# -----------------------------
# Parser + LLM
# -----------------------------
parser = PydanticOutputParser(
    pydantic_object=ResearchVerificationOutput
)

llm = ChatOllama(
    model="mistral",
    temperature=0.1
)


# -----------------------------
# Prompt
# -----------------------------
prompt = PromptTemplate(
    template="""
You are a research verification agent.

Analyze multiple research documents related to ONE sub-question.

Identify ONLY:
1. agreements
2. disagreements
3. gaps

Rules:
- Do NOT answer the sub-question
- Do NOT add external knowledge
- Do NOT infer unstated facts
- Base everything strictly on the documents

SUB-QUESTION:
{sub_question}

DOCUMENTS:
{documents}

{format_instructions}
""",
    input_variables=["sub_question", "documents"],
    partial_variables={
        "format_instructions": parser.get_format_instructions()
    }
)


# -----------------------------
# Verification function (PURE)
# -----------------------------
def verify_research(
    sub_question: str,
    documents: List[Document]
) -> ResearchVerificationOutput:
    """
    Verifies agreement, disagreement, and gaps
    across documents for ONE sub-question.
    """

    if not documents:
        return ResearchVerificationOutput(
            agreements=[],
            disagreements=[],
            gaps=["No documents available for verification."]
        )

    context = "\n\n".join(
        f"Title: {doc.metadata.get('title', 'N/A')}\n"
        f"arXiv ID: {doc.metadata.get('arxiv_id', 'N/A')}\n"
        f"Abstract: {doc.page_content}"
        for doc in documents
    )

    response = llm.invoke(
        prompt.format(
            sub_question=sub_question,
            documents=context
        )
    )

    return parser.parse(response.content)


   
# print(verification_result)



# verification_results = {
#     sub_question_1: ResearchVerificationOutput(
#         agreements=[...],
#         disagreements=[...],
#         gaps=[...]
#     ),
#     sub_question_2: ResearchVerificationOutput(
#         agreements=[...],
#         disagreements=[...],
#         gaps=[...]
#     ),
# }
