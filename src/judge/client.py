"""
JudgeClient
-----------
Scores agent responses against the reference block using the same vllm instance.
Takes InterviewerOutput + AgentResponses, returns JudgeOutput.
"""

import json
import requests
from src.judge.prompt import SYSTEM_PROMPT
from src.judge.models import JudgeOutput
from src.interviewer.models import InterviewerOutput
from src.checker.models import AgentResponses


class JudgeClient:
    def __init__(self, base_url: str = "http://localhost:8000/v1", model: str = "Qwen/Qwen3-30B-A3B-Instruct-2507"):
        self.base_url = base_url.rstrip("/")
        self.model = model

    def run(self, interview: InterviewerOutput, responses: AgentResponses) -> JudgeOutput:
        user_content = self._build_user_content(interview, responses)

        payload = {
            "model": self.model,
            "max_tokens": 1024,
            "temperature": 0.1,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_content},
            ],
        }

        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=300,
        )
        response.raise_for_status()

        body = response.json()
        text = body["choices"][0]["message"]["content"].strip()
        data = json.loads(text)

        return JudgeOutput.model_validate(data)

    def _build_user_content(self, interview: InterviewerOutput, responses: AgentResponses) -> str:
        q = interview.interview
        r = responses
        ref = interview.reference

        # build task rubric lookup
        rubric_map = {tr.task_id: tr.success_criteria for tr in ref.task_rubrics}

        content = f"USER QUERY:\n{ref.user_query}\n\n"
        content += f"AGENT ID:\n{interview.agent_id}\n\n"

        content += "--- REASONING QUESTIONS AND RESPONSES ---\n\n"

        content += f"Q: {q.reasoning_understanding_question}\n"
        content += f"A: {r.reasoning_understanding_response}\n\n"

        content += f"Q: {q.relevant_capabilities_question}\n"
        content += f"A: {r.relevant_capabilities_response}\n\n"

        content += f"Q: {q.limitations_question}\n"
        content += f"A: {r.limitations_response}\n\n"

        content += "--- DEMO TASKS AND RESPONSES ---\n\n"

        content += f"TASK 1: {q.demo_task_question_1}\n"
        content += f"RESPONSE: {r.demo_task_response_1}\n"
        content += f"SUCCESS CRITERIA: {rubric_map.get('demo_task_question_1', '')}\n\n"

        content += f"TASK 2: {q.demo_task_question_2}\n"
        content += f"RESPONSE: {r.demo_task_response_2}\n"
        content += f"SUCCESS CRITERIA: {rubric_map.get('demo_task_question_2', '')}\n\n"

        content += f"TASK 3: {q.demo_task_question_3}\n"
        content += f"RESPONSE: {r.demo_task_response_3}\n"
        content += f"SUCCESS CRITERIA: {rubric_map.get('demo_task_question_3', '')}\n\n"

        content += f"--- IDEAL ANSWER RUBRIC FOR REASONING QUESTIONS ---\n{ref.ideal_answer_rubric}\n\n"

        content += "Return JSON only. Score each response 0-5. Total must equal the sum of all six scores."

        return content
