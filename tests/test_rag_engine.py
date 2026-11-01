from __future__ import annotations

import json
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from rag_engine import AgentEngine, Document, TavilySearch, ToolRegistry, VectorStore


ROOT = Path(__file__).resolve().parents[1]
SAMPLE_DOCS = ROOT / "data" / "sample_docs.json"


def make_engine(user_path: Path | None = None) -> AgentEngine:
    return AgentEngine.from_json_files(
        SAMPLE_DOCS,
        user_path or Path(tempfile.gettempdir()) / "crag-demo-test-user-documents.json",
        web_search=TavilySearch(api_key=""),
    )


class VectorStoreTests(unittest.TestCase):
    def test_hybrid_search_finds_relevant_document(self) -> None:
        store = VectorStore([
            Document("D-1", "Vector retrieval", "Cosine similarity ranks vector search passages by relevance."),
            Document("D-2", "Calculator", "Safe arithmetic evaluation should reject arbitrary code."),
        ])
        hits = store.search("How does cosine similarity rank vector passages?", limit=2)
        self.assertEqual(hits[0].chunk.document_id, "D-1")
        self.assertGreater(hits[0].score, hits[1].score)
        self.assertGreater(hits[0].lexical_coverage, 0.3)

    def test_empty_index_returns_no_hits(self) -> None:
        self.assertEqual(VectorStore().search("anything"), [])


class AgentEngineTests(unittest.TestCase):
    def test_answer_has_xml_envelope_and_real_citation(self) -> None:
        result = make_engine().query("How does vector retrieval rank passages?")
        self.assertIn("<reasoning>", result["answer_xml"])
        self.assertIn("<sources>", result["answer_xml"])
        self.assertIn("<answer>", result["answer_xml"])
        self.assertTrue(result["retrieval"]["relevant"])
        self.assertEqual(result["sources"][0]["id"], "KB-002")
        root = ET.fromstring(f"<response>{result['answer_xml']}</response>")
        self.assertIsNotNone(root.find("answer"))
        self.assertTrue(root.findall("sources/source"))

    def test_low_relevance_reformulates_and_refuses_without_evidence(self) -> None:
        result = make_engine().query("Tell me about quantum entanglement in the 1800s")
        self.assertFalse(result["retrieval"]["relevant"])
        self.assertEqual(len(result["retrieval"]["passes"]), 2)
        self.assertIn("Query reformulation", [step["stage"] for step in result["trace"]])
        self.assertIn("Web search fallback", [step["stage"] for step in result["trace"]])
        self.assertIn("I cannot confirm this based on the available context.", result["answer"])
        self.assertEqual(result["tool_calls"][0]["result"]["status"], "not_configured")

    def test_fresh_query_uses_web_search_even_if_local_search_exists(self) -> None:
        result = make_engine().query("What is the latest Python release?")
        self.assertEqual(result["route"], "external_search")
        self.assertTrue(result["classification"]["needs_freshness"])
        self.assertIn("Web search fallback", [step["stage"] for step in result["trace"]])
        self.assertIn("I cannot confirm this based on the available context.", result["answer"])

    def test_safe_calculator_tool_and_restricted_syntax(self) -> None:
        engine = make_engine()
        result = engine.query("What is 18 * 24?")
        self.assertEqual(result["route"], "direct_calculation")
        self.assertIn("432", result["answer"])
        self.assertEqual(result["tool_calls"][0]["name"], "calculator")
        self.assertEqual(result["tool_calls"][0]["result"]["result"], 432)
        self.assertEqual(engine.tools.invoke("calculator", {"expression": "(2 + 3)^3"})["result"], 125)
        with self.assertRaises(ValueError):
            engine.tools.invoke("calculator", {"expression": "__import__('os').system('echo unsafe')"})
        with self.assertRaises(ValueError):
            engine.tools.invoke("calculator", {"expression": "2 ** 99"})

    def test_uploaded_document_is_persisted_indexed_and_deletable(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            storage = Path(folder) / "user_documents.json"
            engine = make_engine(storage)
            summary = engine.add_document(
                "Incident notes",
                "The Orion retrieval service stores incident runbooks and indexes each upload for local search.",
            )
            self.assertTrue(storage.exists())
            self.assertEqual(json.loads(storage.read_text())[0]["id"], summary["id"])
            self.assertIn(summary["id"], {doc["id"] for doc in engine.list_documents()})
            result = engine.query("How are Orion incident runbooks indexed?")
            self.assertTrue(result["retrieval"]["relevant"])
            self.assertEqual(result["sources"][0]["id"], summary["id"])
            self.assertTrue(engine.delete_document(summary["id"]))
            self.assertFalse(engine.delete_document(summary["id"]))
            self.assertEqual(json.loads(storage.read_text()), [])

    def test_uploaded_document_validation(self) -> None:
        engine = make_engine()
        with self.assertRaises(ValueError):
            engine.add_document("", "This is enough text to test a title requirement.")
        with self.assertRaises(ValueError):
            engine.add_document("Short", "Too short")
        with self.assertRaises(ValueError):
            engine.query(" ")

    def test_xml_escapes_document_metadata(self) -> None:
        engine = AgentEngine(
            [Document("SAFE-1", "RAG & <sources>", "RAG grounding uses source evidence and citations for each supported claim.")],
            web_search=TavilySearch(api_key=""),
        )
        result = engine.query("Explain RAG grounding and citations")
        root = ET.fromstring(f"<response>{result['answer_xml']}</response>")
        self.assertEqual(root.find("sources/source").attrib["title"], "RAG & <sources>")
        self.assertIn("RAG &amp; &lt;sources&gt;", result["answer_xml"])


class ToolRegistryTests(unittest.TestCase):
    def test_schema_validation_rejects_missing_and_wrong_arguments(self) -> None:
        registry = ToolRegistry()
        registry.register(
            "sample",
            "test",
            {
                "type": "object",
                "properties": {"count": {"type": "integer"}},
                "required": ["count"],
                "additionalProperties": False,
            },
            lambda arguments: {"value": arguments["count"]},
        )
        self.assertEqual(registry.invoke("sample", {"count": 3}), {"value": 3})
        with self.assertRaises(ValueError):
            registry.invoke("sample", {})
        with self.assertRaises(ValueError):
            registry.invoke("sample", {"count": "3"})
        with self.assertRaises(ValueError):
            registry.invoke("sample", {"count": 3, "extra": True})


if __name__ == "__main__":
    unittest.main()
