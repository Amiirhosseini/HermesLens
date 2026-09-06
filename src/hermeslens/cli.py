"""Typer CLI for HermesLens."""

from __future__ import annotations

import json
from typing import Optional

import typer
import uvicorn
from rich.console import Console
from rich.table import Table

from hermeslens.catalog import get_framework, list_frameworks
from hermeslens.dissect import brief, dissect
from hermeslens.models import CompareRequest
from hermeslens.scorecard import compare, scorecard_table
from hermeslens.steal import philosophy_diff, steal_ideas

app = typer.Typer(
    name="hermeslens",
    help="Agent framework dissection — scorecards, tradeoffs, steal-these-ideas.",
    no_args_is_help=True,
)
console = Console()


@app.command("list")
def list_cmd() -> None:
    """List catalogued frameworks."""
    table = Table(title="Framework catalog")
    table.add_column("ID")
    table.add_column("Name")
    table.add_column("Language")
    table.add_column("Center of gravity")
    for p in list_frameworks():
        table.add_row(p.id, p.name, p.language, p.center_of_gravity)
    console.print(table)


@app.command()
def show(framework: str) -> None:
    """Print a dissection brief for one framework."""
    console.print(brief(get_framework(framework)))


@app.command()
def score(
    frameworks: list[str] = typer.Argument(..., help="Framework IDs to compare"),
    preset: Optional[str] = typer.Option(None, help="Weight preset: rnd"),
    json_out: bool = typer.Option(False, "--json", help="Emit JSON"),
) -> None:
    """Compare frameworks on the architecture scorecard."""
    result = compare(CompareRequest(frameworks=frameworks), preset=preset)
    if json_out:
        console.print_json(data=result.model_dump(mode="json"))
        return

    table = Table(title="Architecture scorecard")
    table.add_column("Axis")
    for fid in result.frameworks:
        table.add_column(fid, justify="center")
    table.add_column("Leader")

    for axis in result.axes:
        row = [axis.label] + [str(axis.scores.get(f, "-")) for f in result.frameworks]
        row.append(axis.leader or "—")
        table.add_row(*row)
    console.print(table)

    totals = Table(title="Weighted totals")
    totals.add_column("Framework")
    totals.add_column("Score", justify="right")
    for fid, val in result.weighted_totals.items():
        totals.add_row(fid, f"{val:.3f}")
    console.print(totals)
    if result.winner:
        console.print(f"[bold]Winner (this weight set):[/bold] {result.winner}")
    for note in result.notes[:6]:
        console.print(f"• {note}")


@app.command()
def steal(
    target: str = typer.Argument(..., help="Framework to improve"),
    source: Optional[list[str]] = typer.Option(
        None, "--from", help="Source framework IDs (default: all others)"
    ),
    max_ideas: int = typer.Option(6, help="Max ideas to return"),
    json_out: bool = typer.Option(False, "--json"),
) -> None:
    """Generate a steal-these-ideas patch plan."""
    plan = steal_ideas(target, source, max_ideas=max_ideas)
    if json_out:
        console.print_json(data=plan.model_dump(mode="json"))
        return
    console.print(f"[bold]Target:[/bold] {plan.target}")
    console.print(f"[bold]Sources:[/bold] {', '.join(plan.sources)}")
    for idea in plan.ideas:
        console.print(
            f"\n[cyan]{idea.title}[/cyan] ({idea.transfer_cost}) ← {idea.source_framework}"
        )
        console.print(f"  {idea.summary}")
        console.print(f"  Why: {idea.why_it_matters}")
    console.print("\n[bold]Patch outline[/bold]")
    for line in plan.patch_outline:
        console.print(f"• {line}")


@app.command()
def diff(
    left: str,
    right: str,
) -> None:
    """Philosophy / CoG diff between two frameworks."""
    for line in philosophy_diff(left, right):
        console.print(f"• {line}")


@app.command()
def export(
    frameworks: list[str] = typer.Argument(...),
) -> None:
    """Export nested score table as JSON."""
    console.print_json(data=scorecard_table(frameworks))


@app.command("dissect")
def dissect_cmd(
    framework: str,
    json_out: bool = typer.Option(False, "--json"),
) -> None:
    """Full structured dissection."""
    data = dissect(framework)
    if json_out:
        console.print_json(data=data)
    else:
        console.print(brief(get_framework(framework)))
        console.print("\n[bold]Scores[/bold]")
        for s in data["scores"]:
            console.print(f"  {s['label']}: {s['score']}/5 — {s['rationale']}")


@app.command()
def serve(
    host: str = "127.0.0.1",
    port: int = 8765,
) -> None:
    """Run the FastAPI dissection API."""
    uvicorn.run("hermeslens.api:app", host=host, port=port, reload=False)


@app.command()
def mcp() -> None:
    """Run the MCP server (stdio)."""
    from hermeslens.agent.mcp_server import main

    main()


def main() -> None:
    app()


if __name__ == "__main__":
    main()
