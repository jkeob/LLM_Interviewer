import json
import requests
from src.interviewer.prompt import SYSTEM_PROMPT
from src.interviewer.models import InterviewerOutput


class InterviewerClient:
    def __init__(self, base_url: str = "http://localhost:8000/v1", model: str = "Qwen/Qwen3-30B-A3B-Instruct-2507"):
        self.base_url = base_url.rstrip("/")
        self.model = model

    def run(self, user_query: str, manifest: dict) -> InterviewerOutput:
        user_content = (
            f"USER QUERY:\n{user_query}\n\n"
            f"AGENT MANIFEST JSON:\n{json.dumps(manifest, indent=2)}\n\n"
            "Return JSON only."
        )

        payload = {
            "model": self.model,
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

        return InterviewerOutput.model_validate(data)
