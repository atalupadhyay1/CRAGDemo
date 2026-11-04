"""Minimal local MCP server exposing a safe demo tool, resource, and prompt.

Install the official Python SDK, then run this as a local stdio subprocess:
  python -m pip install 'mcp>=1.2.0'
  python AgenticAI/labs/optional/mcp_server.py

Do not add arbitrary SQL, shell, file, or payment capabilities to this demo server.
"""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP


mcp = FastMCP("agentic-ai-course-demo")


@mcp.tool()
def calculate_proposed_refund(total: float, rate: float) -> dict[str, float]:
    """Calculate a proposed amount only; this tool never issues a refund."""
    if total < 0 or total > 1_000_000:
        raise ValueError("total must be between 0 and 1,000,000")
    if rate < 0 or rate > 1:
        raise ValueError("rate must be between 0 and 1")
    return {"total": total, "rate": rate, "proposed_amount": round(total * rate, 2)}


@mcp.resource("policy://refunds/demo")
def refund_policy_resource() -> str:
    """Return a clearly labeled, non-production policy fixture."""
    return (
        "TEACHING FIXTURE ONLY: the example proposes a 10% refund calculation. "
        "A real refund requires an authoritative eligibility check and human approval."
    )


@mcp.prompt()
def review_refund_request(order_total: float) -> str:
    """Create a review prompt; never authorize or execute a refund."""
    return (
        f"Review the proposed refund for an order total of {order_total:.2f}. "
        "Use only approved policy evidence. State missing facts and require human approval. "
        "Do not claim that a refund was issued."
    )


if __name__ == "__main__":
    # stdio is suitable for a local MCP client that launches this subprocess.
    # The SDK owns the protocol stream; avoid printing diagnostics to stdout.
    mcp.run(transport="stdio")
