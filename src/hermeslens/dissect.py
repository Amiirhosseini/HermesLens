"""Dissection summaries for a single framework."""

from __future__ import annotations

from hermeslens.catalog import get_framework
from hermeslens.models import AXIS_LABELS, FrameworkProfile


def dissect(framework_id: str) -> dict:
    p = get_framework(framework_id)
    return {
        "id": p.id,
        "name": p.name,
        "vendor": p.vendor,
        "language": p.language,
        "philosophy": p.philosophy,
        "center_of_gravity": p.center_of_gravity,
        "strengths": p.strengths,
        "weaknesses": p.weaknesses,
        "architecture_notes": p.architecture_notes,
        "urls": p.urls,
        "scores": [
            {
                "axis": s.axis.value,
                "label": AXIS_LABELS[s.axis],
                "score": s.score,
                "rationale": s.rationale,
                "evidence": s.evidence,
            }
            for s in p.scores
        ],
        "ideas": [i.model_dump() for i in p.ideas],
        "weighted_total": p.weighted_total(),
    }


def brief(profile: FrameworkProfile) -> str:
    lines = [
        f"# {profile.name} ({profile.id})",
        f"Vendor: {profile.vendor} | Language: {profile.language}",
        f"Center of gravity: {profile.center_of_gravity}",
        "",
        profile.philosophy,
        "",
        "## Strengths",
        *[f"- {s}" for s in profile.strengths],
        "",
        "## Weaknesses",
        *[f"- {w}" for w in profile.weaknesses],
        "",
        "## Architecture notes",
        *[f"- {n}" for n in profile.architecture_notes],
    ]
    return "\n".join(lines)
