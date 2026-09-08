"""Scorecard comparison engine."""

from __future__ import annotations

from hermeslens.catalog import get_framework
from hermeslens.models import (
    AXIS_LABELS,
    AxisDelta,
    AxisId,
    CompareRequest,
    CompareResult,
)

DEFAULT_WEIGHTS: dict[AxisId, float] = {axis: 1.0 for axis in AxisId}

# Agent R&D bias: emphasize learning, skills, memory, multi-agent, DX
RND_WEIGHTS: dict[AxisId, float] = {
    AxisId.MEMORY: 1.2,
    AxisId.SKILLS: 1.3,
    AxisId.LEARNING: 1.5,
    AxisId.MULTI_AGENT: 1.3,
    AxisId.GATEWAY: 1.0,
    AxisId.SAFETY: 1.1,
    AxisId.DX: 1.2,
    AxisId.TOOLING: 1.0,
    AxisId.CONTEXT: 1.2,
    AxisId.EXTENSIBILITY: 1.1,
}


def parse_weights(raw: dict[str, float] | None, preset: str | None = None) -> dict[AxisId, float]:
    if preset == "rnd":
        base = dict(RND_WEIGHTS)
    else:
        base = dict(DEFAULT_WEIGHTS)
    if not raw:
        return base
    for key, value in raw.items():
        try:
            axis = AxisId(key)
        except ValueError:
            continue
        base[axis] = float(value)
    return base


def compare(req: CompareRequest, preset: str | None = None) -> CompareResult:
    ids = [f.strip().lower() for f in req.frameworks]
    profiles = [get_framework(i) for i in ids]
    weights = parse_weights(req.weights, preset=preset)

    totals = {p.id: p.weighted_total(weights) for p in profiles}
    winner = max(totals, key=totals.get) if totals else None

    axes: list[AxisDelta] = []
    notes: list[str] = []
    for axis in AxisId:
        scores = {p.id: p.score_map().get(axis, 0) for p in profiles}
        if not scores:
            continue
        leader = max(scores, key=scores.get)
        spread = max(scores.values()) - min(scores.values())
        axes.append(
            AxisDelta(
                axis=axis,
                label=AXIS_LABELS[axis],
                scores=scores,
                leader=leader if spread > 0 else None,
                spread=spread,
            )
        )
        if spread >= 2:
            notes.append(
                f"{AXIS_LABELS[axis]}: {leader} leads "
                f"({scores[leader]}/5 vs gap {spread})."
            )

    for p in profiles:
        notes.append(f"{p.name} CoG: {p.center_of_gravity}")

    return CompareResult(
        frameworks=[p.id for p in profiles],
        weighted_totals=totals,
        axes=axes,
        winner=winner,
        notes=notes,
    )


def scorecard_table(framework_ids: list[str]) -> dict[str, dict[str, int]]:
    """Return nested map axis_label -> framework_id -> score."""
    profiles = [get_framework(i) for i in framework_ids]
    table: dict[str, dict[str, int]] = {}
    for axis in AxisId:
        table[AXIS_LABELS[axis]] = {
            p.id: p.score_map().get(axis, 0) for p in profiles
        }
    return table
