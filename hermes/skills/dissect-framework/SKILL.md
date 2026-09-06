---
name: dissect-framework
description: Technically dissect an agent framework (Hermes, OpenClaw, LangChain, AutoGen, CrewAI) — philosophy, center of gravity, strengths, weaknesses, architecture notes.
---

# Dissect framework

## When to use
User asks how an agent framework works, wants an architecture teardown, or needs critical analysis of design tradeoffs.

## Steps
1. Run `hermeslens dissect <id> --json` (or MCP `dissect_framework`).
2. Lead with **center of gravity** (what the system orbits around).
3. Contrast **philosophy** vs a peer (often Hermes vs OpenClaw).
4. Call out **strengths** and **weaknesses** with evidence, not vibes.
5. End with 1–3 **steal-these-ideas** candidates if the user is building something.

## Framework IDs
`hermes`, `openclaw`, `langchain`, `autogen`, `crewai`

## Pitfalls
- Do not claim scores are universal truth — they are curated research notes.
- Distinguish library frameworks (LangChain) from operated products (OpenClaw gateway).
