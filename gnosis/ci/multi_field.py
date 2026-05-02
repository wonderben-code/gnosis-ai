"""Multi-Field Detector — finds convergences across 3+ fields simultaneously.

This is fundamentally different from pairwise detection. Instead of asking
"do these two fields share structure?", we ask "is there a structural pattern
that ALL of these fields instantiate — one that only becomes visible when
you look at all of them together?"

Two-stage approach:
1. Extract structural essence of each field (3-5 core principles)
2. Present all essences simultaneously for N-way pattern detection
"""

from __future__ import annotations

from gnosis.api.claude import ClaudeAPI
from gnosis.data.models import Convergence, Domain


SYSTEM_PROMPT = """You are a component of Gnosis AI, an autonomous knowledge discovery system.
Your role is the Multi-Field Convergence Detector: you identify structural patterns that
emerge ONLY when examining multiple independent fields simultaneously.

These are NOT pairwise convergences. Pairwise convergences have already been found.
You are looking for N-way patterns — structural regularities that all fields share,
and that are only visible when you see them all together.

You must be:
- CONSERVATIVE: Multi-field convergences are rarer and more significant than pairwise
- PRECISE: The pattern must genuinely require all fields to be visible
- HONEST: If the fields don't share a genuine multi-field pattern, say so
- INDEPENDENCE-AWARE: The pattern should not be trivially derivable from known pairwise connections"""


STRUCTURAL_ESSENCE_PROMPT = """Given the following survey of {field_name} ({category}), extract its 3-5 core structural principles.

These should be the deepest structural features of this field — the patterns that define
how objects in this field behave and relate to each other. Focus on STRUCTURE, not content.

Survey results:
{results_text}

Field-level structural conclusion: {structural_conclusion}

Return JSON:
{{
  "structural_essence": [
    {{
      "principle": "One-sentence structural principle",
      "supporting_results": ["result_name_1", "result_name_2"],
      "abstraction_level": "mathematical" or "structural" or "phenomenological"
    }}
  ]
}}"""


MULTI_FIELD_DETECT_PROMPT = """You are examining {n} fields from different domains of science and mathematics simultaneously.

Your task is NOT to find pairwise convergences between pairs of fields — those have already been found.
Your task is to find MULTI-FIELD CONVERGENCES: structural patterns that ALL {n} fields share
simultaneously, patterns that only become visible when you look at all of them together.

## Fields and their structural essences:

{essences_text}

---

Consider: Is there a structural pattern that ALL {n} of these fields instantiate?
Not just "A and B share X" — that's pairwise. We need "A, B, C, and D ALL share X,
and X only becomes visible when you see all of them together."

Be CONSERVATIVE. Multi-field convergences are rarer and more significant than pairwise.
If the fields don't share a genuine multi-field pattern, say so.

Return JSON:
{{
  "multi_field_convergences": [
    {{
      "structural_claim": "The multi-field convergence — what ALL fields share",
      "fields_involved": ["field_id_1", "field_id_2", ...],
      "per_field_manifestation": {{
        "field_id_1": "How this pattern manifests in this field",
        "field_id_2": "How this pattern manifests in this field"
      }},
      "why_multi_field": "Why this pattern is only visible when examining all fields together, not reducible to pairwise convergences",
      "convergence_type": "formal" or "structural_analogy",
      "mathematical_structures": ["Relevant mathematical frameworks"],
      "proposed_equivalence": "The kind of formal relationship: isomorphism, functor, structural_analogy, etc.",
      "formalisability_hint": "high" or "medium" or "low" or "requires_new_mathematics",
      "reasoning": "Explanation of why this is genuine"
    }}
  ],
  "no_convergence_reason": "If none found, explain why"
}}"""


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


class MultiFieldDetector:
    """Detects convergences across 3+ fields simultaneously."""

    def __init__(self, api: ClaudeAPI):
        self.api = api
        self._essence_cache: dict[str, list[dict]] = {}

    def extract_essence(self, domain: Domain) -> list[dict]:
        """Extract structural essence from a surveyed domain.

        Results are cached — one essence per domain, reusable across groups.
        """
        if domain.id in self._essence_cache:
            return self._essence_cache[domain.id]

        prompt = STRUCTURAL_ESSENCE_PROMPT.format(
            field_name=domain.name,
            category=domain.category,
            results_text=_format_results(domain),
            structural_conclusion=domain.structural_conclusion,
        )

        data = self.api.query_json(prompt, system=SYSTEM_PROMPT, max_tokens=2048)
        essence = data.get("structural_essence", [])
        self._essence_cache[domain.id] = essence
        return essence

    def detect(self, domains: list[Domain]) -> tuple[list[Convergence], str]:
        """Detect multi-field convergences across 3+ domains.

        Returns (convergences, no_convergence_reason).
        """
        if len(domains) < 3:
            raise ValueError("Multi-field detection requires 3+ domains")

        # Stage 1: Extract structural essence for each domain
        essences = {}
        for domain in domains:
            essences[domain.id] = self.extract_essence(domain)

        # Stage 2: Build multi-field detection prompt
        essences_text = ""
        for domain in domains:
            essences_text += f"### {domain.name} ({domain.category})\n"
            essences_text += "Core structural principles:\n"
            for e in essences[domain.id]:
                level = e.get("abstraction_level", "structural")
                essences_text += f"- [{level}] {e.get('principle', '?')}\n"
            essences_text += "\n"

        prompt = MULTI_FIELD_DETECT_PROMPT.format(
            n=len(domains),
            essences_text=essences_text,
        )

        # Use deep model for multi-field — needs strongest reasoning
        data = self.api.query_deep_json(prompt, system=SYSTEM_PROMPT, max_tokens=4096)

        field_ids = [d.id for d in domains]
        field_names = [d.name for d in domains]
        source_cats = sorted(set(d.category for d in domains))

        convergences = []
        for c in data.get("multi_field_convergences", []):
            # Build supporting results from per-field manifestations
            supporting = []
            per_field = c.get("per_field_manifestation", {})
            for domain in domains:
                if domain.id in per_field:
                    supporting.append({
                        "result_id": "",
                        "result_name": f"{domain.name} manifestation",
                        "domain_id": domain.id,
                        "domain_name": domain.name,
                        "link_type": "direct",
                        "structural_conclusion": per_field[domain.id],
                    })

            conv = Convergence(
                structural_claim=c["structural_claim"],
                convergence_type=c.get("convergence_type", "structural_analogy"),
                supporting_results=supporting,
                domains=c.get("fields_involved", field_ids),
                domain_names=field_names,
                comparison_type="multi_field",
                mathematical_structures=c.get("mathematical_structures", []),
                proposed_equivalence=c.get("proposed_equivalence", ""),
                formalisability_hint=c.get("formalisability_hint", ""),
                source_categories=source_cats,
            )
            convergences.append(conv)

        no_reason = data.get("no_convergence_reason", "")
        return convergences, no_reason
