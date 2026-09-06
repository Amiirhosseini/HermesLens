"""Core unit tests for HermesLens."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from hermeslens.api import app as api_app
from hermeslens.catalog import get_framework, list_frameworks
from hermeslens.dissect import brief, dissect
from hermeslens.models import AxisId, CompareRequest
from hermeslens.scorecard import RND_WEIGHTS, compare, parse_weights
from hermeslens.steal import philosophy_diff, steal_ideas


def test_catalog_has_core_frameworks() -> None:
    ids = {p.id for p in list_frameworks()}
    assert {"hermes", "openclaw", "langchain", "autogen", "crewai"} <= ids


def test_hermes_learning_beats_openclaw() -> None:
    hermes = get_framework("hermes")
    openclaw = get_framework("openclaw")
    assert hermes.score_map()[AxisId.LEARNING] > openclaw.score_map()[AxisId.LEARNING]


def test_openclaw_gateway_beats_hermes() -> None:
    hermes = get_framework("hermes")
    openclaw = get_framework("openclaw")
    assert openclaw.score_map()[AxisId.GATEWAY] > hermes.score_map()[AxisId.GATEWAY]


def test_compare_hermes_openclaw() -> None:
    result = compare(CompareRequest(frameworks=["hermes", "openclaw"]), preset="rnd")
    assert set(result.frameworks) == {"hermes", "openclaw"}
    assert result.winner in {"hermes", "openclaw"}
    assert len(result.axes) == len(AxisId)
    assert any("CoG" in n for n in result.notes)


def test_aliases() -> None:
    assert get_framework("hermes-agent").id == "hermes"
    assert get_framework("langgraph").id == "langchain"


def test_unknown_framework() -> None:
    with pytest.raises(KeyError):
        get_framework("not-a-real-framework")


def test_steal_ideas_prefers_low_cost() -> None:
    plan = steal_ideas("hermes", ["openclaw"], max_ideas=5)
    assert plan.target == "hermes"
    assert plan.ideas
    costs = [i.transfer_cost for i in plan.ideas]
    assert costs == sorted(costs, key=lambda c: {"low": 0, "medium": 1, "high": 2}[c])


def test_steal_into_openclaw_from_hermes() -> None:
    plan = steal_ideas("openclaw", ["hermes"], max_ideas=5)
    assert any(i.source_framework == "hermes" for i in plan.ideas)
    assert plan.patch_outline


def test_philosophy_diff() -> None:
    lines = philosophy_diff("hermes", "openclaw")
    assert len(lines) >= 4
    assert any("Center of gravity" in line for line in lines)


def test_dissect_structure() -> None:
    data = dissect("hermes")
    assert data["id"] == "hermes"
    assert data["scores"]
    assert "weighted_total" in data
    text = brief(get_framework("hermes"))
    assert "Hermes" in text


def test_parse_weights_rnd() -> None:
    w = parse_weights(None, preset="rnd")
    assert w[AxisId.LEARNING] == RND_WEIGHTS[AxisId.LEARNING]


def test_api_health_and_compare() -> None:
    client = TestClient(api_app)
    assert client.get("/health").json()["ok"] is True
    fw = client.get("/frameworks").json()
    assert len(fw) >= 5
    detail = client.get("/frameworks/hermes")
    assert detail.status_code == 200
    cmp = client.post("/compare", json={"frameworks": ["hermes", "openclaw"]}, params={"preset": "rnd"})
    assert cmp.status_code == 200
    body = cmp.json()
    assert "weighted_totals" in body
    steal = client.get("/steal", params={"target": "openclaw", "sources": "hermes"})
    assert steal.status_code == 200
    assert steal.json()["ideas"]


def test_api_404() -> None:
    client = TestClient(api_app)
    assert client.get("/frameworks/nope").status_code == 404
