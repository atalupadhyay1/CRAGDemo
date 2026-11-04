"""Dependency-free teaching lab: a bounded model/tool/orchestrator loop.

The DemoPlanner is a deterministic double, not an LLM. Replace the Planner
adapter for a provider integration; keep the tool registry and policy boundary.
Run from the repository root: python AgenticAI/labs/agent_loop_demo.py
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Callable, Protocol


class ToolCallError(ValueError):
    """Raised when a requested tool or its arguments are invalid."""


@dataclass(frozen=True)
class ToolDefinition:
    name: str
    description: str
    schema: dict[str, Any]
    handler: Callable[[dict[str, Any]], dict[str, Any]]


class ToolRegistry:
    """Small JSON-schema-style registry with explicit types and allowlisting."""

    def __init__(self) -> None:
        self._tools: dict[str, ToolDefinition] = {}

    def register(self, definition: ToolDefinition) -> None:
        if definition.name in self._tools:
            raise ValueError(f"Tool already registered: {definition.name}")
        self._tools[definition.name] = definition

    def definitions(self) -> list[dict[str, Any]]:
        return [
            {"name": tool.name, "description": tool.description, "parameters": tool.schema}
            for tool in self._tools.values()
        ]

    def invoke(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        tool = self._tools.get(name)
        if tool is None:
            raise ToolCallError(f"Tool is not allowlisted: {name}")
        if not isinstance(arguments, dict):
            raise ToolCallError("Arguments must be a JSON object.")
        schema = tool.schema
        properties = schema.get("properties", {})
        missing = [key for key in schema.get("required", []) if key not in arguments]
        if missing:
            raise ToolCallError(f"Missing required arguments: {', '.join(missing)}")
        if schema.get("additionalProperties") is False:
            extras = sorted(set(arguments) - set(properties))
            if extras:
                raise ToolCallError(f"Unexpected arguments: {', '.join(extras)}")
        expected_types = {
            "string": lambda value: isinstance(value, str),
            "integer": lambda value: isinstance(value, int) and not isinstance(value, bool),
            "number": lambda value: isinstance(value, (int, float)) and not isinstance(value, bool),
            "boolean": lambda value: isinstance(value, bool),
        }
        for key, value in arguments.items():
            property_schema = properties.get(key)
            if property_schema is None:
                continue
            expected = property_schema.get("type")
            predicate = expected_types.get(expected)
            if predicate is not None and not predicate(value):
                raise ToolCallError(f"Argument '{key}' must be a {expected}.")
            enum = property_schema.get("enum")
            if enum is not None and value not in enum:
                raise ToolCallError(f"Argument '{key}' must be one of {enum}.")
        return tool.handler(arguments)


@dataclass(frozen=True)
class ToolRequest:
    name: str
    arguments: dict[str, Any]


@dataclass(frozen=True)
class FinalAnswer:
    text: str


Decision = ToolRequest | FinalAnswer


class Planner(Protocol):
    def decide(self, history: list[dict[str, Any]], tools: list[dict[str, Any]]) -> Decision:
        """Choose an allowed tool request or return a final answer."""


class DemoPlanner:
    """A small scripted planner so the lab runs without a model/API key."""

    def decide(self, history: list[dict[str, Any]], tools: list[dict[str, Any]]) -> Decision:
        observations = {
            message.get("name"): message.get("content")
            for message in history
            if message.get("role") == "tool"
        }
        policy = observations.get("search_refund_policy")
        calculation = observations.get("calculate_refund")
        if policy is None:
            return ToolRequest("search_refund_policy", {"topic": "refund eligibility"})
        if calculation is None:
            return ToolRequest(
                "calculate_refund",
                {"total": 120.0, "rate": policy["refund_rate"]},
            )
        return FinalAnswer(
            f"The example policy permits a {policy['refund_rate']:.0%} refund. "
            f"For the example order total of ${calculation['total']:.2f}, "
            f"the calculated amount is ${calculation['refund_amount']:.2f}. "
            "This is a draft calculation only; no refund was issued."
        )


def search_refund_policy(arguments: dict[str, Any]) -> dict[str, Any]:
    """Return a fixed teaching fixture; a production tool would query approved policy."""
    return {
        "topic": arguments["topic"],
        "refund_rate": 0.10,
        "source_id": "POLICY-DEMO-01",
        "excerpt": "For this exercise only, eligible refunds are 10 percent of the order total.",
    }


def calculate_refund(arguments: dict[str, Any]) -> dict[str, Any]:
    total = float(arguments["total"])
    rate = float(arguments["rate"])
    if total < 0 or total > 1_000_000:
        raise ToolCallError("Total must be between 0 and 1,000,000.")
    if not 0 <= rate <= 1:
        raise ToolCallError("Rate must be between 0 and 1.")
    return {"total": total, "rate": rate, "refund_amount": round(total * rate, 2)}


def build_demo_registry() -> ToolRegistry:
    registry = ToolRegistry()
    registry.register(ToolDefinition(
        name="search_refund_policy",
        description="Read the approved demo refund policy. Does not issue a refund.",
        schema={
            "type": "object",
            "properties": {"topic": {"type": "string"}},
            "required": ["topic"],
            "additionalProperties": False,
        },
        handler=search_refund_policy,
    ))
    registry.register(ToolDefinition(
        name="calculate_refund",
        description="Calculate a proposed amount; does not move money or update an account.",
        schema={
            "type": "object",
            "properties": {
                "total": {"type": "number"},
                "rate": {"type": "number"},
            },
            "required": ["total", "rate"],
            "additionalProperties": False,
        },
        handler=calculate_refund,
    ))
    return registry


@dataclass
class AgentResult:
    answer: str
    status: str
    steps: int
    trace: list[dict[str, Any]] = field(default_factory=list)
    history: list[dict[str, Any]] = field(default_factory=list)


class Agent:
    def __init__(self, planner: Planner, tools: ToolRegistry, max_steps: int = 6) -> None:
        if max_steps < 1:
            raise ValueError("max_steps must be at least 1")
        self.planner = planner
        self.tools = tools
        self.max_steps = max_steps

    def run(self, question: str) -> AgentResult:
        clean_question = question.strip()
        if not clean_question:
            raise ValueError("Question must not be empty.")
        history: list[dict[str, Any]] = [{"role": "user", "content": clean_question}]
        trace: list[dict[str, Any]] = []
        for step in range(1, self.max_steps + 1):
            decision = self.planner.decide(history, self.tools.definitions())
            if isinstance(decision, FinalAnswer):
                trace.append({"step": step, "type": "final", "status": "complete"})
                return AgentResult(decision.text, "complete", step, trace, history)
            if not isinstance(decision, ToolRequest):
                raise TypeError("Planner must return ToolRequest or FinalAnswer.")

            trace.append({
                "step": step,
                "type": "tool_call",
                "tool": decision.name,
                "arguments": decision.arguments,
                "status": "requested",
            })
            history.append({
                "role": "assistant",
                "tool_call": {"name": decision.name, "arguments": decision.arguments},
            })
            try:
                observation = self.tools.invoke(decision.name, decision.arguments)
                status = "ok"
            except ToolCallError as error:
                observation = {"error": str(error), "retryable": False}
                status = "rejected"
            history.append({"role": "tool", "name": decision.name, "content": observation})
            trace[-1]["status"] = status
            trace[-1]["observation"] = observation

        trace.append({"step": self.max_steps + 1, "type": "stop", "status": "max_steps"})
        return AgentResult(
            "Stopped at the configured step limit. The task is not confirmed complete.",
            "max_steps",
            self.max_steps,
            trace,
            history,
        )


def build_demo_agent(max_steps: int = 6) -> Agent:
    return Agent(DemoPlanner(), build_demo_registry(), max_steps=max_steps)


def main() -> None:
    result = build_demo_agent().run("Find the demo refund policy and calculate the proposed amount for a $120 order.")
    print("ANSWER")
    print(result.answer)
    print("\nTRACE")
    print(json.dumps(result.trace, indent=2))
    print("\nNo refund was issued by this lab.")


if __name__ == "__main__":
    main()
