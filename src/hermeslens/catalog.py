"""Built-in catalog of agent frameworks for dissection."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import yaml

from hermeslens.models import AxisId, AxisScore, DesignIdea, FrameworkProfile

DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "frameworks"


def _axis(axis: AxisId, score: int, rationale: str, *evidence: str) -> AxisScore:
    return AxisScore(axis=axis, score=score, rationale=rationale, evidence=list(evidence))


def _builtin_profiles() -> dict[str, FrameworkProfile]:
    """Canonical profiles used when YAML files are missing."""
    hermes = FrameworkProfile(
        id="hermes",
        name="Hermes Agent",
        vendor="Nous Research",
        language="Python",
        philosophy=(
            "Self-improving agent loop first: observe → distill → reuse → refine. "
            "Procedural skills are first-class memory, not just plugins."
        ),
        center_of_gravity="AIAgent execution loop + learning loop",
        strengths=[
            "Built-in skill creation/patching from successful trajectories",
            "Layered memory: curated MEMORY.md/USER.md + SQLite FTS5 + optional Honcho",
            "Prompt kept small/stable for caching; retrieval via tools",
            "Model-agnostic providers; messaging gateway + cron",
            "agentskills.io compatible Skills Hub",
        ],
        weaknesses=[
            "Self-written skills need approval gates in production",
            "Skill sprawl without curator/lifecycle policies",
            "Learning quality depends on trajectory quality and eval signal",
        ],
        architecture_notes=[
            "Core is the agent loop; gateway/cron/ACP orbit around it",
            "skill_manage tool creates/patches SKILL.md under ~/.hermes/skills/",
            "Progressive disclosure: skill index cheap, full body loaded on match",
            "SOUL.md is instance-global identity (not workspace-tied)",
            "Five-layer safety posture: auth, approvals, isolation, credential filter, context scan",
        ],
        urls={
            "docs": "https://hermes-agent.nousresearch.com/docs/",
            "learning_loop": "https://hermes-agent.ai/features/learning-loop",
        },
        scores=[
            _axis(
                AxisId.MEMORY,
                5,
                "Layered stack with hard budget on always-on memory and FTS5 recall.",
                "MEMORY.md + USER.md ~1.3k tokens",
                "SQLite FTS5 session_search",
            ),
            _axis(
                AxisId.SKILLS,
                5,
                "Procedural skills as living memory; create/patch during use.",
                "skill_manage",
                "agentskills.io",
            ),
            _axis(
                AxisId.LEARNING,
                5,
                "Closed learning loop with skill distillation and trajectory export.",
                "observe→distill→reuse→refine",
            ),
            _axis(
                AxisId.MULTI_AGENT,
                3,
                "Strong single-agent evolution; multi-agent is secondary vs swarm frameworks.",
            ),
            _axis(
                AxisId.GATEWAY,
                4,
                "Messaging gateway + cron jobs in fresh sessions.",
                "Telegram/Discord/Slack/WhatsApp",
            ),
            _axis(
                AxisId.SAFETY,
                4,
                "Safer-by-default narrative with approvals and isolation layers.",
            ),
            _axis(
                AxisId.DX,
                4,
                "TUI, slash skills, clear home directory layout.",
            ),
            _axis(
                AxisId.TOOLING,
                4,
                "Large built-in tool surface + MCP integration.",
            ),
            _axis(
                AxisId.CONTEXT,
                5,
                "Stable prompt + progressive skill disclosure + memory flush before compaction.",
            ),
            _axis(
                AxisId.EXTENSIBILITY,
                4,
                "MCP, Skills Hub, ACP for editors; less plugin-harness depth than OpenClaw.",
            ),
        ],
        ideas=[
            DesignIdea(
                id="hermes-learning-loop",
                title="Observe→distill→reuse→refine skill loop",
                source_framework="hermes",
                summary=(
                    "After N successful similar trajectories, distill a SKILL.md and refine "
                    "it when pitfalls appear mid-session."
                ),
                why_it_matters="Turns episodic success into inspectable procedural memory.",
                transfer_cost="medium",
                integrate_into=["openclaw", "langchain", "custom"],
                axes=[AxisId.LEARNING, AxisId.SKILLS],
            ),
            DesignIdea(
                id="hermes-prompt-budget",
                title="Tiny frozen always-on memory + tool retrieval",
                source_framework="hermes",
                summary=(
                    "Keep MEMORY.md/USER.md tiny and frozen per session; push history into "
                    "searchable store with summarization on demand."
                ),
                why_it_matters="Improves cache hit rate and forces memory curation.",
                transfer_cost="medium",
                integrate_into=["openclaw", "crewai", "custom"],
                axes=[AxisId.MEMORY, AxisId.CONTEXT],
            ),
            DesignIdea(
                id="hermes-progressive-skills",
                title="Progressive skill disclosure",
                source_framework="hermes",
                summary=(
                    "Load only skill name/description in the prompt; hydrate full SKILL.md "
                    "when the task matches."
                ),
                why_it_matters="Near-zero token tax for large skill libraries.",
                transfer_cost="low",
                integrate_into=["openclaw", "langchain", "autogen", "custom"],
                axes=[AxisId.SKILLS, AxisId.CONTEXT],
            ),
        ],
    )

    openclaw = FrameworkProfile(
        id="openclaw",
        name="OpenClaw",
        vendor="OpenClaw community / Steinberger lineage",
        language="TypeScript / Node.js",
        philosophy=(
            "Control-plane-first personal agent: one Gateway owns channels, credentials, "
            "policy, and session orchestration. Skills are mostly human-authored."
        ),
        center_of_gravity="Gateway daemon (WebSocket control plane)",
        strengths=[
            "Clear Brain vs Hands separation (reason vs execute)",
            "Gateway owns channels, auth, policy; harness plugins for model-native runtimes",
            "Multi-agent routing by channel binding",
            "File-backed workspace identity (SOUL.md, MEMORY.md, HEARTBEAT.md)",
            "ClawHub skills + plugin SDK for harnesses",
        ],
        weaknesses=[
            "Learning loop is weaker than Hermes (skills less auto-distilled)",
            "Single-process gateway → vertical scale story",
            "Safety historically operator-heavy; defaults tightened over time",
        ],
        architecture_notes=[
            "Gateway binds loopback by default; channels plug into one daemon",
            "Embedded agent runner + optional vendor harnesses (Codex/Copilot/Claude SDK)",
            "Memory: Markdown source of truth + hybrid retrieval over files/transcripts",
            "SOUL.md is workspace-scoped identity",
            "Heartbeat / dreaming loops for proactive autonomy",
        ],
        urls={
            "architecture": "https://clawdocs.org/architecture/overview",
            "docs": "https://docs.openclaw.ai/",
        },
        scores=[
            _axis(
                AxisId.MEMORY,
                4,
                "Markdown-canonical memory with hybrid search; less rigid token budgeting.",
            ),
            _axis(
                AxisId.SKILLS,
                4,
                "Mature SKILL.md + ClawHub ecosystem; primarily human-authored.",
            ),
            _axis(
                AxisId.LEARNING,
                2,
                "Improves via operator edits and community skills more than auto-distillation.",
            ),
            _axis(
                AxisId.MULTI_AGENT,
                4,
                "Router binds channels to specialized agents behind one gateway.",
            ),
            _axis(
                AxisId.GATEWAY,
                5,
                "Gateway-centric product: channels, sessions, approvals, node registry.",
            ),
            _axis(
                AxisId.SAFETY,
                3,
                "Strong policy surface evolving; historically needed tight operator config.",
            ),
            _axis(
                AxisId.DX,
                4,
                "One binary/daemon mental model; rich channel ecosystem.",
            ),
            _axis(
                AxisId.TOOLING,
                4,
                "Hands layer: shell, FS, browser, HTTP with sandboxing patterns.",
            ),
            _axis(
                AxisId.CONTEXT,
                4,
                "Assembles SOUL + memory + session package per turn; workspace-native.",
            ),
            _axis(
                AxisId.EXTENSIBILITY,
                5,
                "Plugin harness registry lets model families keep native runtimes.",
            ),
        ],
        ideas=[
            DesignIdea(
                id="openclaw-gateway",
                title="Trusted gateway vs untrusted execution",
                source_framework="openclaw",
                summary=(
                    "Keep credentials/channels/policy on a trusted Gateway; move risky "
                    "execution to sandboxed Hands / remote nodes."
                ),
                why_it_matters="Fail-closed control plane for toB deployments.",
                transfer_cost="high",
                integrate_into=["hermes", "custom"],
                axes=[AxisId.GATEWAY, AxisId.SAFETY],
            ),
            DesignIdea(
                id="openclaw-harness",
                title="Model-native harness plugins",
                source_framework="openclaw",
                summary=(
                    "Register harnesses that run a model family's native session loop "
                    "while Gateway still owns channels and policy."
                ),
                why_it_matters="Avoid lowest-common-denominator agent loops across providers.",
                transfer_cost="high",
                integrate_into=["hermes", "langchain", "custom"],
                axes=[AxisId.EXTENSIBILITY, AxisId.TOOLING],
            ),
            DesignIdea(
                id="openclaw-workspace-soul",
                title="Workspace-scoped identity pack",
                source_framework="openclaw",
                summary=(
                    "SOUL.md + AGENTS.md + TOOLS.md + HEARTBEAT.md as a project-local "
                    "behavior pack instead of one global personality."
                ),
                why_it_matters="Better for multi-repo / multi-tenant product surfaces.",
                transfer_cost="low",
                integrate_into=["hermes", "crewai", "custom"],
                axes=[AxisId.CONTEXT, AxisId.DX],
            ),
        ],
    )

    langchain = FrameworkProfile(
        id="langchain",
        name="LangChain / LangGraph",
        vendor="LangChain",
        language="Python / TypeScript",
        philosophy=(
            "Composable chains and graphs: explicit state machines for agent control flow, "
            "with a huge ecosystem of integrations."
        ),
        center_of_gravity="Graph / runnable composition layer",
        strengths=[
            "LangGraph gives durable, inspectable agent state machines",
            "Massive connector ecosystem",
            "Strong for productizing RAG + tools in apps",
        ],
        weaknesses=[
            "Easy to over-abstract; many apps become glue code",
            "Learning loop / skill distillation not a first-class product feature",
            "DX complexity at scale",
        ],
        architecture_notes=[
            "LCEL / Runnable graphs with checkpoints",
            "Tool calling via structured schemas",
            "Memory as optional stores rather than opinionated layered stack",
        ],
        urls={"docs": "https://python.langchain.com/"},
        scores=[
            _axis(AxisId.MEMORY, 3, "Flexible stores; less opinionated layering."),
            _axis(AxisId.SKILLS, 2, "Skills as patterns/prompts; not a unified skill OS."),
            _axis(AxisId.LEARNING, 2, "You build eval/feedback loops yourself."),
            _axis(AxisId.MULTI_AGENT, 4, "LangGraph multi-actor patterns are strong."),
            _axis(AxisId.GATEWAY, 2, "Library, not a messaging gateway product."),
            _axis(AxisId.SAFETY, 3, "Depends on app; callbacks and permissions exist."),
            _axis(AxisId.DX, 3, "Powerful but steep; many versions/APIs historically."),
            _axis(AxisId.TOOLING, 5, "Best-in-class tool/integration surface."),
            _axis(AxisId.CONTEXT, 4, "Prompt templates + message history utilities."),
            _axis(AxisId.EXTENSIBILITY, 5, "Huge plugin/integration market."),
        ],
        ideas=[
            DesignIdea(
                id="langchain-graph-state",
                title="Durable graph state with checkpoints",
                source_framework="langchain",
                summary="Model agent control flow as an explicit graph with resumable state.",
                why_it_matters="Debuggable long-running product agents.",
                transfer_cost="medium",
                integrate_into=["hermes", "openclaw", "custom"],
                axes=[AxisId.MULTI_AGENT, AxisId.DX],
            )
        ],
    )

    autogen = FrameworkProfile(
        id="autogen",
        name="AutoGen",
        vendor="Microsoft",
        language="Python",
        philosophy=(
            "Conversation-centric multi-agent: agents talk to each other with roles, "
            "and group chat patterns drive collaboration."
        ),
        center_of_gravity="Multi-agent conversation runtime",
        strengths=[
            "Mature multi-agent chat patterns",
            "Human-in-the-loop easy to express",
            "Good research/prototyping velocity",
        ],
        weaknesses=[
            "Conversation loops can burn tokens",
            "Less opinionated on procedural skill memory",
            "Product gateway story is secondary",
        ],
        architecture_notes=[
            "Conversable agents + GroupChat manager",
            "Tool use via function calling wrappers",
            "Strong for planner/critic/executor roleplays",
        ],
        urls={"docs": "https://microsoft.github.io/autogen/"},
        scores=[
            _axis(AxisId.MEMORY, 3, "Conversation history + optional stores."),
            _axis(AxisId.SKILLS, 2, "Skills usually prompt/role packs."),
            _axis(AxisId.LEARNING, 2, "No native Hermes-style distillation."),
            _axis(AxisId.MULTI_AGENT, 5, "Core value proposition."),
            _axis(AxisId.GATEWAY, 2, "Library-first."),
            _axis(AxisId.SAFETY, 3, "HITL helps; sandboxing is app-owned."),
            _axis(AxisId.DX, 3, "Good tutorials; evolving APIs."),
            _axis(AxisId.TOOLING, 4, "Solid tool registration patterns."),
            _axis(AxisId.CONTEXT, 3, "Role prompts + chat transcripts."),
            _axis(AxisId.EXTENSIBILITY, 4, "Extensions and agent teams."),
        ],
        ideas=[
            DesignIdea(
                id="autogen-groupchat",
                title="Role-based group chat with manager",
                source_framework="autogen",
                summary="Planner/researcher/critic/executor with an explicit speaker policy.",
                why_it_matters="Clearest multi-agent collaboration teaching tool.",
                transfer_cost="medium",
                integrate_into=["hermes", "crewai", "custom"],
                axes=[AxisId.MULTI_AGENT],
            )
        ],
    )

    crewai = FrameworkProfile(
        id="crewai",
        name="CrewAI",
        vendor="CrewAI",
        language="Python",
        philosophy=(
            "Crews of role-specialized agents with tasks and processes "
            "(sequential/hierarchical) optimized for business workflows."
        ),
        center_of_gravity="Crew / task process orchestration",
        strengths=[
            "Very approachable multi-agent DX for toB demos",
            "Clear Roles, Goals, Backstories, Tasks",
            "Process modes map to org charts",
        ],
        weaknesses=[
            "Less deep on learning loops and gateway ops",
            "Can feel template-heavy for systems research",
            "Memory/skills less sophisticated than Hermes",
        ],
        architecture_notes=[
            "Crew = agents + tasks + process",
            "Tools attached per agent",
            "Hierarchical process adds a manager agent",
        ],
        urls={"docs": "https://docs.crewai.com/"},
        scores=[
            _axis(AxisId.MEMORY, 3, "Short/long-term memory options; simpler than Hermes."),
            _axis(AxisId.SKILLS, 3, "Tools + prompts as skills; growing ecosystem."),
            _axis(AxisId.LEARNING, 2, "Limited native self-evolution."),
            _axis(AxisId.MULTI_AGENT, 5, "Crew metaphor is the product."),
            _axis(AxisId.GATEWAY, 2, "App framework, not channel gateway."),
            _axis(AxisId.SAFETY, 3, "Depends on deployment wrappers."),
            _axis(AxisId.DX, 5, "Fastest path to a multi-agent demo."),
            _axis(AxisId.TOOLING, 4, "Clean tool attachment model."),
            _axis(AxisId.CONTEXT, 3, "Role backstories drive prompting."),
            _axis(AxisId.EXTENSIBILITY, 3, "Integrations improving; less harness depth."),
        ],
        ideas=[
            DesignIdea(
                id="crewai-process",
                title="Sequential vs hierarchical crew processes",
                source_framework="crewai",
                summary="Encode org-like workflows as process modes with a manager agent.",
                why_it_matters="Maps cleanly to toB business scenarios.",
                transfer_cost="low",
                integrate_into=["autogen", "langchain", "custom"],
                axes=[AxisId.MULTI_AGENT, AxisId.DX],
            )
        ],
    )

    return {
        p.id: p
        for p in (hermes, openclaw, langchain, autogen, crewai)
    }


def _load_yaml_overrides() -> dict[str, FrameworkProfile]:
    if not DATA_DIR.exists():
        return {}
    out: dict[str, FrameworkProfile] = {}
    for path in DATA_DIR.glob("*.yaml"):
        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        profile = FrameworkProfile.model_validate(raw)
        out[profile.id] = profile
    return out


@lru_cache(maxsize=1)
def load_catalog() -> dict[str, FrameworkProfile]:
    catalog = _builtin_profiles()
    catalog.update(_load_yaml_overrides())
    return catalog


def list_frameworks() -> list[FrameworkProfile]:
    return sorted(load_catalog().values(), key=lambda p: p.name.lower())


def get_framework(framework_id: str) -> FrameworkProfile:
    catalog = load_catalog()
    key = framework_id.strip().lower()
    aliases = {
        "hermes-agent": "hermes",
        "langgraph": "langchain",
        "lang-chain": "langchain",
        "ms-autogen": "autogen",
        "crew": "crewai",
    }
    key = aliases.get(key, key)
    if key not in catalog:
        known = ", ".join(sorted(catalog))
        raise KeyError(f"Unknown framework '{framework_id}'. Known: {known}")
    return catalog[key]


def reload_catalog() -> dict[str, FrameworkProfile]:
    load_catalog.cache_clear()
    return load_catalog()
