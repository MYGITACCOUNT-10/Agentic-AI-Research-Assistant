from typing import List
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate



# LLM
llm = ChatOllama(
    model="mistral",
    temperature=0.4
)


# Prompt
prompt = PromptTemplate(
    template="""
You are a research synthesis agent.

Your task is to synthesize verified research findings for ONE sub-question.

You are given:
- Agreements: claims supported by multiple documents
- Disagreements: conflicting or varying findings
- Gaps: aspects insufficiently addressed in the literature

Instructions:
- Integrate the information into a single coherent synthesis
- Do NOT add new facts or external knowledge
- Do NOT invent metrics or results
- Use cautious, research-appropriate language
- Focus on patterns, variability, and limitations

SUB-QUESTION:
{sub_question}

AGREEMENTS:
{agreements}

DISAGREEMENTS:
{disagreements}

GAPS:
{gaps}

Write a concise synthesis paragraph based ONLY on the above information.
""",
    input_variables=["sub_question", "agreements", "disagreements", "gaps"],
)


# -----------------------------
# Synthesis function (PURE)
# -----------------------------
def synthesize_subquestion(
    sub_question: str,
    agreements: List[str],
    disagreements: List[str],
    gaps: List[str]
) -> str:
    """
    Synthesizes verified findings for ONE sub-question.
    """

    response = llm.invoke(
        prompt.format(
            sub_question=sub_question,
            agreements="\n".join(f"- {a}" for a in agreements),
            disagreements="\n".join(f"- {d}" for d in disagreements),
            gaps="\n".join(f"- {g}" for g in gaps),
        )
    )

    return response.content

    

# --------EXAMPLE USAGE -------#
