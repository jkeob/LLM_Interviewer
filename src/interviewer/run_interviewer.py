import json
from pathlib import Path
from src.interviewer.client import InterviewerClient


def main() -> None:
    manifest = json.loads(Path("manifests/sample_manifest.json").read_text())

    user_query = (
        "I need an agent that can summarize long research transcripts, "
        "stay grounded in provided documents, and clearly state limitations."
    )

    client = InterviewerClient()
    result = client.run(user_query=user_query, manifest=manifest)
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
