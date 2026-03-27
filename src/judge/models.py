from pydantic import BaseModel, Field
from typing import List


class QuestionScore(BaseModel):
    question_id: str
    score: int = Field(..., ge=0, le=5)
    justification: str


class JudgeOutput(BaseModel):
    agent_id: str
    scores: List[QuestionScore]
    total_score: int = Field(..., ge=0, le=30)
    verdict: str
