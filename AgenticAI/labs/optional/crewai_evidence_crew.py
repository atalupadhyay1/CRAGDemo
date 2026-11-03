"""Optional CrewAI sequential crew using only learner-supplied evidence.

Install CrewAI and configure a provider before running; for example:
  python -m pip install crewai
  export OPENAI_API_KEY=...  # keep secrets out of source control and chat
  python AgenticAI/labs/optional/crewai_evidence_crew.py

This is a framework integration exercise, not a claim that model output is verified.
"""

from __future__ import annotations

import os

from crewai import Agent, Crew, Process, Task


QUESTION = "What must happen before a refund is issued?"
EVIDENCE = (
    "POLICY-01: A human must approve a financial refund before execution. "
    "The current customer-specific eligibility has not been checked."
)


def build_crew() -> Crew:
    model = os.getenv("COURSE_LLM", "openai/gpt-4o-mini")
    analyst = Agent(
        role="Evidence Analyst",
        goal="Extract only claims directly supported by the supplied evidence",
        backstory="You are careful, cite source IDs, and identify missing facts rather than guessing.",
        llm=model,
        allow_delegation=False,
        verbose=False,
    )
    reviewer = Agent(
        role="Safety Reviewer",
        goal="Check that the draft does not claim an action occurred or bypass approval",
        backstory="You review high-impact actions conservatively and report the exact limitation.",
        llm=model,
        allow_delegation=False,
        verbose=False,
    )
    analysis_task = Task(
        description=(
            "Answer this question using only the supplied evidence. Cite its source ID. "
            "If a necessary fact is missing, say so.\nQuestion: {question}\nEvidence: {evidence}"
        ),
        expected_output="A short finding with source ID and any missing facts.",
        agent=analyst,
    )
    review_task = Task(
        description=(
            "Review the previous finding. Do not invent policy or claim a refund was issued. "
            "State the approval gate and the missing eligibility check."
        ),
        expected_output="A safety-reviewed answer with a clear no-action statement.",
        agent=reviewer,
        context=[analysis_task],
    )
    return Crew(
        agents=[analyst, reviewer],
        tasks=[analysis_task, review_task],
        process=Process.sequential,
        verbose=False,
    )


def main() -> None:
    if not os.getenv("OPENAI_API_KEY") and os.getenv("COURSE_LLM", "openai/gpt-4o-mini").startswith("openai/"):
        raise SystemExit("Set a provider credential securely, or choose a configured COURSE_LLM provider.")
    result = build_crew().kickoff(inputs={"question": QUESTION, "evidence": EVIDENCE})
    print(result)
    print("\nReview the trace and source grounding; model output is not an authorization decision.")


if __name__ == "__main__":
    main()
