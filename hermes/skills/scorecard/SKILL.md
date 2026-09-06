---
name: scorecard
description: Compare agent frameworks on a multi-axis architecture scorecard (memory, skills, learning, multi-agent, gateway, safety, DX, tooling, context, extensibility).
---

# Scorecard

## When to use
User wants a side-by-side comparison, radar/table view, or R&D-weighted ranking of agent frameworks.

## Steps
1. Confirm frameworks (default: `hermes,openclaw`).
2. Run `hermeslens score hermes openclaw --preset rnd` or MCP `compare_frameworks`.
3. Highlight axes with **spread ≥ 2** — those are the real forks in design philosophy.
4. State the winner **under the chosen weights**, and note that changing weights changes the winner.

## Axes
memory, skills, learning, multi_agent, gateway, safety, dx, tooling, context, extensibility

## Verification
- Totals should be between 1 and 5.
- Notes should mention each framework's center of gravity.
