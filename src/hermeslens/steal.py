"""Steal-these-ideas planner — transfer design patterns across frameworks."""

from __future__ import annotations

from hermeslens.catalog import get_framework, list_frameworks
from hermeslens.models import DesignIdea, StealPlan


COST_RANK = {"low": 0, "medium": 1, "high": 2}


def _compatible(idea: DesignIdea, target_id: str) -> bool:
    destinations = {d.lower() for d in idea.integrate_into}
    if not destinations:
        return True
    return target_id in destinations or "custom" in destinations


def steal_ideas(
    target: str,
    sources: list[str] | None = None,
    *,
    max_ideas: int = 8,
    prefer_low_cost: bool = True,
) -> StealPlan:
    target_profile = get_framework(target)
    if sources:
        source_profiles = [get_framework(s) for s in sources]
    else:
        source_profiles = [p for p in list_frameworks() if p.id != target_profile.id]

    ideas: list[DesignIdea] = []
    for src in source_profiles:
        for idea in src.ideas:
            if _compatible(idea, target_profile.id):
                ideas.append(idea)

    if not ideas:
        for src in source_profiles:
            ideas.extend(src.ideas)

    def sort_key(idea: DesignIdea) -> tuple[int, str]:
        cost = COST_RANK.get(idea.transfer_cost.lower(), 9)
        return (cost if prefer_low_cost else -cost, idea.title.lower())

    ideas_sorted = sorted(ideas, key=sort_key)[:max_ideas]

    patch_outline = [
        f"[{idea.transfer_cost}] {idea.title} ← {idea.source_framework}: {idea.summary}"
        for idea in ideas_sorted
    ]
    patch_outline.append(
        f"Target {target_profile.name} CoG remains: {target_profile.center_of_gravity}"
    )
    patch_outline.append(
        "Validate each transfer with a minimal spike: one module, one test, one demo knob."
    )

    return StealPlan(
        target=target_profile.id,
        sources=[p.id for p in source_profiles],
        ideas=ideas_sorted,
        patch_outline=patch_outline,
        metadata={
            "target_name": target_profile.name,
            "idea_count": len(ideas_sorted),
        },
    )


def philosophy_diff(left: str, right: str) -> list[str]:
    a = get_framework(left)
    b = get_framework(right)
    return [
        f"{a.name}: {a.philosophy}",
        f"{b.name}: {b.philosophy}",
        f"Center of gravity — {a.id}: {a.center_of_gravity}",
        f"Center of gravity — {b.id}: {b.center_of_gravity}",
        f"Key strength gap — {a.id}: {a.strengths[0] if a.strengths else 'n/a'}",
        f"Key strength gap — {b.id}: {b.strengths[0] if b.strengths else 'n/a'}",
    ]
