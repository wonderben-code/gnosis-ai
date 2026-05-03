"""CLI interface for Gnosis AI."""

from __future__ import annotations

from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from gnosis.config import Config

console = Console()


@click.group()
@click.option("--max-plan", is_flag=True, default=False,
              help="Use Claude Code CLI (Max plan) instead of API — $0 cost")
@click.pass_context
def cli(ctx, max_plan: bool):
    """Gnosis AI — Autonomous Knowledge Discovery"""
    ctx.ensure_object(dict)
    ctx.obj["config"] = Config.load()
    ctx.obj["use_max_plan"] = max_plan


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
    orch = Orchestrator(config, use_max_plan=ctx.obj.get("use_max_plan", False))
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
    orch = Orchestrator(config, use_max_plan=ctx.obj.get("use_max_plan", False))
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
    orch = Orchestrator(config, use_max_plan=ctx.obj.get("use_max_plan", False))
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


# ─── v2 COMMANDS ───


@cli.command()
@click.option("--strategy", "-s", default="cross-category-priority",
              type=click.Choice(["cross-category-priority", "exhaustive", "transitivity",
                                 "hub", "random"]),
              help="Search strategy")
@click.option("--scope", default="all", help="Field scope: 'all', a category, or comma-separated fields")
@click.option("--max-cost", type=float, default=50.0, help="Maximum API cost in USD")
@click.option("--max-hours", type=float, default=12.0, help="Maximum runtime in hours")
@click.option("--include-multi-field", is_flag=True, help="Also run multi-field after pairwise")
@click.pass_context
def codex(ctx, strategy: str, scope: str, max_cost: float, max_hours: float, include_multi_field: bool):
    """Codex mode: systematic cross-domain discovery with smart search strategies."""
    from gnosis.orchestrator import Orchestrator
    from gnosis.strategy import SearchStrategy, StrategyType
    from gnosis.data.taxonomy import Taxonomy
    from gnosis.data.corpus import CorpusManager
    from gnosis.data.store import Store

    config = ctx.obj["config"]
    config.max_cost_usd = max_cost
    config.max_hours = max_hours

    taxonomy = Taxonomy(config)
    store = Store(config)
    corpus = CorpusManager(store, taxonomy)

    # Map CLI strategy name to enum
    strategy_map = {
        "cross-category-priority": StrategyType.CROSS_CATEGORY_PRIORITY,
        "exhaustive": StrategyType.EXHAUSTIVE_PAIRWISE,
        "transitivity": StrategyType.TRANSITIVITY_PROBE,
        "hub": StrategyType.HUB_EXPANSION,
        "random": StrategyType.RANDOM_SAMPLE,
    }
    strat = strategy_map[strategy]

    search = SearchStrategy(taxonomy, explored_pairs=corpus.explored_pairs())

    # Generate tasks based on strategy
    if strat == StrategyType.TRANSITIVITY_PROBE:
        all_convs = corpus.all_convergences()
        tasks = search.generate_tasks(strat, convergences=all_convs)
    elif strat == StrategyType.HUB_EXPANSION:
        all_convs = corpus.all_convergences()
        tasks = search.generate_tasks(strat, convergences=all_convs)
    else:
        tasks = search.generate_tasks(strat)

    if not tasks:
        console.print("[yellow]No tasks generated. All pairs may already be explored.[/yellow]")
        return

    summary = search.summary(tasks)
    console.print(f"\n[bold]Gnosis AI — Codex Mode[/bold]")
    console.print(f"Strategy: {strategy}")
    console.print(f"Tasks: {summary['total_tasks']} ({summary['cross_category']} cross, {summary['within_category']} within, {summary['multi_field']} multi-field)")
    console.print(f"Budget: {max_hours}h / ${max_cost}")
    console.print(f"Top priority: {summary['top_priority']:.2f}")
    console.print()

    # Execute via the orchestrator
    orch = Orchestrator(config, use_max_plan=ctx.obj.get("use_max_plan", False))
    orch.auto(scope=scope, max_hours=max_hours, max_cost=max_cost)


@cli.command()
@click.option("--strategies", "-s", default="by_domain,by_category,holistic",
              help="Comma-separated grouping strategies")
