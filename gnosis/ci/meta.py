"""Meta-Convergence Engine — finds higher-order patterns across convergences."""

from __future__ import annotations

from gnosis.api.claude import ClaudeAPI
from gnosis.data.models import Convergence, Finding

SYSTEM_PROMPT = """You are a component of Gnosis AI, an autonomous knowledge discovery system.
Your role is the Meta-Convergence Engine: you find higher-order structural patterns across
convergences that were discovered independently.

Meta-convergence is the core of Convergent Descent: when convergences from different field
pairs themselves share structural patterns, those patterns represent deeper truths that
emerge only from cross-domain analysis.

You must be:
- STRUCTURAL: Look for genuine structural patterns, not shared vocabulary
- REDUCTIVE: Try to reduce multiple convergences to fewer, deeper findings
- HONEST: If convergences don't share patterns, say so — don't force it
- AWARE of fixed points: If reduction produces the same output as input, stop"""


META_PROMPT = """These {n} convergences were discovered independently across different field combinations.
Each represents a structural pattern found by comparing results from independent domains.

{convergences_text}

TASK: Do these convergences themselves share structural patterns? Can they be reduced
to fewer, deeper structural findings?

Consider:
1. Do multiple convergences describe aspects of the same deeper structure?
2. Are there pairwise links between convergences that suggest a shared underlying principle?
3. Can the full set be reduced to 1-3 fundamental structural features?
4. If reduced to features: do those features themselves collapse further?

Return JSON:
{{
  "meta_convergences": [
    {{
      "structural_finding": "The meta-convergence finding — what the convergences collectively point to",
      "source_convergence_ids": ["id1", "id2", ...],
      "coined_term": "A name for this finding if it warrants one, or null",
      "reasoning": "Why these convergences point to this deeper structure"
    }}
  ],
  "reduction_possible": true/false,
  "fixed_point_reached": true/false,
  "fixed_point_statement": "If fixed point reached: the irreducible structural finding, or null"
}}

If the convergences don't share meaningful higher-order patterns, return:
{{"meta_convergences": [], "reduction_possible": false, "fixed_point_reached": false, "fixed_point_statement": null}}"""


def _format_convergences(convergences: list[Convergence]) -> str:
    lines = []
    for i, c in enumerate(convergences, 1):
        domains = ", ".join(c.domain_names) if c.domain_names else ", ".join(c.domains)
        lines.append(f"### Convergence {i} (ID: {c.id})")
        lines.append(f"**Fields:** {domains}")
        lines.append(f"**Type:** {c.convergence_type}")
        lines.append(f"**Structural claim:** {c.structural_claim}")
        lines.append("")
    return "\n".join(lines)


class MetaConvergenceEngine:
    """Finds higher-order patterns across convergences — the core of Convergent Descent."""

    def __init__(self, api: ClaudeAPI):
        self.api = api

    def meta_converge(
        self,
        convergences: list[Convergence],
        max_iterations: int = 5,
    ) -> list[Finding]:
        """Run iterative meta-convergence until fixed point or exhaustion.

        Returns all findings produced across iterations.
        """
        if len(convergences) < 2:
            return []

        all_findings = []
        current_convergences = convergences
        level = 1

        for iteration in range(max_iterations):
            findings = self._one_round(current_convergences, level)

            if not findings:
                # No further meta-convergence possible
                break

            all_findings.extend(findings)

            # Check for fixed point
            if any(f.coined_term and "fixed_point" in (f.coined_term or "").lower()
                   for f in findings):
                break

            # If we reduced to 1 finding, check if it's irreducible
            if len(findings) == 1:
                break

            # Convert findings back to convergences for next iteration
            current_convergences = [
                Convergence(
                    structural_claim=f.structural_finding,
                    convergence_type="formal",
                    domains=[],
                    domain_names=["meta-convergence"],
                    id=f.id,
                )
                for f in findings
            ]
            level += 1

        return all_findings

    def _one_round(
        self,
        convergences: list[Convergence],
        level: int,
    ) -> list[Finding]:
        """Run one round of meta-convergence."""

        prompt = META_PROMPT.format(
            n=len(convergences),
            convergences_text=_format_convergences(convergences),
        )

        # Use deep model for meta-convergence — needs strongest reasoning
        data = self.api.query_deep_json(prompt, system=SYSTEM_PROMPT)

        findings = []
        for mc in data.get("meta_convergences", []):
            finding = Finding(
                structural_finding=mc["structural_finding"],
                level=level,
                source_convergence_ids=mc.get("source_convergence_ids", []),
                is_meta_convergence=True,
                coined_term=mc.get("coined_term"),
            )
            findings.append(finding)

        # If a fixed point was reached, add it as a finding
        if data.get("fixed_point_reached") and data.get("fixed_point_statement"):
            fp = Finding(
                structural_finding=data["fixed_point_statement"],
                level=level,
                source_convergence_ids=[c.id for c in convergences],
                is_meta_convergence=True,
                coined_term="Fixed Point",
            )
            findings.append(fp)

        return findings
