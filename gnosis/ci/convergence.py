"""Convergence Detector — finds structural convergences across domains."""

from __future__ import annotations

from dataclasses import asdict

from gnosis.api.claude import ClaudeAPI
from gnosis.data.models import Convergence, Domain

SYSTEM_PROMPT = """You are a component of Gnosis AI, an autonomous knowledge discovery system.
Your role is the Convergence Detector: you identify genuine structural convergences across
independent fields of science and mathematics.

A CONVERGENCE is when independently developed results from different fields arrive at the
same structural conclusion — not through shared assumptions, but through independent reasoning
from different foundations.

You must be:
- CONSERVATIVE: Only flag genuine structural agreements, not surface similarities
- PRECISE about type: "formal" = same mathematical structure appears independently;
  "structural_analogy" = parallel structure but not formally identical
- HONEST: If the connection is weak or speculative, say so — or don't include it
- INDEPENDENCE-AWARE: Results that share foundational mathematics or derive from each
  other do NOT constitute a convergence"""


DETECT_PROMPT = """Examine the structural conclusions from these two independent fields and
identify genuine convergences.

## Field A: {domain_a_name} ({domain_a_category})
Field-level structural conclusion: {domain_a_conclusion}

Results:
{domain_a_results}

## Field B: {domain_b_name} ({domain_b_category})
Field-level structural conclusion: {domain_b_conclusion}

Results:
{domain_b_results}

These fields use different foundational mathematics and address different problems.
Are there genuine structural convergences — cases where independently developed results
arrive at the same structural conclusion?

For each convergence found, classify it as:
- "formal": The same mathematical structure appears independently in both fields
- "structural_analogy": Parallel structure but not formally identical

Be conservative. Shared vocabulary is not convergence. Surface-level similarities are
not convergence. Only flag cases where the structural conclusions genuinely agree on
something about the nature of the domain.

Return JSON:
{{
  "convergences": [
    {{
      "structural_claim": "The convergence finding — one clear sentence stating what both fields agree on",
      "convergence_type": "formal" or "structural_analogy",
      "supporting_results": [
        {{
          "result_name": "Name of result",
          "domain_id": "field_id",
          "domain_name": "Field Name",
          "link_type": "direct" or "analogical_extension",
          "structural_conclusion": "What this result contributes to the convergence"
        }}
      ],
      "mathematical_structures": ["Mathematical frameworks relevant to this convergence, e.g. category theory, measure theory, group theory"],
      "proposed_equivalence": "The kind of formal relationship claimed: isomorphism, adjunction, functor, structural_analogy, homomorphism, or other",
      "formalisability_hint": "How feasible is formal proof? high = standard maths, medium = requires work, low = mostly analogical, requires_new_mathematics = beyond current formalism",
      "reasoning": "Brief explanation of why this is a genuine convergence, not a superficial similarity"
    }}
  ],
  "no_convergence_reason": "If no convergences found, explain why"
}}

If no genuine convergences exist between these fields, return {{"convergences": [], "no_convergence_reason": "Explanation"}}."""


def _format_results(domain: Domain) -> str:
    """Format a domain's results for the prompt."""
    lines = []
    for r_dict in domain.results:
        status = r_dict.get("epistemic_status", "?")
        name = r_dict.get("name", "?")
        authors = r_dict.get("authors", "?")
        conclusion = r_dict.get("structural_conclusion", "")
        lines.append(f"- **{name}** ({authors}) [{status}]: {conclusion}")
    return "\n".join(lines)


class ConvergenceDetector:
    """Detects structural convergences between pairs of surveyed domains."""

    def __init__(self, api: ClaudeAPI):
        self.api = api

    def detect(self, domain_a: Domain, domain_b: Domain) -> tuple[list[Convergence], str]:
        """Detect convergences between two surveyed domains.

        Returns (convergences, no_convergence_reason).
        """

        prompt = DETECT_PROMPT.format(
            domain_a_name=domain_a.name,
            domain_a_category=domain_a.category,
            domain_a_conclusion=domain_a.structural_conclusion,
            domain_a_results=_format_results(domain_a),
            domain_b_name=domain_b.name,
            domain_b_category=domain_b.category,
            domain_b_results=_format_results(domain_b),
            domain_b_conclusion=domain_b.structural_conclusion,
        )

        data = self.api.query_json(prompt, system=SYSTEM_PROMPT, max_tokens=4096)

        # Determine comparison type from categories
        is_cross = domain_a.category != domain_b.category
        comp_type = "cross_category" if is_cross else "within_category"
        source_cats = sorted(set([domain_a.category, domain_b.category]))

        convergences = []
        for c in data.get("convergences", []):
            supporting = []
            for s in c.get("supporting_results", []):
                supporting.append({
                    "result_id": "",
                    "result_name": s.get("result_name", ""),
                    "domain_id": s.get("domain_id", ""),
                    "domain_name": s.get("domain_name", ""),
                    "link_type": s.get("link_type", "direct"),
                    "structural_conclusion": s.get("structural_conclusion", ""),
                })

            conv = Convergence(
                structural_claim=c["structural_claim"],
                convergence_type=c.get("convergence_type", "structural_analogy"),
                supporting_results=supporting,
                domains=[domain_a.id, domain_b.id],
                domain_names=[domain_a.name, domain_b.name],
                comparison_type=comp_type,
                mathematical_structures=c.get("mathematical_structures", []),
                proposed_equivalence=c.get("proposed_equivalence", ""),
                formalisability_hint=c.get("formalisability_hint", ""),
                source_categories=source_cats,
            )
            convergences.append(conv)

        no_reason = data.get("no_convergence_reason", "")
        return convergences, no_reason

    def detect_multi(self, domains: list[Domain]) -> list[Convergence]:
        """Detect convergences across all pairs of domains."""
        all_convergences = []
        seen_pairs = set()

        for i, da in enumerate(domains):
            for j, db in enumerate(domains):
                if i >= j:
                    continue
                pair_key = tuple(sorted([da.id, db.id]))
                if pair_key in seen_pairs:
                    continue
                seen_pairs.add(pair_key)

                convs, _ = self.detect(da, db)
                all_convergences.extend(convs)

        return all_convergences
