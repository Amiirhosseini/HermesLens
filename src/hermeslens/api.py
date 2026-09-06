"""FastAPI surface for HermesLens."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from hermeslens import __version__
from hermeslens.catalog import get_framework, list_frameworks
from hermeslens.dissect import dissect
from hermeslens.models import CompareRequest, StealPlan
from hermeslens.scorecard import compare
from hermeslens.steal import philosophy_diff, steal_ideas

app = FastAPI(
    title="HermesLens",
    description="Agent framework dissection API",
    version=__version__,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    return {"ok": True, "version": __version__}


@app.get("/frameworks")
def frameworks() -> list[dict]:
    return [
        {
            "id": p.id,
            "name": p.name,
            "vendor": p.vendor,
            "language": p.language,
            "center_of_gravity": p.center_of_gravity,
        }
        for p in list_frameworks()
    ]


@app.get("/frameworks/{framework_id}")
def framework_detail(framework_id: str) -> dict:
    try:
        return dissect(framework_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/compare")
def compare_endpoint(req: CompareRequest, preset: str | None = Query(None)) -> dict:
    try:
        return compare(req, preset=preset).model_dump(mode="json")
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/steal")
def steal_endpoint(
    target: str,
    sources: str | None = Query(None, description="Comma-separated source IDs"),
    max_ideas: int = 6,
) -> StealPlan:
    try:
        src = [s.strip() for s in sources.split(",")] if sources else None
        return steal_ideas(target, src, max_ideas=max_ideas)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/diff")
def diff_endpoint(left: str, right: str) -> dict:
    try:
        return {"left": left, "right": right, "lines": philosophy_diff(left, right)}
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/catalog/raw/{framework_id}")
def raw_profile(framework_id: str) -> dict:
    try:
        return get_framework(framework_id).model_dump(mode="json")
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
