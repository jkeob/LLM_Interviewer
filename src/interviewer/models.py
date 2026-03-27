from pydantic import BaseModel, Field
from typing import List


class InterviewQuestions(BaseModel):
    reasoning_understanding_question: str
    relevant_capabilities_question: str
    limitations_question: str
    demo_task_question_1: str
    demo_task_question_2: str
    demo_task_question_3: str


class TaskRubric(BaseModel):
    task_id: str
    success_criteria: str


class ReferenceBlock(BaseModel):
    user_query: str
    intent_summary: str
    task_rubrics: List[TaskRubric]
    ideal_answer_rubric: str


class InterviewerOutput(BaseModel):
    agent_id: str
    interview: InterviewQuestions
    reference: ReferenceBlock
