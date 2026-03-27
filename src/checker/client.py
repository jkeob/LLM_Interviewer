import requests
from src.interviewer.models import InterviewerOutput
from src.checker.models import AgentResponses


class CheckerClient:
    def __init__(self, timeout: int = 120):
        self.timeout = timeout

    def run(self, interview: InterviewerOutput, manifest: dict) -> AgentResponses:
        endpoint = self._get_endpoint(manifest)

        questions = interview.interview

        return AgentResponses(
            agent_id=interview.agent_id,
            reasoning_understanding_response=self._ask(endpoint, questions.reasoning_understanding_question),
            relevant_capabilities_response=self._ask(endpoint, questions.relevant_capabilities_question),
            limitations_response=self._ask(endpoint, questions.limitations_question),
            demo_task_response_1=self._ask(endpoint, questions.demo_task_question_1),
            demo_task_response_2=self._ask(endpoint, questions.demo_task_question_2),
            demo_task_response_3=self._ask(endpoint, questions.demo_task_question_3),
        )

    def _ask(self, endpoint: str, message: str) -> str:
        response = requests.post(
            endpoint,
            headers={"Content-Type": "application/json"},
            json={"message": message},
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()["response"]

    def _get_endpoint(self, manifest: dict) -> str:
        bindings = manifest.get("protocol_bindings", [])
        for binding in bindings:
            if binding.get("protocol") == "http":
                return binding["endpoint"]
        raise ValueError("No HTTP protocol binding found in manifest")
