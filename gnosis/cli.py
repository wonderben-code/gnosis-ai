"""CLI interface for Gnosis AI."""

from __future__ import annotations

from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from gnosis.config import Config

console = Console()


@click.group()
@click.pass_context
def cli(ctx):
    """Gnosis AI — Autonomous Knowledge Discovery"""
    ctx.ensure_object(dict)
    ctx.obj["config"] = Config.load()


@cli.command()
@click.option("--question", "-q", required=True, help="The foundational question to investigate")
@click.option("--domains", "-d", required=True, help="Comma-separated domain IDs or categories")
@click.option("--max-depth", default=5, help="Maximum descent depth")
@click.option("--max-cost", type=float, default=None, help="Maximum API cost in USD")
@click.pass_context
def guided(ctx, question: str, domains: str, max_depth: int, max_cost: float | None):
    """Guided mode: question + domains → findings."""
    from gnosis.orchestrator import Orchestrator

    config = ctx.obj["config"]
    if max_cost:
        config.max_cost_usd = max_cost
    orch = Orchestrator(config)
    domain_list = [d.strip() for d in domains.split(",")]
    orch.guided(question=question, domain_specs=domain_list, max_depth=max_depth)


@cli.command()
@click.option("--domains", "-d", required=True, help="Comma-separated domain IDs or categories")
@click.option("--max-cost", type=float, default=None, help="Maximum API cost in USD")
@click.pass_context
def explore(ctx, domains: str, max_cost: float | None):
    """Exploration mode: domains → convergences (no question needed)."""
    from gnosis.orchestrator import Orchestrator

    config = ctx.obj["config"]
    if max_cost:
        config.max_cost_usd = max_cost
    orch = Orchestrator(config)
    domain_list = [d.strip() for d in domains.split(",")]
    orch.explore(domain_specs=domain_list)


@cli.command()
@click.option("--scope", "-s", default="all", help="Scope: 'all', a category, or comma-separated fields")
@click.option("--max-hours", type=float, default=None, help="Maximum runtime in hours")
@click.option("--max-cost", type=float, default=None, help="Maximum API cost in USD")
@click.pass_context
def auto(ctx, scope: str, max_hours: float | None, max_cost: float | None):
    """Auto mode: systematic discovery across all fields."""
    from gnosis.orchestrator import Orchestrator

    config = ctx.obj["config"]
    orch = Orchestrator(config)
    orch.auto(scope=scope, max_hours=max_hours, max_cost=max_cost)


@cli.command()
@click.option("--run", "-r", default=None, help="Run ID (default: latest)")
@click.option("--format", "-f", "fmt", type=click.Choice(["markdown", "json"]), default="markdown")
@click.option("--output", "-o", default=None, help="Output file path")
@click.pass_context
def report(ctx, run: str | None, fmt: str, output: str | None):
    """View or export a discovery report."""
    from gnosis.data.store import Store
    from gnosis.reports.generator import generate_markdown, generate_json, save_report

    config = ctx.obj["config"]
    store = Store(config)

    if run:
        run_obj = store.load_run(run)
    else:
        run_obj = store.latest_run()

    if not run_obj:
        console.print("[red]No runs found.[/red]")
        return

    if output:
        save_report(run_obj, Path(output), fmt)
        console.print(f"[green]Report saved to {output}[/green]")
    else:
        if fmt == "markdown":
            console.print(generate_markdown(run_obj))
        else:
            console.print(generate_json(run_obj))


@cli.command()
@click.pass_context
def runs(ctx):
    """List all discovery runs."""
    from gnosis.data.store import Store

    config = ctx.obj["config"]
    store = Store(config)
    all_runs = store.list_runs()

    if not all_runs:
        console.print("[dim]No runs yet. Start with: gnosis guided -q 'Your question' -d 'domain1,domain2'[/dim]")
        return

    table = Table(title="Discovery Runs")
    table.add_column("ID", style="cyan")
    table.add_column("Mode")
    table.add_column("Domains")
    table.add_column("Convergences")
    table.add_column("Duration")
    table.add_column("Cost")

    for r in all_runs:
        stats = r.get_stats()
        table.add_row(
            r.id,
            r.mode,
            str(stats.domains_surveyed),
            str(stats.convergences_found),
            r.duration_human,
            f"${stats.estimated_cost_usd:.2f}",
        )

    console.print(table)


@cli.command()
@click.option("--category", "-c", default=None, help="Filter by category")
@click.pass_context
def fields(ctx, category: str | None):
    """View the field taxonomy."""
    from gnosis.data.taxonomy import Taxonomy

    config = ctx.obj["config"]
    taxonomy = Taxonomy(config)

    if category:
        matching = {k: v for k, v in taxonomy.categories.items()
                    if k.lower() == category.lower()}
    else:
        matching = taxonomy.categories

    for cat_name, cat_fields in matching.items():
        console.print(f"\n[bold]{cat_name}[/bold] ({len(cat_fields)} fields)")
        for f in cat_fields:
            console.print(f"  [cyan]{f.id:<28}[/cyan] {f.name}")

    console.print(f"\n[dim]Total: {taxonomy.count} fields[/dim]")


@cli.command()
@click.argument("domain_id")
@click.pass_context
def survey(ctx, domain_id: str):
    """View a cached domain survey."""
    from gnosis.data.store import Store

    config = ctx.obj["config"]
    store = Store(config)
    domain = store.load_domain(domain_id)

    if not domain:
        console.print(f"[red]Domain '{domain_id}' not surveyed yet.[/red]")
        return

    console.print(f"\n[bold]{domain.name}[/bold] ({domain.category})")
    console.print(f"[dim]{domain.description}[/dim]")
    console.print(f"\n[italic]Structural conclusion:[/italic] {domain.structural_conclusion}\n")

    results = domain.get_results()
    table = Table(title=f"Established Results ({len(results)})")
    table.add_column("#", style="dim")
    table.add_column("Result")
    table.add_column("Status", style="cyan")
    table.add_column("Structural Conclusion")

    for i, r in enumerate(results, 1):
        table.add_row(
            str(i),
            f"{r.name} ({r.authors})",
            r.epistemic_status,
            r.structural_conclusion[:80] + "..." if len(r.structural_conclusion) > 80 else r.structural_conclusion,
        )

    console.print(table)
