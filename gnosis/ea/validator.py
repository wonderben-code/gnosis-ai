"""EA Engine — Epistemic Assurance validation for convergences."""

from __future__ import annotations

from dataclasses import asdict

from gnosis.api.claude import ClaudeAPI
from gnosis.data.models import (
    Convergence, EAScores, EpistemicStatus, ConvergenceType,
    ConfidenceCategory, StrengthCategory,
)


INDEPENDENCE_PROMPT = """Assess the independence of these fields contributing to a convergence.

Convergence claim: {claim}

Contributing fields and results:
{results_text}

For each pair of contributing results from different fields, assess:
1. Do they share foundational mathematics?
2. Was one derived from or inspired by the other?
3. Do they address the same problem?
4. Were they developed by the same research community?

Return JSON:
{{
  "independence_score": 0.0-1.0,
  "assessment": "Brief explanation",
  "concerns": ["Any independence concerns, or empty list"]
}}

Score guide: 1.0 = completely independent (different math, different problems, different communities).
0.7 = mostly independent (some shared tools). 0.4 = partially related. 0.2 = same subfield."""


ADVERSARIAL_PROMPT = """You are an adversarial reviewer. Your job is to find counter-evidence
and weaknesses in this convergence claim.

Convergence claim: {claim}
Supporting fields: {fields}
Convergence type: {conv_type}

Supporting evidence:
{results_text}

Actively search for:
1. Established results from ANY field that contradict this claim
2. Well-known objections to this type of cross-domain comparison
3. Whether this convergence is trivial (explainable by shared mathematical tools
   rather than genuine structural agreement)
4. Whether the structural conclusions were over-interpreted to create a false match
5. Alternative explanations for the apparent convergence

Return JSON:
{{
  "counter_evidence": ["List of specific counter-evidence or objections"],
  "trivial": true/false,
  "trivial_reason": "If trivial, explain why",
  "support_ratio": 0.0-1.0,
  "assessment": "Overall adversarial assessment"
}}

support_ratio: 1.0 = no counter-evidence found, claim is robust.
0.7 = minor concerns but claim holds. 0.4 = significant concerns. 0.0 = claim is false."""


class EAValidator:
    """Epistemic Assurance — validates convergences through multiple checks."""

    def __init__(self, api: ClaudeAPI):
        self.api = api

    def validate(self, convergence: Convergence) -> EAScores:
        """Run all EA checks on a convergence. Returns scores."""

        scores = EAScores()

        # 1. Convergence strength (computed from data, no API call needed)
        scores.strength = self._compute_strength(convergence)

        # 2. Independence verification (API call)
        scores.independence = self._check_independence(convergence)

        # 3. Adversarial scan (API call)
        scores.adversarial = self._adversarial_scan(convergence)

        # 4. Reproducibility (computed from structure)
        scores.reproducibility = self._check_reproducibility(convergence)

        # 5. Depth consistency (default 1.0, checked later across findings)
        scores.depth_consistency = 1.0

        # Aggregate
        scores.compute_confidence()

        # Store scores on the convergence
        convergence.ea_scores = asdict(scores)

        return scores

    def _compute_strength(self, conv: Convergence) -> float:
        """Compute convergence strength from framework count, independence, epistemic weight."""

        supporting = conv.get_supporting()
        if not supporting:
            return 0.0

        # Framework count factor (normalized: 2 results = 0.4, 4 = 0.7, 6+ = 1.0)
        n = len(supporting)
        count_factor = min(1.0, 0.2 + (n - 1) * 0.2)

        # Epistemic weight (average status weight of supporting results)
        weights = []
        for s in supporting:
            try:
                status = EpistemicStatus(s.epistemic_status)
                weights.append(status.weight)
            except (ValueError, AttributeError):
                weights.append(0.7)  # default to established_framework weight
        epistemic_factor = sum(weights) / len(weights) if weights else 0.5

        # Convergence type weight
        try:
            type_weight = ConvergenceType(conv.convergence_type).weight
        except ValueError:
            type_weight = 0.6

        # Domain diversity (more domains = stronger)
        domain_count = len(set(conv.domains))
        diversity_factor = min(1.0, 0.3 + domain_count * 0.2)

        return min(1.0, count_factor * epistemic_factor * type_weight * diversity_factor)

    def _check_independence(self, conv: Convergence) -> float:
        """Verify independence of contributing fields via Claude."""

        supporting = conv.get_supporting()
        if len(supporting) < 2:
            return 0.0

        results_text = "\n".join(
            f"- [{s.domain_name}] {s.result_name}: {s.structural_conclusion}"
            for s in supporting
        )

        prompt = INDEPENDENCE_PROMPT.format(
            claim=conv.structural_claim,
            results_text=results_text,
        )

        try:
            data = self.api.query_json(prompt, max_tokens=2048)
            return float(data.get("independence_score", 0.5))
        except Exception:
            return 0.5  # default on failure

    def _adversarial_scan(self, conv: Convergence) -> float:
        """Adversarial scan for counter-evidence."""

        supporting = conv.get_supporting()
        results_text = "\n".join(
            f"- [{s.domain_name}] {s.result_name}: {s.structural_conclusion}"
            for s in supporting
        )
        fields = ", ".join(conv.domain_names) if conv.domain_names else ", ".join(conv.domains)

        prompt = ADVERSARIAL_PROMPT.format(
            claim=conv.structural_claim,
            fields=fields,
            conv_type=conv.convergence_type,
            results_text=results_text,
        )

        try:
            # Use deep model for adversarial — needs strongest critical reasoning
            data = self.api.query_deep_json(prompt, max_tokens=2048)
            score = float(data.get("support_ratio", 0.5))
            # Penalize if flagged as trivial
            if data.get("trivial", False):
                score *= 0.3
            return score
        except Exception:
            return 0.5  # default on failure

    def _check_reproducibility(self, conv: Convergence) -> float:
        """Estimate reproducibility from structural properties.

        Full reproducibility testing (re-running with different subsets) is expensive.
        For v1, we use structural proxies:
        - More supporting results = more robust
        - Results from more domains = more robust
        - Formal convergence more robust than analogy
        """
        supporting = conv.get_supporting()
        n_results = len(supporting)
        n_domains = len(set(s.domain_id for s in supporting))

        # More results = more robust (diminishing returns)
        result_factor = min(1.0, 0.3 + n_results * 0.15)

        # More domains = more robust
        domain_factor = min(1.0, 0.2 + n_domains * 0.25)

        # Direct links more robust than analogical
        direct_ratio = sum(1 for s in supporting if s.link_type == "direct") / max(1, n_results)
        link_factor = 0.5 + direct_ratio * 0.5

        return result_factor * domain_factor * link_factor
