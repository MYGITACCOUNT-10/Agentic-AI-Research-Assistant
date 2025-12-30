#“What kind of research thinking does this question require?”
# Your system should answer this question before doing anything else:
# “What kind of research question is this?”
# Because:
# Summary questions ≠ comparison questions
# Methods ≠ limitations
# Later → different agents / workflows
from typing import Literal
from typing import Union, List, Literal
from pydantic import BaseModel
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

class IntentOutput(BaseModel):
    intent: Union[
        Literal["SUMMARY", "COMPARISON", "METHODS", "LIMITATIONS", "DATASETS"],
        List[Literal["SUMMARY", "COMPARISON", "METHODS", "LIMITATIONS", "DATASETS"]]
    ]



parser = PydanticOutputParser(pydantic_object=IntentOutput)

llm = ChatOllama(model="mistral", temperature=0.0)

prompt = PromptTemplate(
    template="""
Classify the research question into EXACTLY ONE intent.
{format_instructions}

QUESTION:
{query}
""",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)


def classify_intent(query: str) -> str:
    response = llm.invoke(prompt.format(query=query))
    parsed = parser.parse(response.content)

    intent = parsed.intent


    if isinstance(intent, list):
        intent = intent[0]

    return intent

