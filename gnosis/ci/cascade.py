"""Recursive Cascade Engine — multi-level meta-convergence with multiple grouping strategies.

The v1 MetaConvergenceEngine takes ALL convergences and reduces them in one pass.
The CascadeEngine applies MULTIPLE grouping strategies at each level, producing
potentially different meta-convergences from different perspectives on the same data.

Grouping strategies:
- BY_DOMAIN: group by shared field (all convergences involving field X)
- BY_CATEGORY: group by category pair (all Physics×Biology convergences)
- BY_PATTERN: Claude-assisted clustering by structural similarity
- BY_CONFIDENCE: group by confidence tier
- PAIRWISE: compare convergences pairwise
- HOLISTIC: all together (v1 behaviour)
- CROSS_LEVEL: compare findings across levels
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from gnosis.api.claude import ClaudeAPI
from gnosis.ci.meta import MetaConvergenceEngine
from gnosis.data.models import Convergence, Finding, ConfidenceCategory


class GroupingStrategy(str, Enum):
    BY_DOMAIN = "by_domain"
    BY_CATEGORY = "by_category"
    BY_PATTERN = "by_pattern"
    BY_CONFIDENCE = "by_confidence"
    PAIRWISE = "pairwise"
    HOLISTIC = "holistic"
    CROSS_LEVEL = "cross_level"


@dataclass
class CascadeResult:
    """Result of a full cascade run."""
    findings: list[Finding] = field(default_factory=list)
    levels_reached: int = 0
    fixed_point_reached: bool = False
    strategy_counts: dict[str, int] = field(default_factory=dict)


CROSS_LEVEL_PROMPT = """You are comparing findings from different levels of analysis.

## Level {lower_level} findings (more specific):
{findings_text_lower}

## Level {upper_level} findings (more abstract):
{findings_text_higher}

Do any lower-level findings share structural features with higher-level patterns?
A lower-level finding might be a SPECIFIC INSTANCE of a higher-level pattern.
Or a higher-level pattern might EXPLAIN why a lower-level finding exists.

Return JSON:
{{
  "cross_level_convergences": [
    {{
      "structural_claim": "The cross-level relationship",
      "lower_finding_ids": ["id1"],
      "higher_finding_ids": ["id2"],
      "relationship_type": "instance_of" or "explained_by" or "structural_parallel",
      "reasoning": "Why this cross-level relationship is genuine"
    }}
  ]
}}

If no genuine cross-level relationships exist, return {{"cross_level_convergences": []}}."""


PATTERN_CLUSTERING_PROMPT = """Group these {n} convergences by structural similarity. Convergences that describe
aspects of the same underlying pattern should be in the same cluster.

{convergences_text}

