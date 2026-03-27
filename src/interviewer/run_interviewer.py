import json
from pathlib import Path
from src.interviewer.client import InterviewerClient


def main() -> None:
        manifest = json.loads(Path("manifests/sample_manifest.json").read_text())

        user_query = (
            "I need an agent that can handle a wide range of tasks from code generation to email generation, "
            "For example, I want to be able to have the agent find issues in my code, find the bug, and fix the code so it runs properly without errors. I also want it to be able to craft emails to any one of contacts."
        )

        client = InterviewerClient()
        result = client.run(user_query=user_query, manifest=manifest)
        print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
