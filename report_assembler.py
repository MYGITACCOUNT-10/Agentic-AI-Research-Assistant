from typing import Dict
from pydantic import BaseModel

class ResearchReport(BaseModel):
    research_question: str
    overview: str
    detailed_findings: Dict[str, str]
    limitations: str
    conclusion: str


# Static assembler texts
OVERVIEW_TEXT = (
    "This report presents an abstract-level literature analysis of the given research question. "
    "Relevant research papers were retrieved using semantic similarity over paper abstracts. "
    "The literature was analyzed per research sub-question, verified for agreement, disagreement, "
    "and gaps, and synthesized into structured findings."
)

LIMITATIONS_TEXT = (
    "This analysis is limited to abstract-level information and does not include full-paper examination. "
    "As a result, detailed experimental setups, exact performance metrics, and fine-grained "
    "methodological comparisons are not always available. Several sub-questions could not be fully "
    "answered due to insufficient reporting within abstracts."
)

CONCLUSION_TEXT = (
    "Overall, the reviewed literature reflects active research efforts in the given domain. "
    "While abstracts provide useful insight into research directions and general findings, "
    "the lack of standardized and explicit reporting limits detailed comparison. "
    "The results highlight both current research trends and areas where deeper, "
    "full-paper analysis is required."
)

# Report assembler (PURE FUNCTION)

def assemble_report(
    research_question: str,
    synthesis_per_subquestion: Dict[str, str]
) -> ResearchReport:
    """
    Assemble the final research report from synthesized sub-question outputs.
    NO execution. NO imports of computed data.
    """

    return ResearchReport(
        research_question=research_question,
        overview=OVERVIEW_TEXT,
        detailed_findings=synthesis_per_subquestion,
        limitations=LIMITATIONS_TEXT,
        conclusion=CONCLUSION_TEXT
    )
