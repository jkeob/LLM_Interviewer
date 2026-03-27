"""
Orchestrator
------------
Chains the full LMAJ pipeline:
  1. Start vllm server
  2. Run interviewer — generates questions + reference block
  3. Run checker — hits agent endpoint with each question, collects responses
  4. Run judge — scores responses against reference block
  5. Print final evaluation
  6. Stop vllm server
"""

import json
from pathlib import Path

from src.interviewer.client import InterviewerClient
from src.interviewer.server import start, stop
from src.checker.client import CheckerClient
from src.judge.client import JudgeClient


def main():
    # load manifest
    manifest = json.loads(Path("stub_agent/manifest.json").read_text())

    user_query = (
        "I need an agent that can handle a wide range of tasks from code generation to email generation. "
        "For example, I want to be able to have the agent find issues in my code, find the bug, and fix "
        "the code so it runs properly without errors. I also want it to be able to craft emails to any "
        "one of my contacts."
    )

    start()

    try:
        # step 1 — interviewer generates questions + reference block
        print("\n[orchestrator] running interviewer...")
        interviewer = InterviewerClient()
        interview = interviewer.run(user_query=user_query, manifest=manifest)
        print("[orchestrator] interview generated")
        print(interview.model_dump_json(indent=2))

        # step 2 — checker hits agent with each question and collects responses
        print("\n[orchestrator] running checker...")
        checker = CheckerClient()
        responses = checker.run(interview=interview, manifest=manifest)
        print("[orchestrator] responses collected")
        print(responses.model_dump_json(indent=2))

        # step 3 — judge scores responses against reference block
        print("\n[orchestrator] running judge...")
        judge = JudgeClient()
        result = judge.run(interview=interview, responses=responses)
        print("[orchestrator] evaluation complete")

        # print final result
        print("\n" + "=" * 72)
        print("FINAL EVALUATION")
        print("=" * 72)
        print(f"Agent:       {result.agent_id}")
        print(f"Total Score: {result.total_score} / 30")
        print(f"\nVerdict:\n{result.verdict}")
        print("\nScore Breakdown:")
        for s in result.scores:
            print(f"  [{s.score}/5] {s.question_id}")
            print(f"         {s.justification}")
        print("=" * 72)

    finally:
        stop()


if __name__ == "__main__":
    main()
