from __future__ import annotations

import unittest

from agent_loop_demo import Agent, FinalAnswer, ToolRequest, ToolCallError, build_demo_agent, build_demo_registry
from multi_agent_demo import Coordinator


class RepeatingPlanner:
    def decide(self, history, tools):
        return ToolRequest("search_refund_policy", {"topic": "refund"})


class AgentLoopLabTests(unittest.TestCase):
    def test_demo_runs_tools_then_finishes(self) -> None:
        result = build_demo_agent().run("Calculate the proposed refund for a $120 order.")
        self.assertEqual(result.status, "complete")
        self.assertEqual(result.steps, 3)
        self.assertIn("$12.00", result.answer)
        self.assertTrue(any(item["type"] == "tool_call" for item in result.trace))
        self.assertIn("no refund was issued", result.answer.lower())

    def test_schema_rejects_extra_and_wrongly_typed_arguments(self) -> None:
        registry = build_demo_registry()
        with self.assertRaises(ToolCallError):
            registry.invoke("calculate_refund", {"total": 100, "rate": 0.1, "currency": "USD"})
        with self.assertRaises(ToolCallError):
            registry.invoke("calculate_refund", {"total": True, "rate": 0.1})
        with self.assertRaises(ToolCallError):
            registry.invoke("shell", {"command": "whoami"})

    def test_loop_has_a_hard_step_limit(self) -> None:
        result = Agent(RepeatingPlanner(), build_demo_registry(), max_steps=2).run("Search repeatedly")
        self.assertEqual(result.status, "max_steps")
        self.assertIn("not confirmed complete", result.answer)
        self.assertEqual(result.steps, 2)

    def test_empty_question_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            build_demo_agent().run("  ")


class MultiAgentLabTests(unittest.TestCase):
    def test_coordinator_requires_approval_for_financial_side_effect(self) -> None:
        result = Coordinator().run("Please issue the refund now.")
        self.assertEqual(result.status, "approval_required")
        self.assertIn("No refund was issued", result.answer)
        self.assertEqual(len(result.findings), 2)

    def test_coordinator_abstains_without_evidence(self) -> None:
        result = Coordinator().run("What is the password reset process?")
        self.assertEqual(result.status, "insufficient_evidence")
        self.assertIn("cannot confirm", result.answer)


if __name__ == "__main__":
    unittest.main()
