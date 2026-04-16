"""Knowledge Store — persistent storage for domains, runs, convergences, findings."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Optional

from gnosis.config import Config
from gnosis.data.models import Domain, Convergence, Finding, Run


class Store:
    """JSON-file-based knowledge store."""

    def __init__(self, config: Config):
        self.config = config
        config.ensure_dirs()
        self.domains_dir = config.data_dir / "domains"
        self.runs_dir = config.data_dir / "runs"
        self.convergences_dir = config.data_dir / "convergences"
        self.findings_dir = config.data_dir / "findings"

    # --- Domains ---

    def save_domain(self, domain: Domain):
        path = self.domains_dir / f"{domain.id}.json"
        path.write_text(json.dumps(asdict(domain), indent=2))

    def load_domain(self, domain_id: str) -> Optional[Domain]:
        path = self.domains_dir / f"{domain_id}.json"
        if not path.exists():
            return None
        data = json.loads(path.read_text())
        return Domain(**data)

    def domain_is_surveyed(self, domain_id: str) -> bool:
        domain = self.load_domain(domain_id)
        return domain is not None and domain.surveyed

    def list_domains(self) -> list[Domain]:
        domains = []
        for path in sorted(self.domains_dir.glob("*.json")):
            data = json.loads(path.read_text())
            domains.append(Domain(**data))
        return domains

    # --- Runs ---

    def save_run(self, run: Run):
        path = self.runs_dir / f"{run.id}.json"
        path.write_text(json.dumps(asdict(run), indent=2, default=str))

    def load_run(self, run_id: str) -> Optional[Run]:
        path = self.runs_dir / f"{run_id}.json"
        if not path.exists():
            return None
        data = json.loads(path.read_text())
        return Run(**data)

    def latest_run(self) -> Optional[Run]:
        runs = sorted(self.runs_dir.glob("*.json"), key=lambda p: p.stat().st_mtime)
        if not runs:
            return None
        data = json.loads(runs[-1].read_text())
        return Run(**data)

    def list_runs(self) -> list[Run]:
        runs = []
        for path in sorted(self.runs_dir.glob("*.json"), key=lambda p: p.stat().st_mtime):
            data = json.loads(path.read_text())
            runs.append(Run(**data))
        return runs

    # --- Convergences (master registry) ---

    def save_convergence(self, conv: Convergence):
        path = self.convergences_dir / f"{conv.id}.json"
        path.write_text(json.dumps(asdict(conv), indent=2))

    def load_convergence(self, conv_id: str) -> Optional[Convergence]:
        path = self.convergences_dir / f"{conv_id}.json"
        if not path.exists():
            return None
        data = json.loads(path.read_text())
        return Convergence(**data)

    def list_convergences(self) -> list[Convergence]:
        convs = []
        for path in sorted(self.convergences_dir.glob("*.json")):
            data = json.loads(path.read_text())
            convs.append(Convergence(**data))
        return convs

    # --- Findings (master registry) ---

    def save_finding(self, finding: Finding):
        path = self.findings_dir / f"{finding.id}.json"
        path.write_text(json.dumps(asdict(finding), indent=2, default=str))

    def load_finding(self, finding_id: str) -> Optional[Finding]:
        path = self.findings_dir / f"{finding_id}.json"
        if not path.exists():
            return None
        data = json.loads(path.read_text())
        return Finding(**data)

    def list_findings(self) -> list[Finding]:
        findings = []
        for path in sorted(self.findings_dir.glob("*.json")):
            data = json.loads(path.read_text())
            findings.append(Finding(**data))
        return findings
