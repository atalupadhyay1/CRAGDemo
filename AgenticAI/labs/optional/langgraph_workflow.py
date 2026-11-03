"""A deterministic LangGraph that retrieves, rewrites once, then answers or abstains.

Install the optional dependency with: python -m pip install langgraph
Run from the repository root: python AgenticAI/labs/optional/langgraph_workflow.py
No model API key is required; the fixed corpus is a teaching fixture.
"""

from __future__ import annotations

import re
from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph


CORPUS = [
    {
        "id": "POLICY-01",
        "text": "Refunds require a current eligibility check. A human must approve a financial refund before execution.",
    },
    {
        "id": "POLICY-02",
        "text": "Support agents may search the approved runbook and draft a response, but must not invent missing policy facts.",
    },
]
STOP_WORDS = {"a", "an", "and", "are", "for", "how", "is", "me", "of", "the", "to", "what", "when", "must"}
SYNONYMS = {"reimburse": "refund", "reimbursement": "refund", "authorize": "approval", "authorization": "approval"}


class CourseState(TypedDict):
    original_question: str
    query: str
    attempts: int
    evidence: list[dict[str, str]]
    answer: str
    status: str


def terms(text: str) -> set[str]:
    result = set()
    for raw in re.findall(r"[a-z0-9]+", text.casefold()):
        if raw in STOP_WORDS or len(raw) < 2:
            continue
        word = SYNONYMS.get(raw, raw)
        if len(word) > 4 and word.endswith("s"):
            word = word[:-1]
        result.add(word)
    return result


def retrieve(state: CourseState) -> dict:
    query_terms = terms(state["query"])
    ranked: list[tuple[float, dict[str, str]]] = []
    for document in CORPUS:
        document_terms = terms(document["text"])
        overlap = len(query_terms & document_terms)
        score = overlap / max(len(query_terms), 1)
        if overlap >= 2 and score >= 0.3:
            ranked.append((score, document))
    ranked.sort(key=lambda item: item[0], reverse=True)
    evidence = [document | {"score": f"{score:.2f}"} for score, document in ranked]
    return {"evidence": evidence}


def rewrite(state: CourseState) -> dict:
    expanded = set(terms(state["original_question"]))
    for term in tuple(expanded):
        synonym = SYNONYMS.get(term)
        if synonym:
            expanded.add(synonym)
    return {"query": " ".join(sorted(expanded)), "attempts": state["attempts"] + 1}


def route_after_retrieval(state: CourseState) -> Literal["answer", "rewrite", "abstain"]:
    if state["evidence"]:
        return "answer"
    if state["attempts"] < 1:
        return "rewrite"
    return "abstain"


def answer_from_evidence(state: CourseState) -> dict:
    citations = ", ".join(item["id"] for item in state["evidence"])
    snippets = " ".join(item["text"] for item in state["evidence"])
    return {
        "answer": f"Retrieved context: {snippets} Sources: {citations}.",
        "status": "grounded",
    }


def abstain(state: CourseState) -> dict:
    return {
        "answer": "I cannot confirm this from the demo corpus. Add an approved source or ask a person.",
        "status": "insufficient_evidence",
    }


def build_graph():
    builder = StateGraph(CourseState)
    builder.add_node("retrieve", retrieve)
    builder.add_node("rewrite", rewrite)
    builder.add_node("answer", answer_from_evidence)
    builder.add_node("abstain", abstain)
    builder.add_edge(START, "retrieve")
    builder.add_conditional_edges(
        "retrieve",
        route_after_retrieval,
        {"answer": "answer", "rewrite": "rewrite", "abstain": "abstain"},
    )
    builder.add_edge("rewrite", "retrieve")
    builder.add_edge("answer", END)
    builder.add_edge("abstain", END)
    return builder.compile()


def main() -> None:
    graph = build_graph()
    for question in (
        "Who must approve a reimbursement?",
        "What is today's weather on Mars?",
    ):
        initial: CourseState = {
            "original_question": question,
            "query": question,
            "attempts": 0,
            "evidence": [],
            "answer": "",
            "status": "running",
        }
        result = graph.invoke(initial)
        print(f"\nQUESTION: {question}")
        print(f"STATUS: {result['status']} | RETRIEVAL ATTEMPTS: {result['attempts'] + 1}")
        print(result["answer"])


if __name__ == "__main__":
    main()
