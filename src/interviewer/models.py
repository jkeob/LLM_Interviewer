from pydantic import BaseModel, Field
from typing import List


class InterviewQuestions(BaseModel):
    task_understanding_question: str
    relevant_capabilities_question: str
    approach_question: str
    micro_demo_question: str
    limitations_question: str


class ReferenceBlock(BaseModel):
    user_query: str
    intent_summary: str
    success_criteria: List[str] = Field(default_factory=list)
    ideal_answer_rubric: str


class InterviewerOutput(BaseModel):
    agent_id: str
    interview: InterviewQuestions
    reference: ReferenceBlock
