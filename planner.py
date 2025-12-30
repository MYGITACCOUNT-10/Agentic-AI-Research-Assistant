#Input
# -->User question
# -->Intent (SUMMARY / COMPARISON / METHODS / etc.)
# Output
# -->A small list of research sub-questions
# Example
# -->User query:“Compare CNN and transformer based deepfake detection methods”
# Planner output:
# ---> What CNN-based approaches are used?
# ---> What transformer-based approaches are used?
# ---> What datasets are used for evaluation?
# ---> What are the performance differences?

from typing import List
from pydantic import BaseModel
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser


# Output schema
class PlanOutput(BaseModel):
    sub_questions: List[str]



# LLM + parser
parser = PydanticOutputParser(pydantic_object=PlanOutput)

llm = ChatOllama(
    model="mistral",
    temperature=0.4,
)

prompt = PromptTemplate(
    template="""
You are a research planning agent.

Your task is to break the main research question into
clear, atomic sub-questions that a researcher would investigate.

Intent of the question: {intent}

Rules:
- Generate 3 to 5 sub-questions
- Each sub-question must be specific
- Do NOT answer the questions
- Do NOT include explanations

{format_instructions}

MAIN QUESTION:
{query}
""",
    input_variables=["query", "intent"],
    partial_variables={
        "format_instructions": parser.get_format_instructions()
    }
)


# Planner function (PURE)
def generate_subquestions(query: str, intent: str) -> List[str]:
    """
    Generate research sub-questions from a main query and its intent.
    NO execution on import.
    """

    response = llm.invoke(
        prompt.format(query=query, intent=intent)
    )

    parsed = parser.parse(response.content)
    return parsed.sub_questions

# query = "Compare CNN and transformer based deepfake detection methods"


# for idx,sub_q in enumerate(list_of_subquestion):
#     print(f"Sub-question {idx+1}: {sub_q}")