Return JSON:
{{
  "clusters": [
    {{
      "cluster_name": "Descriptive name for this structural pattern",
      "convergence_ids": ["id1", "id2"],
      "shared_pattern": "What these convergences have in common structurally"
    }}
  ]
}}"""


class CascadeEngine:
    """Multi-level recursive cascade with multiple grouping strategies."""

    def __init__(self, api: ClaudeAPI, field_category_fn=None):
        """
        Args:
            api: Claude API instance
            field_category_fn: callable(field_id) -> category_name
        """
        self.api = api
        self.meta_engine = MetaConvergenceEngine(api)
        self._field_category = field_category_fn or (lambda x: "unknown")

    def run_cascade(
        self,
        convergences: list[Convergence],
        strategies: list[GroupingStrategy] | None = None,
        max_levels: int = 5,
        cross_level: bool = True,
    ) -> CascadeResult:
        """Run the full multi-level cascade.

        At each level:
        1. Apply each grouping strategy to create groups of convergences
        2. Run meta-convergence on each group
        3. Deduplicate findings across strategies
        4. Optionally compare across levels
        5. Convert findings to convergence-like objects for next level
        """
        if strategies is None:
            strategies = [
                GroupingStrategy.BY_DOMAIN,
                GroupingStrategy.BY_CATEGORY,
                GroupingStrategy.BY_PATTERN,
                GroupingStrategy.HOLISTIC,
            ]

        all_findings: list[Finding] = []
        current_level_objects = convergences
        level = 1
        strategy_counts: dict[str, int] = {}
        fp_reached = False

        while level <= max_levels:
            level_findings: list[Finding] = []

            for strategy in strategies:
                groups = self._group(current_level_objects, strategy)
                for group_name, group_items in groups.items():
                    if len(group_items) < 2:
                        continue

                    findings = self.meta_engine._one_round(group_items, level)
                    for f in findings:
                        f.grouping_strategy = strategy.value
                        f.group_name = group_name

                    level_findings.extend(findings)
                    strategy_counts[strategy.value] = (
                        strategy_counts.get(strategy.value, 0) + len(findings)
                    )

            if not level_findings:
                break

            # Deduplicate across strategies
            level_findings = self._deduplicate(level_findings)
            all_findings.extend(level_findings)

            # Check for fixed points
            if any(
                f.coined_term and "fixed_point" in (f.coined_term or "").lower()
                for f in level_findings
            ):
                fp_reached = True
                break

            # Cross-level comparison
            if cross_level and level > 1:
                prev_level_findings = [
                    f for f in all_findings if f.level == level - 1
                ]
                cross_findings = self._cross_level_compare(
                    prev_level_findings, level_findings, level
                )
                for cf in cross_findings:
                    cf.grouping_strategy = GroupingStrategy.CROSS_LEVEL.value
                all_findings.extend(cross_findings)

            # If only 1 finding, it's irreducible
            if len(level_findings) == 1:
                break

            # Convert findings to convergence-like objects for next level
            current_level_objects = self._findings_to_convergences(level_findings)
            level += 1

        return CascadeResult(
            findings=all_findings,
            levels_reached=level,
            fixed_point_reached=fp_reached,
            strategy_counts=strategy_counts,
        )

    def _group(
        self,
        items: list[Convergence],
        strategy: GroupingStrategy,
    ) -> dict[str, list[Convergence]]:
        """Group convergences by the specified strategy."""

        if strategy == GroupingStrategy.BY_DOMAIN:
            groups: dict[str, list[Convergence]] = {}
            for c in items:
                for d in c.domains:
                    groups.setdefault(f"domain:{d}", []).append(c)
            return groups

        elif strategy == GroupingStrategy.BY_CATEGORY:
            groups = {}
            for c in items:
                cats = sorted(set(
                    self._field_category(d) for d in c.domains
                ))
                key = "×".join(cats) if len(cats) > 1 else cats[0] if cats else "unknown"
                groups.setdefault(f"category:{key}", []).append(c)
            return groups

        elif strategy == GroupingStrategy.BY_PATTERN:
            return self._cluster_by_pattern(items)

        elif strategy == GroupingStrategy.BY_CONFIDENCE:
            groups = {}
            for c in items:
                ea = c.get_ea()
                if ea.confidence > 0:
                    tier = ConfidenceCategory.from_score(ea.confidence).value
                else:
                    tier = "unscored"
                groups.setdefault(f"confidence:{tier}", []).append(c)
            return groups

        elif strategy == GroupingStrategy.HOLISTIC:
            return {"all": list(items)}

        elif strategy == GroupingStrategy.CROSS_LEVEL:
            # Handled separately in run_cascade
            return {}

        return {"all": list(items)}

    def _cluster_by_pattern(
        self, items: list[Convergence]
    ) -> dict[str, list[Convergence]]:
        """Use Claude to cluster convergences by structural similarity."""
        if len(items) < 3:
            return {"all": list(items)}

        # Format convergences for clustering
        lines = []
        for c in items:
            domains = ", ".join(c.domain_names) if c.domain_names else ", ".join(c.domains)
            lines.append(f"- ID: {c.id} | Fields: {domains} | Claim: {c.structural_claim}")
        convergences_text = "\n".join(lines)

        prompt = PATTERN_CLUSTERING_PROMPT.format(
            n=len(items),
            convergences_text=convergences_text,
        )

        try:
            data = self.api.query_json(prompt, max_tokens=4096)
            id_to_conv = {c.id: c for c in items}
            groups: dict[str, list[Convergence]] = {}

            for cluster in data.get("clusters", []):
                name = cluster.get("cluster_name", "unnamed")
                conv_ids = cluster.get("convergence_ids", [])
                group_convs = [id_to_conv[cid] for cid in conv_ids if cid in id_to_conv]
                if len(group_convs) >= 2:
                    groups[f"pattern:{name}"] = group_convs

            return groups if groups else {"all": list(items)}
        except Exception:
            return {"all": list(items)}

    def _cross_level_compare(
        self,
        prev_level: list[Finding],
        curr_level: list[Finding],
        level: int,
    ) -> list[Finding]:
        """Compare findings across levels."""
        if not prev_level or not curr_level:
            return []

        lower_text = "\n".join(
            f"- ID: {f.id} | Level {f.level}: {f.structural_finding}"
            + (f" ({f.coined_term})" if f.coined_term else "")
            for f in prev_level
        )
        upper_text = "\n".join(
            f"- ID: {f.id} | Level {f.level}: {f.structural_finding}"
            + (f" ({f.coined_term})" if f.coined_term else "")
            for f in curr_level
        )

        prompt = CROSS_LEVEL_PROMPT.format(
            lower_level=level - 1,
            upper_level=level,
            findings_text_lower=lower_text,
            findings_text_higher=upper_text,
        )

        try:
            data = self.api.query_json(prompt, max_tokens=4096)
            findings = []
            for cl in data.get("cross_level_convergences", []):
                f = Finding(
                    structural_finding=cl["structural_claim"],
                    level=level,
                    source_convergence_ids=(
                        cl.get("lower_finding_ids", []) +
                        cl.get("higher_finding_ids", [])
                    ),
                    is_meta_convergence=True,
                    coined_term=None,
                )
                findings.append(f)
            return findings
        except Exception:
            return []

    def _deduplicate(self, findings: list[Finding]) -> list[Finding]:
        """Remove findings that are structurally similar (from different strategies).

        Uses simple text similarity — if two findings share >70% of their words,
        keep the one with more source convergence IDs.
        """
        if len(findings) <= 1:
            return findings

        def _words(text: str) -> set[str]:
            return set(text.lower().split())

        keep: list[Finding] = []
        for f in findings:
            is_dup = False
            f_words = _words(f.structural_finding)
            for existing in keep:
                e_words = _words(existing.structural_finding)
                if not f_words or not e_words:
                    continue
                overlap = len(f_words & e_words) / max(len(f_words | e_words), 1)
                if overlap > 0.7:
                    # Keep the one with more sources
                    if len(f.source_convergence_ids) > len(existing.source_convergence_ids):
                        keep.remove(existing)
                        keep.append(f)
                    is_dup = True
                    break
            if not is_dup:
                keep.append(f)

        return keep

    def _findings_to_convergences(self, findings: list[Finding]) -> list[Convergence]:
        """Convert findings to convergence-like objects for the next cascade level."""
        return [
            Convergence(
                structural_claim=f.structural_finding,
                convergence_type="formal",
                domains=[],
                domain_names=["meta-convergence"],
                id=f.id,
                comparison_type="cross_level",
                parent_convergence_ids=f.source_convergence_ids,
            )
            for f in findings
        ]
