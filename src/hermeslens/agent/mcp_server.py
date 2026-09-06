"""MCP server exposing HermesLens dissection tools."""

from __future__ import annotations

import json

from mcp.server.fastmcp import FastMCP

from hermeslens.catalog import list_frameworks
from hermeslens.dissect import dissect
from hermeslens.models import CompareRequest
from hermeslens.scorecard import compare
from hermeslens.steal import philosophy_diff, steal_ideas

mcp = FastMCP("hermeslens")


@mcp.tool()
def list_agent_frameworks() -> str:
    """List agent frameworks in the HermesLens catalog."""
    rows = [
        {"id": p.id, "name": p.name, "cog": p.center_of_gravity}
        for p in list_frameworks()
    ]
    return json.dumps(rows, indent=2)


@mcp.tool()
def dissect_framework(framework_id: str) -> str:
    """Technically dissect one agent framework (architecture, scores, ideas)."""
    return json.dumps(dissect(framework_id), indent=2)


@mcp.tool()
def compare_frameworks(framework_ids: str, preset: str = "rnd") -> str:
    """Compare comma-separated framework IDs on the architecture scorecard."""
    ids = [x.strip() for x in framework_ids.split(",") if x.strip()]
    result = compare(CompareRequest(frameworks=ids), preset=preset or None)
    return json.dumps(result.model_dump(mode="json"), indent=2)


@mcp.tool()
def steal_design_ideas(target: str, sources: str = "", max_ideas: int = 6) -> str:
    """Propose transferable design ideas into a target framework."""
    src = [s.strip() for s in sources.split(",") if s.strip()] or None
    plan = steal_ideas(target, src, max_ideas=max_ideas)
    return json.dumps(plan.model_dump(mode="json"), indent=2)


@mcp.tool()
def philosophy_compare(left: str, right: str) -> str:
    """Diff philosophies and centers of gravity between two frameworks."""
    return json.dumps({"lines": philosophy_diff(left, right)}, indent=2)


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
