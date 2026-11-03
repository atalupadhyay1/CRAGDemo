"""Run the repository's local corrective-RAG engine without external search.

Run from the repository root: python AgenticAI/labs/rag_demo.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPOSITORY_ROOT))

from rag_engine import AgentEngine, TavilySearch  # noqa: E402


def main() -> None:
    engine = AgentEngine.from_json_files(
        REPOSITORY_ROOT / "data" / "sample_docs.json",
        REPOSITORY_ROOT / "data" / "course_uploads.json",
        web_search=TavilySearch(api_key=""),  # This lab never makes a network search call.
    )
    questions = [
        "How does vector retrieval rank passages?",
        "What is the current weather on Mars today?",
    ]
    for question in questions:
        result = engine.query(question)
        print(f"\nQUESTION: {question}")
        print(f"ROUTE: {result['route']}")
        print(f"ANSWER: {result['answer']}")
        print("SOURCES:")
        for source in result["sources"]:
            print(f"  - {source['id']}: {source['title']}")
        print("TRACE:")
        for step in result["trace"]:
            print(f"  - {step['stage']}: {step['detail']}")


if __name__ == "__main__":
    main()
