# HermesLens

**Agent framework dissection lab** — architecture scorecards, center-of-gravity diffs, and steal-these-ideas patches for Hermes, OpenClaw, LangChain/LangGraph, AutoGen, and CrewAI.

> **Live demo:** [amiirhosseini.github.io/hermeslens](https://amiirhosseini.github.io/hermeslens/)  
> Touchable scorecard in the browser — flip weights, compare frameworks, expand transferable ideas. No server.

[![Live Demo](https://img.shields.io/badge/demo-live-0f7a6c)](https://amiirhosseini.github.io/hermeslens/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11%2B-green.svg)](pyproject.toml)

## What it solves

Agent ecosystems move fast. Teams need a repeatable way to:

- **Dissect** emerging projects (Hermes learning loop vs OpenClaw gateway) without cargo-culting blogs
- **Score** architectures on shared axes (memory, skills, self-evolution, multi-agent, safety, DX…)
- **Transfer** concrete mechanisms into a proprietary or open-source framework as ranked patch ideas

HermesLens is a research/engineering toolkit for that loop — catalog → compare → steal → spike.

## Features

| Area | What you get |
|------|----------------|
| **Catalog** | Curated profiles: Hermes, OpenClaw, LangChain/LangGraph, AutoGen, CrewAI |
| **Scorecard** | 10-axis scores with rationales + evidence notes |
| **Weight presets** | Equal, Agent R&D, Product/gateway |
| **Steal planner** | Transfer-cost ranked design ideas + patch outline |
| **CLI / API / MCP** | Same engine for humans, scripts, and Hermes |
| **Live demo** | GitHub Pages interactive lab |

## Quick start

```bash
git clone https://github.com/Amiirhosseini/hermeslens.git
cd hermeslens
python -m venv .venv && .\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"

hermeslens list
hermeslens dissect hermes
hermeslens score hermes openclaw --preset rnd
hermeslens steal openclaw --from hermes --from langchain
hermeslens diff hermes openclaw
```

## Live demo walkthrough

1. Open the [live demo](https://amiirhosseini.github.io/hermeslens/)
2. Keep **Hermes** + **OpenClaw** selected
3. Click **R&D weights** — watch learning/skills axes dominate
4. Switch to **Product / gateway bias** — OpenClaw usually climbs
5. Open **Steal-these-ideas** cards — expand low-cost transfers first

## Hermes skills

```bash
hermeslens mcp
# /dissect-framework  /scorecard  /steal-ideas
```

Skills live under `hermes/skills/`.

## Axes

| Axis | Question |
|------|----------|
| Memory | How is knowledge layered, budgeted, retrieved? |
| Skills | Procedural knowledge model + lifecycle |
| Learning | Self-evolution / distillation loop |
| Multi-agent | Collaboration patterns |
| Gateway | Channels, sessions, ops control plane |
| Safety | Defaults for approvals / isolation |
| DX | Developer / operator experience |
| Tooling | Function calling & tool surface |
| Context | Prompt/context engineering posture |
| Extensibility | Plugins, MCP, harnesses |

Scores are curated research notes (1–5), not benchmarks. Override via YAML in `data/frameworks/`.

## Layout

```text
hermeslens/
  src/hermeslens/     # catalog, scorecard, steal, CLI, API, MCP
  hermes/skills/      # Hermes Agent skills
  docs/               # GitHub Pages live demo
  tests/
  data/frameworks/    # optional YAML overrides
```

## API

```bash
hermeslens serve
# GET  /frameworks
# GET  /frameworks/{id}
# POST /compare
# GET  /steal?target=openclaw&sources=hermes
```

## License

Apache-2.0
