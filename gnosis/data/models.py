"""Core data models for Gnosis AI."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


class EpistemicStatus(str, Enum):
    PROVEN_THEOREM = "proven_theorem"
    EXPERIMENTALLY_CONFIRMED = "experimentally_confirmed"
    ESTABLISHED_FRAMEWORK = "established_framework"
    WELL_SUPPORTED_CONJECTURE = "well_supported_conjecture"
    CANDIDATE_THEORY = "candidate_theory"
    CONJECTURAL = "conjectural"
    NUMERICAL_RESULT = "numerical_result"

    @property
    def weight(self) -> float:
        return {
            self.PROVEN_THEOREM: 1.0,
            self.EXPERIMENTALLY_CONFIRMED: 1.0,
            self.ESTABLISHED_FRAMEWORK: 0.85,
            self.WELL_SUPPORTED_CONJECTURE: 0.6,
            self.CANDIDATE_THEORY: 0.4,
            self.CONJECTURAL: 0.2,
            self.NUMERICAL_RESULT: 0.7,
        }[self]


class ConvergenceType(str, Enum):
    FORMAL = "formal"
    STRUCTURAL_ANALOGY = "structural_analogy"

    @property
    def weight(self) -> float:
        return {self.FORMAL: 1.0, self.STRUCTURAL_ANALOGY: 0.6}[self]


class ConfidenceCategory(str, Enum):
    VERIFIED = "verified"          # >= 0.80
    SUPPORTED = "supported"        # 0.60 - 0.79
    PRELIMINARY = "preliminary"    # 0.40 - 0.59
    SPECULATIVE = "speculative"    # < 0.40

    @classmethod
    def from_score(cls, score: float) -> ConfidenceCategory:
        if score >= 0.80:
            return cls.VERIFIED
        elif score >= 0.60:
            return cls.SUPPORTED
        elif score >= 0.40:
            return cls.PRELIMINARY
        return cls.SPECULATIVE


class StrengthCategory(str, Enum):
    HIGH = "high"        # >= 0.75
    MEDIUM = "medium"    # 0.40 - 0.74
    LOW = "low"          # < 0.40

    @classmethod
    def from_score(cls, score: float) -> StrengthCategory:
        if score >= 0.75:
            return cls.HIGH
        elif score >= 0.40:
            return cls.MEDIUM
        return cls.LOW


class RunMode(str, Enum):
    GUIDED = "guided"
    EXPLORATION = "exploration"
    AUTO = "auto"


def _uid() -> str:
    return uuid.uuid4().hex[:12]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class Result:
    """An established result from a domain of science/mathematics."""

    name: str
    authors: str
    year: int
    domain_id: str
    epistemic_status: str  # EpistemicStatus value
    structural_conclusion: str
    source_citation: str = ""
    id: str = field(default_factory=_uid)

    @property
    def status(self) -> EpistemicStatus:
        return EpistemicStatus(self.epistemic_status)


@dataclass
class Domain:
    """A surveyed domain of science/mathematics."""

    id: str
    name: str
    category: str
    description: str = ""
    results: list[dict] = field(default_factory=list)
    structural_conclusion: str = ""
    surveyed: bool = False
    survey_timestamp: str = ""

    def get_results(self) -> list[Result]:
        return [Result(**r) for r in self.results]


@dataclass
class SupportingResult:
    """A result that supports a convergence."""

    result_id: str
    result_name: str
    domain_id: str
    domain_name: str
    link_type: str  # "direct" or "analogical_extension"
    structural_conclusion: str = ""
    epistemic_status: str = "established_framework"


@dataclass
class EAScores:
    """Epistemic Assurance validation scores."""

    strength: float = 0.0
    independence: float = 0.0
    adversarial: float = 0.0
    reproducibility: float = 0.0
    depth_consistency: float = 1.0
    confidence: float = 0.0
    confidence_category: str = "speculative"

    def compute_confidence(self) -> float:
        self.confidence = (
            self.strength * 0.30
            + self.independence * 0.25
            + self.adversarial * 0.20
            + self.reproducibility * 0.15
            + self.depth_consistency * 0.10
        )
        self.confidence_category = ConfidenceCategory.from_score(self.confidence).value
        return self.confidence


@dataclass
class Convergence:
    """A structural convergence across domains."""

    structural_claim: str
    convergence_type: str  # ConvergenceType value
    supporting_results: list[dict] = field(default_factory=list)
    domains: list[str] = field(default_factory=list)
    domain_names: list[str] = field(default_factory=list)
    ea_scores: dict = field(default_factory=dict)
    discovered_in_run: str = ""
    discovered_at_level: int = 0
    timestamp: str = field(default_factory=_now)
    id: str = field(default_factory=_uid)

    def get_supporting(self) -> list[SupportingResult]:
        return [SupportingResult(**r) for r in self.supporting_results]

    def get_ea(self) -> EAScores:
        return EAScores(**self.ea_scores) if self.ea_scores else EAScores()

    @property
    def strength_category(self) -> StrengthCategory:
        ea = self.get_ea()
        return StrengthCategory.from_score(ea.strength)


@dataclass
class Finding:
    """A structural finding from convergence or meta-convergence."""

    structural_finding: str
    level: int
    source_convergence_ids: list[str] = field(default_factory=list)
    is_meta_convergence: bool = False
    coined_term: Optional[str] = None
    next_question: Optional[str] = None
    confidence: float = 0.0
    discovered_in_run: str = ""
    timestamp: str = field(default_factory=_now)
    id: str = field(default_factory=_uid)


@dataclass
class RunStats:
    """Statistics for a discovery run."""

    domains_surveyed: int = 0
    results_catalogued: int = 0
    combinations_explored: int = 0
    convergences_found: int = 0
    high_strength: int = 0
    medium_strength: int = 0
    analogical: int = 0
    findings_produced: int = 0
    meta_convergences: int = 0
    fixed_point_reached: bool = False
    api_calls: int = 0
    tokens_used: int = 0
    estimated_cost_usd: float = 0.0
    cycles_completed: int = 0
    termination_reason: str = ""


@dataclass
class Run:
    """A complete discovery run."""

    mode: str  # RunMode value
    input_question: Optional[str] = None
    input_domains: list[str] = field(default_factory=list)
    convergences: list[dict] = field(default_factory=list)
    findings: list[dict] = field(default_factory=list)
    stats: dict = field(default_factory=dict)
    started_at: str = field(default_factory=_now)
    completed_at: str = ""
    id: str = field(default_factory=lambda: f"run_{_uid()}")

    def get_convergences(self) -> list[Convergence]:
        return [Convergence(**c) for c in self.convergences]

    def get_findings(self) -> list[Finding]:
        return [Finding(**f) for f in self.findings]

    def get_stats(self) -> RunStats:
        return RunStats(**self.stats) if self.stats else RunStats()

    def complete(self, reason: str = "finished"):
        self.completed_at = _now()
        stats = self.get_stats()
        stats.termination_reason = reason
        self.stats = asdict(stats)

    @property
    def duration_seconds(self) -> int:
        if not self.completed_at:
            return 0
        start = datetime.fromisoformat(self.started_at)
        end = datetime.fromisoformat(self.completed_at)
        return int((end - start).total_seconds())

    @property
    def duration_human(self) -> str:
        s = self.duration_seconds
        if s < 60:
            return f"{s}s"
        elif s < 3600:
            return f"{s // 60}m {s % 60}s"
        else:
            return f"{s // 3600}h {(s % 3600) // 60}m"