@click.option("--max-levels", type=int, default=5, help="Maximum cascade levels")
@click.option("--cross-level", is_flag=True, default=True, help="Include cross-level comparisons")
@click.pass_context
def cascade(ctx, strategies: str, max_levels: int, cross_level: bool):
    """Run recursive cascade on the full convergence corpus."""
    from gnosis.data.store import Store
    from gnosis.data.taxonomy import Taxonomy
    from gnosis.data.corpus import CorpusManager
    from gnosis.ci.cascade import CascadeEngine, GroupingStrategy
    from gnosis.api.claude import create_api

    config = ctx.obj["config"]
    store = Store(config)
    taxonomy = Taxonomy(config)
    corpus = CorpusManager(store, taxonomy)
    api = create_api(config, use_max_plan=ctx.obj.get("use_max_plan", False))

    # Parse strategies
    strategy_map = {s.value: s for s in GroupingStrategy}
    strat_list = []
    for s in strategies.split(","):
        s = s.strip()
        if s in strategy_map:
            strat_list.append(strategy_map[s])
        else:
            console.print(f"[red]Unknown strategy: {s}. Available: {', '.join(strategy_map.keys())}[/red]")
            return

    all_convs = corpus.all_convergences()
    if len(all_convs) < 2:
        console.print("[yellow]Need at least 2 convergences for cascade.[/yellow]")
        return

    console.print(f"\n[bold]Gnosis AI — Recursive Cascade[/bold]")
    console.print(f"Convergences: {len(all_convs)}")
    console.print(f"Strategies: {', '.join(s.value for s in strat_list)}")
    console.print(f"Max levels: {max_levels}")
    console.print(f"Cross-level: {'yes' if cross_level else 'no'}")
    console.print()

    engine = CascadeEngine(api, field_category_fn=corpus.field_category)
    result = engine.run_cascade(
        all_convs,
        strategies=strat_list,
        max_levels=max_levels,
        cross_level=cross_level,
    )

    # Display results
    console.print(f"\n[bold]Cascade Results[/bold]")
    console.print(f"Levels reached: {result.levels_reached}")
    console.print(f"Fixed point: {'YES' if result.fixed_point_reached else 'no'}")
    console.print(f"Total findings: {len(result.findings)}")
    console.print(f"Strategy breakdown: {result.strategy_counts}")

    for f in result.findings:
        term = f" ({f.coined_term})" if f.coined_term else ""
        strategy_tag = f" [{f.grouping_strategy}]" if f.grouping_strategy else ""
        console.print(f"\n  [bold magenta]Level {f.level}{term}{strategy_tag}[/bold magenta]")
        console.print(f"  {f.structural_finding}")

    # Save findings
    for f in result.findings:
        store.save_finding(f)
    console.print(f"\n[dim]Saved {len(result.findings)} findings to store[/dim]")


@cli.group()
@click.pass_context
def corpus(ctx):
    """Corpus commands — query and analyse the convergence corpus."""
    pass


@corpus.command()
@click.pass_context
def stats(ctx):
    """Show corpus statistics."""
    from gnosis.data.store import Store
    from gnosis.data.taxonomy import Taxonomy
    from gnosis.data.corpus import CorpusManager

    config = ctx.obj["config"]
    store = Store(config)
    taxonomy = Taxonomy(config)
    corpus_mgr = CorpusManager(store, taxonomy)

    s = corpus_mgr.stats()

    table = Table(title="Convergence Corpus")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="white")
    table.add_row("Total convergences", str(s["total_convergences"]))
    table.add_row("Negative (no convergence)", str(s["total_negative"]))
    table.add_row("Fields explored", str(s["total_fields_explored"]))
    table.add_row("Category pairs", str(s["total_category_pairs"]))
    table.add_row("Runs", str(s["total_runs"]))
    console.print(table)

    if s["by_confidence"]:
        console.print("\n[bold]By confidence:[/bold]")
        for tier, count in s["by_confidence"].items():
            console.print(f"  {tier}: {count}")

    if s["by_comparison_type"]:
        console.print("\n[bold]By comparison type:[/bold]")
        for t, count in s["by_comparison_type"].items():
            console.print(f"  {t}: {count}")

    if s["top_category_pairs"]:
        console.print("\n[bold]Top category pairs:[/bold]")
        for pair, count in s["top_category_pairs"]:
            console.print(f"  {pair}: {count}")


