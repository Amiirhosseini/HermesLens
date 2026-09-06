---
name: steal-ideas
description: Extract transferable design ideas from emerging agent projects and outline patches for a target framework or product.
---

# Steal ideas

## When to use
User is building an agent framework/product and wants concrete patterns from Hermes, OpenClaw, LangChain, AutoGen, or CrewAI.

## Steps
1. Identify **target** (what you are improving).
2. Optionally limit **sources** with `--from`.
3. Run `hermeslens steal <target> --from hermes --from openclaw` or MCP `steal_design_ideas`.
4. Sort by transfer cost: prefer **low** spikes first.
5. For each idea: one module, one test, one demo knob — then merge.

## Good transfers
- Progressive skill disclosure (Hermes)
- Tiny frozen always-on memory (Hermes)
- Trusted gateway vs untrusted Hands (OpenClaw)
- Model-native harness plugins (OpenClaw)
- Durable graph checkpoints (LangGraph)
- Role group-chat manager (AutoGen)

## Pitfalls
- Do not copy brand/UI — copy **mechanisms**.
- High-cost ideas need an ADR before implementation.
