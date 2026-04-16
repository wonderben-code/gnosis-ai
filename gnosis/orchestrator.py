"""Orchestrator — manages the three modes and the discovery pipeline."""

from __future__ import annotations

import itertools
from dataclasses import asdict
from typing import Optional

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from gnosis.api.claude import ClaudeAPI
from gnosis.ci.surveyor import Surveyor
from gnosis.ci.convergence import ConvergenceDetector
from gnosis.ci.meta import MetaConvergenceEngine
from gnosis.config import Config
from gnosis.data.models import (
    Convergence, Domain, Finding, Run, RunMode, RunStats,
    StrengthCategory, ConfidenceCategory,
)
from gnosis.data.store import Store
from gnosis.data.taxonomy import Taxonomy, FieldInfo
from gnosis.ea.validator import EAValidator

console = Console()


class Orchestrator:
    """The main Gnosis AI orchestrator — runs the full discovery pipeline."""

    def __init__(self, config: Config):
        self.config = config
        self.api = ClaudeAPI(config)
        self.store = Store(config)
        self.taxonomy = Taxonomy(config)
        self.surveyor = Surveyor(self.api, self.store)
        self.detector = ConvergenceDetector(self.api)
        self.meta_engine = MetaConvergenceEngine(self.api)
        self.validator = EAValidator(self.api)

    def _cost_status(self) -> str:
        """Return a formatted cost status line."""
        spent = self.api.stats.cost_usd
        limit = self.config.max_cost_usd
        pct = (spent / limit * 100) if limit > 0 else 0
        return f"${spent:.2f} / ${limit:.2f} ({pct:.0f}%)"

    # ─── GUIDED MODE ───

    def guided(
        self,
        question: str,
        domain_specs: list[str],
        max_depth: int = 5,
    ) -> Run:
        """Guided mode: question + domains → findings."""

        fields = []
        for spec in domain_specs:
            fields.extend(self.taxonomy.resolve(spec))

        run = Run(mode=RunMode.GUIDED.value, input_question=question, input_domains=[f.id for f in fields])
        stats = RunStats()

        console.print(f"\n[bold]Gnosis AI — Guided Mode[/bold]")
        console.print(f"Question: [italic]{question}[/italic]")
        console.print(f"Domains: {', '.join(f.name for f in fields)}")
        console.print(f"Budget: ${self.config.max_cost_usd:.2f}\n")

        # Step 1: Survey domains
        domains = self._survey_domains(fields, stats, question=question)
        console.print(f"[dim]  💰 Cost so far: {self._cost_status()}[/dim]\n")

        # Step 2: Detect convergences
        convergences = self._detect_convergences(domains, stats, run.id)
        console.print(f"[dim]  💰 Cost so far: {self._cost_status()}[/dim]\n")

        # Step 3: EA validate
        convergences = self._validate_convergences(convergences, stats)
        console.print(f"[dim]  💰 Cost so far: {self._cost_status()}[/dim]\n")

        # Step 4: Meta-converge
        findings = self._meta_converge(convergences, stats, run.id)

        # Assemble run
        run.convergences = [asdict(c) for c in convergences]
        run.findings = [asdict(f) for f in findings]
        stats.convergences_found = len(convergences)
        stats.findings_produced = len(findings)
        stats.api_calls = self.api.stats.calls
        stats.tokens_used = self.api.stats.input_tokens + self.api.stats.output_tokens
        stats.estimated_cost_usd = round(self.api.stats.cost_usd, 2)
        run.stats = asdict(stats)
        run.complete()

        # Save
        self.store.save_run(run)
        for c in convergences:
            self.store.save_convergence(c)
        for f in findings:
            self.store.save_finding(f)

        # Display summary
        self._display_summary(run)
        return run

    # ─── EXPLORATION MODE ───

    def explore(self, domain_specs: list[str]) -> Run:
        """Exploration mode: domains → convergences (no question)."""

        fields = []
        for spec in domain_specs:
            fields.extend(self.taxonomy.resolve(spec))

        run = Run(mode=RunMode.EXPLORATION.value, input_domains=[f.id for f in fields])
        stats = RunStats()

        console.print(f"\n[bold]Gnosis AI — Exploration Mode[/bold]")
        console.print(f"Domains: {', '.join(f.name for f in fields)}")
        console.print(f"Budget: ${self.config.max_cost_usd:.2f}\n")

        # Step 1: Survey domains (no question — open survey)
        domains = self._survey_domains(fields, stats)
        console.print(f"[dim]  💰 Cost so far: {self._cost_status()}[/dim]\n")

        # Step 2: Detect convergences
        convergences = self._detect_convergences(domains, stats, run.id)
        console.print(f"[dim]  💰 Cost so far: {self._cost_status()}[/dim]\n")

        # Step 3: EA validate
        convergences = self._validate_convergences(convergences, stats)
        console.print(f"[dim]  💰 Cost so far: {self._cost_status()}[/dim]\n")

        # Step 4: Meta-converge
        findings = self._meta_converge(convergences, stats, run.id)

        # Assemble run
        run.convergences = [asdict(c) for c in convergences]
        run.findings = [asdict(f) for f in findings]
        stats.convergences_found = len(convergences)
        stats.findings_produced = len(findings)
        stats.api_calls = self.api.stats.calls
        stats.tokens_used = self.api.stats.input_tokens + self.api.stats.output_tokens
        stats.estimated_cost_usd = round(self.api.stats.cost_usd, 2)
        run.stats = asdict(stats)
        run.complete()

        self.store.save_run(run)
        for c in convergences:
            self.store.save_convergence(c)
        for f in findings:
            self.store.save_finding(f)

        self._display_summary(run)
        return run

    # ─── AUTO MODE ───

    def auto(
        self,
        scope: str = "all",
        max_hours: Optional[float] = None,
        max_cost: Optional[float] = None,
    ) -> Run:
        """Auto mode: systematic discovery across all fields."""

        import time

        fields = self.taxonomy.resolve(scope)
        if max_hours:
            self.config.max_hours = max_hours
        if max_cost:
            self.config.max_cost_usd = max_cost

        run = Run(mode=RunMode.AUTO.value, input_domains=[f.id for f in fields])
        stats = RunStats()
        start_time = time.time()
        max_seconds = self.config.max_hours * 3600

        console.print(f"\n[bold]Gnosis AI — Auto Mode[/bold]")
        console.print(f"Scope: {len(fields)} fields")
        console.print(f"Limits: {self.config.max_hours}h / ${self.config.max_cost_usd}")
        console.print()

        # Step 1: Survey all domains
        domains = self._survey_domains(fields, stats)

        all_convergences = []
        all_findings = []
        cycle = 0

        # Generate all pairs
        pairs = list(itertools.combinations(domains, 2))
        console.print(f"[dim]Possible combinations: {len(pairs)}[/dim]\n")

        # Process in batches
        batch_size = 10
        pair_index = 0

        while pair_index < len(pairs):
            cycle += 1
            elapsed = time.time() - start_time

            # Check limits
            if elapsed > max_seconds:
                stats.termination_reason = f"max_hours ({self.config.max_hours}h)"
                break
            if self.api.stats.cost_usd >= self.config.max_cost_usd:
                stats.termination_reason = f"max_cost (${self.config.max_cost_usd})"
                break

            batch_end = min(pair_index + batch_size, len(pairs))
            batch = pairs[pair_index:batch_end]

            console.print(f"[bold]Cycle {cycle}[/bold] — pairs {pair_index+1}-{batch_end} of {len(pairs)}")

            cycle_convergences = []
            for da, db in batch:
                try:
                    convs = self.detector.detect(da, db)
                    for c in convs:
                        c.discovered_in_run = run.id
                    cycle_convergences.extend(convs)
                    stats.combinations_explored += 1
                except Exception as e:
                    console.print(f"[red]Error comparing {da.name} × {db.name}: {e}[/red]")

            # EA validate this batch
            for c in cycle_convergences:
                try:
                    self.validator.validate(c)
                except Exception:
                    pass

            # Filter by minimum strength
            strong = [c for c in cycle_convergences
                      if c.get_ea().confidence >= self.config.min_confidence]

            all_convergences.extend(strong)
            console.print(
                f"  Found {len(cycle_convergences)} convergences, "
                f"{len(strong)} passed EA (≥{self.config.min_confidence}) "
                f"| 💰 {self._cost_status()}"
            )

            # Check discovery rate
            if cycle > 2 and len(strong) == 0:
                stats.termination_reason = "discovery_rate_low"
                console.print("[yellow]Discovery rate dropped — continuing but noting.[/yellow]")

            pair_index = batch_end
            stats.cycles_completed = cycle

        # Meta-converge all findings
        if len(all_convergences) >= 2:
            console.print(f"\n[bold]Meta-convergence[/bold] across {len(all_convergences)} convergences...")
            all_findings = self.meta_engine.meta_converge(all_convergences)
            for f in all_findings:
                f.discovered_in_run = run.id

        if not stats.termination_reason:
            stats.termination_reason = "all_pairs_explored"

        # Assemble run
        run.convergences = [asdict(c) for c in all_convergences]
        run.findings = [asdict(f) for f in all_findings]
        stats.convergences_found = len(all_convergences)
        stats.high_strength = sum(1 for c in all_convergences if c.get_ea().strength >= 0.75)
        stats.medium_strength = sum(1 for c in all_convergences if 0.4 <= c.get_ea().strength < 0.75)
        stats.analogical = sum(1 for c in all_convergences if c.convergence_type == "structural_analogy")
        stats.findings_produced = len(all_findings)
        stats.meta_convergences = sum(1 for f in all_findings if f.is_meta_convergence)
        stats.api_calls = self.api.stats.calls
        stats.tokens_used = self.api.stats.input_tokens + self.api.stats.output_tokens
        stats.estimated_cost_usd = round(self.api.stats.cost_usd, 2)
        run.stats = asdict(stats)
        run.complete(stats.termination_reason)

        self.store.save_run(run)
        for c in all_convergences:
            self.store.save_convergence(c)
        for f in all_findings:
            self.store.save_finding(f)

        self._display_summary(run)
        return run

    # ─── SHARED PIPELINE STEPS ───

    def _survey_domains(
        self,
        fields: list[FieldInfo],
        stats: RunStats,
        question: str | None = None,
    ) -> list[Domain]:
        """Survey all domains, with caching."""
        domains = []

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Surveying domains...", total=len(fields))

            for field in fields:
                progress.update(task, description=f"Surveying {field.name}...")
                try:
                    domain = self.surveyor.survey(field, question=question)
                    domains.append(domain)
                    stats.domains_surveyed += 1
                    stats.results_catalogued += len(domain.results)
                except Exception as e:
                    console.print(f"[red]Survey failed for {field.name}: {e}[/red]")
                progress.advance(task)

        console.print(
            f"[green]Surveyed {len(domains)} domains, "
            f"{stats.results_catalogued} results catalogued[/green]\n"
        )
        return domains

    def _detect_convergences(
        self,
        domains: list[Domain],
        stats: RunStats,
        run_id: str,
    ) -> list[Convergence]:
        """Detect convergences across all domain pairs."""
        pairs = list(itertools.combinations(domains, 2))
        all_convs = []

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Detecting convergences...", total=len(pairs))

            for da, db in pairs:
                progress.update(
                    task,
                    description=f"Comparing {da.name} × {db.name}...",
                )
                try:
                    convs = self.detector.detect(da, db)
                    for c in convs:
                        c.discovered_in_run = run_id
                    all_convs.extend(convs)
                    stats.combinations_explored += 1
                except Exception as e:
                    console.print(f"[red]Error: {da.name} × {db.name}: {e}[/red]")
                progress.advance(task)

        console.print(f"[green]Found {len(all_convs)} convergences across {len(pairs)} pairs[/green]\n")
        return all_convs

    def _validate_convergences(
        self,
        convergences: list[Convergence],
        stats: RunStats,
    ) -> list[Convergence]:
        """EA validate all convergences."""
        if not convergences:
            return []

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("EA validation...", total=len(convergences))

            for conv in convergences:
                progress.update(task, description=f"Validating: {conv.structural_claim[:60]}...")
                try:
                    self.validator.validate(conv)
                except Exception as e:
                    console.print(f"[red]EA error: {e}[/red]")
                progress.advance(task)

        # Filter
        passed = [c for c in convergences if c.get_ea().confidence >= self.config.min_confidence]
        filtered = len(convergences) - len(passed)
        console.print(
            f"[green]EA validated: {len(passed)} passed, {filtered} filtered "
            f"(min confidence: {self.config.min_confidence})[/green]\n"
        )
        return passed

    def _meta_converge(
        self,
        convergences: list[Convergence],
        stats: RunStats,
        run_id: str,
    ) -> list[Finding]:
        """Run meta-convergence on validated convergences."""
        if len(convergences) < 2:
            return []

        console.print(f"[bold]Meta-convergence[/bold] across {len(convergences)} convergences...")
        findings = self.meta_engine.meta_converge(convergences)

        for f in findings:
            f.discovered_in_run = run_id

        stats.meta_convergences = len(findings)
        if findings:
            console.print(f"[green]Found {len(findings)} meta-convergence(s)[/green]\n")
        else:
            console.print("[dim]No meta-convergences found[/dim]\n")

        return findings

    # ─── DISPLAY ───

    def _display_summary(self, run: Run):
        """Display a summary of the run results."""
        stats = run.get_stats()
        convergences = run.get_convergences()
        findings = run.get_findings()

        console.print("\n" + "=" * 60)
        console.print(f"[bold]GNOSIS AI — Discovery Report[/bold]")
        console.print("=" * 60)
        console.print(f"Run: {run.id}")
        console.print(f"Mode: {run.mode} | Duration: {run.duration_human}")
        if run.input_question:
            console.print(f"Question: {run.input_question}")
        console.print(f"Cost: ${stats.estimated_cost_usd:.2f} | API calls: {stats.api_calls}")
        console.print()

        # Stats table
        table = Table(title="Summary")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="white")
        table.add_row("Domains surveyed", str(stats.domains_surveyed))
        table.add_row("Results catalogued", str(stats.results_catalogued))
        table.add_row("Combinations explored", str(stats.combinations_explored))
        table.add_row("Convergences found", str(stats.convergences_found))
        table.add_row("Meta-convergences", str(stats.meta_convergences))
        if stats.termination_reason:
            table.add_row("Terminated", stats.termination_reason)
        console.print(table)

        # Convergences
        if convergences:
            console.print(f"\n[bold]Convergences ({len(convergences)})[/bold]")
            for i, c in enumerate(convergences, 1):
                ea = c.get_ea()
                cat = ConfidenceCategory.from_score(ea.confidence).value.upper()
                strength = StrengthCategory.from_score(ea.strength).value.upper()
                domains = ", ".join(c.domain_names) if c.domain_names else ", ".join(c.domains)
                color = {"VERIFIED": "green", "SUPPORTED": "blue", "PRELIMINARY": "yellow"}.get(cat, "dim")
                console.print(f"\n  [{color}]{i}. [{cat}] {c.structural_claim}[/{color}]")
                console.print(f"     Fields: {domains}")
                console.print(f"     Type: {c.convergence_type} | Strength: {strength} | Confidence: {ea.confidence:.2f}")

        # Findings
        if findings:
            console.print(f"\n[bold]Meta-Convergence Findings ({len(findings)})[/bold]")
            for f in findings:
                term = f" ({f.coined_term})" if f.coined_term else ""
                console.print(f"\n  [bold magenta]Level {f.level}{term}[/bold magenta]")
                console.print(f"  {f.structural_finding}")

        console.print(f"\n[dim]Full data saved to: {self.config.data_dir / 'runs' / run.id}.json[/dim]")
        console.print()
