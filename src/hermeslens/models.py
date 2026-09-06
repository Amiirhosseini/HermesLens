"""Typed models for framework profiles, axes, and scorecards."""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator


class AxisId(str, Enum):
    MEMORY = "memory"
    SKILLS = "skills"
    LEARNING = "learning"
    MULTI_AGENT = "multi_agent"
    GATEWAY = "gateway"
    SAFETY = "safety"
    DX = "dx"
    TOOLING = "tooling"
    CONTEXT = "context"
    EXTENSIBILITY = "extensibility"


AXIS_LABELS: dict[AxisId, str] = {
    AxisId.MEMORY: "Memory architecture",
    AxisId.SKILLS: "Skills / procedural knowledge",
    AxisId.LEARNING: "Self-evolution / learning loop",
    AxisId.MULTI_AGENT: "Multi-agent collaboration",
    AxisId.GATEWAY: "Gateway / messaging / ops",
    AxisId.SAFETY: "Safety & isolation defaults",
    AxisId.DX: "Developer experience",
    AxisId.TOOLING: "Tools & function calling",
    AxisId.CONTEXT: "Context / prompt engineering",
    AxisId.EXTENSIBILITY: "Extensibility (plugins/MCP)",
}


class AxisScore(BaseModel):
    axis: AxisId
    score: int = Field(ge=1, le=5)
    rationale: str
    evidence: list[str] = Field(default_factory=list)

    @field_validator("score")
    @classmethod
    def clamp_score(cls, v: int) -> int:
        return max(1, min(5, int(v)))


class DesignIdea(BaseModel):
    id: str
    title: str
    source_framework: str
    summary: str
    why_it_matters: str
    transfer_cost: str = Field(description="low | medium | high")
    integrate_into: list[str] = Field(default_factory=list)
    axes: list[AxisId] = Field(default_factory=list)


class FrameworkProfile(BaseModel):
    id: str
    name: str
    vendor: str
    language: str
    philosophy: str
    center_of_gravity: str
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    architecture_notes: list[str] = Field(default_factory=list)
    urls: dict[str, str] = Field(default_factory=dict)
    scores: list[AxisScore] = Field(default_factory=list)
    ideas: list[DesignIdea] = Field(default_factory=list)

    def score_map(self) -> dict[AxisId, int]:
        return {s.axis: s.score for s in self.scores}

    def weighted_total(self, weights: dict[AxisId, float] | None = None) -> float:
        w = weights or {a: 1.0 for a in AxisId}
        total_w = 0.0
        acc = 0.0
        for s in self.scores:
            weight = float(w.get(s.axis, 1.0))
            acc += s.score * weight
            total_w += weight
        return round(acc / total_w, 3) if total_w else 0.0


class CompareRequest(BaseModel):
    frameworks: list[str] = Field(min_length=1)
    weights: dict[str, float] = Field(default_factory=dict)


class AxisDelta(BaseModel):
    axis: AxisId
    label: str
    scores: dict[str, int]
    leader: str | None
    spread: int


class CompareResult(BaseModel):
    frameworks: list[str]
    weighted_totals: dict[str, float]
    axes: list[AxisDelta]
    winner: str | None
    notes: list[str] = Field(default_factory=list)


class StealPlan(BaseModel):
    target: str
    sources: list[str]
    ideas: list[DesignIdea]
    patch_outline: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