@corpus.command()
@click.option("--min", "min_convs", type=int, default=3, help="Minimum convergences to qualify as hub")
@click.pass_context
def hubs(ctx, min_convs: int):
    """Show hub fields (fields with the most convergences)."""
    from gnosis.data.store import Store
    from gnosis.data.taxonomy import Taxonomy
    from gnosis.data.corpus import CorpusManager

    config = ctx.obj["config"]
    store = Store(config)
    taxonomy = Taxonomy(config)
    corpus_mgr = CorpusManager(store, taxonomy)

    hub_list = corpus_mgr.hub_fields(min_convergences=min_convs)
    if not hub_list:
        console.print(f"[dim]No fields with {min_convs}+ convergences.[/dim]")
        return

    table = Table(title=f"Hub Fields (≥{min_convs} convergences)")
    table.add_column("Field", style="cyan")
    table.add_column("Category", style="dim")
    table.add_column("Convergences", style="bold")

    for field_id, count in hub_list:
        fi = taxonomy.get(field_id)
        name = fi.name if fi else field_id
        cat = fi.category if fi else "?"
        table.add_row(name, cat, str(count))

    console.print(table)


@corpus.command()
@click.pass_context
def transitivity(ctx):
    """Show transitivity candidates (A↔B and B↔C exist, but not A↔C)."""
    from gnosis.data.store import Store
    from gnosis.data.taxonomy import Taxonomy
    from gnosis.data.corpus import CorpusManager

    config = ctx.obj["config"]
    store = Store(config)
    taxonomy = Taxonomy(config)
    corpus_mgr = CorpusManager(store, taxonomy)

    candidates = corpus_mgr.transitivity_candidates()
    if not candidates:
        console.print("[dim]No transitivity candidates found.[/dim]")
        return

    console.print(f"\n[bold]Transitivity Candidates ({len(candidates)})[/bold]")
    console.print("[dim]A↔B and B↔C converge, but A↔C hasn't been explored[/dim]\n")

    for a, b, c in candidates[:20]:
        fa, fb, fc = taxonomy.get(a), taxonomy.get(b), taxonomy.get(c)
        a_name = fa.name if fa else a
        b_name = fb.name if fb else b
        c_name = fc.name if fc else c
        console.print(f"  {a_name} ↔ [bold]{b_name}[/bold] ↔ {c_name}")

    if len(candidates) > 20:
        console.print(f"\n[dim]... and {len(candidates) - 20} more[/dim]")


@corpus.command()
@click.pass_context
def negatives(ctx):
    """Show negative convergences (informative absences)."""
    from gnosis.data.store import Store
    from gnosis.data.taxonomy import Taxonomy
    from gnosis.data.corpus import CorpusManager

    config = ctx.obj["config"]
    store = Store(config)
    taxonomy = Taxonomy(config)
    corpus_mgr = CorpusManager(store, taxonomy)

    negs = corpus_mgr.negatives()
    if not negs:
        console.print("[dim]No negative convergences recorded yet.[/dim]")
        return

    console.print(f"\n[bold]Negative Convergences ({len(negs)})[/bold]")
    for n in negs:
        domains = ", ".join(n.domain_names) if n.domain_names else ", ".join(n.domains)
        console.print(f"  {domains}: {n.structural_claim}")


@corpus.command()
@click.option("--format", "-f", "fmt", type=click.Choice(["logos", "json"]), default="json")
@click.option("--output", "-o", default=None, help="Output file path")
@click.pass_context
def export(ctx, fmt: str, output: str | None):
    """Export corpus in Logos-compatible format."""
    import json
    from dataclasses import asdict
    from gnosis.data.store import Store
    from gnosis.data.taxonomy import Taxonomy
    from gnosis.data.corpus import CorpusManager

    config = ctx.obj["config"]
    store = Store(config)
    taxonomy = Taxonomy(config)
    corpus_mgr = CorpusManager(store, taxonomy)

    convs = corpus_mgr.all_convergences()
    data = [asdict(c) for c in convs]

    if fmt == "logos":
        # Filter to formalisable convergences
        data = [d for d in data if d.get("formalisability_hint") in ("high", "medium", "")]

    json_str = json.dumps(data, indent=2)

    if output:
        Path(output).write_text(json_str)
        console.print(f"[green]Exported {len(data)} convergences to {output}[/green]")
    else:
        console.print(json_str)
