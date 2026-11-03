"""Dependency-free manager/specialist lab with explicit result contracts.

Run from the repository root: python AgenticAI/labs/multi_agent_demo.py
This is a deterministic orchestration demonstration, not a multi-LLM system.
"""

from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass
from typing import Protocol


@dataclass(frozen=True)
class Finding:
    agent: str
    status: str
    summary: str
    evidence_ids: tuple[str, ...] = ()
    requires_approval: bool = False
    limitations: tuple[str, ...] = ()


class Specialist(Protocol):
    name: str

    def run(self, question: str) -> Finding:
        """Return a bounded, typed finding for the coordinator."""


class PolicyResearcher:
    name = "policy_researcher"

    def run(self, question: str) -> Finding:
        if "refund" not in question.casefold():
            return Finding(
                self.name,
                "no_evidence",
                "The demo corpus has no matching refund-policy answer.",
                limitations=("No live policy lookup is configured.",),
            )
        return Finding(
            self.name,
            "complete",
            "The demo policy says refund actions should be checked against current eligibility rules.",
            evidence_ids=("POLICY-DEMO-01",),
            limitations=("Teaching fixture only; not a real policy or customer entitlement.",),
        )


class SafetyReviewer:
    name = "safety_reviewer"

    def run(self, question: str) -> Finding:
        asks_to_execute = any(
            term in question.casefold()
            for term in ("issue", "send", "process", "execute", "approve", "pay")
        )
        needs_approval = "refund" in question.casefold() and asks_to_execute
        return Finding(
            self.name,
            "complete",
            "A refund is a financial side effect; do not execute from this demo."
            if needs_approval else "No financial write was requested in this demo question.",
            requires_approval=needs_approval,
            limitations=("This reviewer uses a transparent demo rule, not a production policy engine.",),
        )


@dataclass(frozen=True)
class CoordinatorResult:
    answer: str
    status: str
    findings: tuple[Finding, ...]


class Coordinator:
    def __init__(self, specialists: tuple[Specialist, ...] | None = None) -> None:
        self.specialists = specialists or (PolicyResearcher(), SafetyReviewer())

    def run(self, question: str) -> CoordinatorResult:
        if not question.strip():
            raise ValueError("Question must not be empty.")
        # These specialists are independent in this example. In production, only
        # parallelize when dependencies, privacy, and budget allow it.
        with ThreadPoolExecutor(max_workers=len(self.specialists)) as pool:
            futures = [pool.submit(agent.run, question) for agent in self.specialists]
            findings = tuple(future.result() for future in futures)

        research = next((item for item in findings if item.agent == "policy_researcher"), None)
        reviewer = next((item for item in findings if item.agent == "safety_reviewer"), None)
        if research is None or research.status != "complete":
            answer = "I cannot confirm this from the demo evidence. No action was taken."
            status = "insufficient_evidence"
        elif reviewer is not None and reviewer.requires_approval:
            answer = f"{research.summary} A human approval and current eligibility check are required before any refund. No refund was issued."
            status = "approval_required"
        else:
            answer = f"{research.summary} This lab only returns a finding; it does not perform a refund."
            status = "complete"
        return CoordinatorResult(answer, status, findings)


def main() -> None:
    coordinator = Coordinator()
    for question in (
        "What does the refund policy say?",
        "Please issue the refund now.",
        "What is the password reset process?",
    ):
        result = coordinator.run(question)
        print(f"\nQUESTION: {question}")
        print(json.dumps(asdict(result), indent=2))


if __name__ == "__main__":
    main()
