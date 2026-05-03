"""Convergence Quality Checker — formal criteria and counterexample testing.

Ensures convergences meet rigorous structural criteria. Does NOT filter —
assigns quality scores and flags that travel with the convergence.
Novel discoveries are the whole point; quality scoring ensures transparency,
not gatekeeping.

Two checks:
  1. Formal Convergence Criteria — does this meet the definition of a
     structural correspondence? (checkable properties)
  2. Computational Counterexample Testing — try to break the convergence
     with concrete numerical instances. Surviving tests raises confidence.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ConvergenceCriteria:
    """Formal criteria assessment for a convergence."""

    # Each criterion: True/False/None (None = not assessable)
    has_formal_definitions: bool | None = None
    has_concrete_mapping: bool | None = None
    mapping_preserves_structure: bool | None = None
    is_nontrivial: bool | None = None
    generates_predictions: bool | None = None

    # Scores
    criteria_met: int = 0
    criteria_total: int = 5
    quality_score: float = 0.0  # 0.0-1.0

    # Detail
    assessment_notes: str = ""
    predictions: list[str] = field(default_factory=list)

    def compute_score(self) -> float:
        """Compute quality score from criteria."""
        assessed = []
        for val in [
            self.has_formal_definitions,
            self.has_concrete_mapping,
            self.mapping_preserves_structure,
            self.is_nontrivial,
            self.generates_predictions,
        ]:
            if val is not None:
                assessed.append(val)

        if not assessed:
            self.quality_score = 0.5  # Can't assess
            return 0.5

        self.criteria_met = sum(1 for v in assessed if v)
        self.criteria_total = len(assessed)
        self.quality_score = round(self.criteria_met / self.criteria_total, 3)
        return self.quality_score

    def to_dict(self) -> dict:
        return {
            "has_formal_definitions": self.has_formal_definitions,
            "has_concrete_mapping": self.has_concrete_mapping,
            "mapping_preserves_structure": self.mapping_preserves_structure,
            "is_nontrivial": self.is_nontrivial,
            "generates_predictions": self.generates_predictions,
            "criteria_met": self.criteria_met,
            "criteria_total": self.criteria_total,
            "quality_score": self.quality_score,
            "predictions": self.predictions,
            "assessment_notes": self.assessment_notes,
        }


@dataclass
class CounterexampleResult:
    """Result of computational counterexample testing."""

    tests_run: int = 0
    tests_passed: int = 0
    tests_failed: int = 0
    applicable: bool = True  # False for purely abstract convergences
    resistance_score: float = 0.0  # 0.0-1.0 (1.0 = survived all tests)
    details: str = ""

    def compute_score(self) -> float:
        if not self.applicable or self.tests_run == 0:
            self.resistance_score = 0.5  # Neutral — can't test
            return 0.5
        self.resistance_score = round(self.tests_passed / self.tests_run, 3)
        return self.resistance_score

    def to_dict(self) -> dict:
        return {
            "tests_run": self.tests_run,
            "tests_passed": self.tests_passed,
            "tests_failed": self.tests_failed,
            "applicable": self.applicable,
            "resistance_score": self.resistance_score,
            "details": self.details,
        }


class ConvergenceQualityChecker:
    """Checks convergence quality via formal criteria and counterexample testing.

    Uses Claude (via API) for criteria assessment and test generation.
    Uses NumPy/SymPy (external) for actual counterexample computation.

    Usage:
        checker = ConvergenceQualityChecker(api)
        criteria = checker.check_criteria(convergence)
        counter = checker.test_counterexamples(convergence)
    """

    def __init__(self, api):
        """Args: api — ClaudeAPI or MaxPlanAPI instance."""
        self.api = api

    def check_criteria(self, convergence: dict) -> ConvergenceCriteria:
        """Assess formal convergence criteria.

        Checks whether the convergence meets the mathematical definition
        of a structural correspondence. Does NOT filter — scores.
        """
        claim = convergence.get("structural_claim", "")
        domains = ", ".join(
            convergence.get("domain_names", convergence.get("domains", []))
        )
        conv_type = convergence.get("convergence_type", "")
        math_structs = convergence.get("mathematical_structures", [])
        supporting = convergence.get("supporting_results", [])

        supporting_text = "\n".join(
            f"- [{r.get('domain_name', '')}] {r.get('result_name', '')}: "
            f"{r.get('structural_conclusion', '')}"
            for r in supporting[:10]
        )

        prompt = f"""Assess this convergence against formal structural criteria.

CLAIM: {claim}
DOMAINS: {domains}
TYPE: {conv_type}
MATHEMATICAL STRUCTURES: {', '.join(math_structs) if math_structs else 'not specified'}

SUPPORTING RESULTS:
{supporting_text}

For each criterion, answer true, false, or null (if not assessable):

1. has_formal_definitions: Do BOTH sides of this convergence have clearly specifiable
   formal mathematical definitions? (Not vague concepts — actual mathematical objects
   with axioms/properties that can be written down.)

2. has_concrete_mapping: Can a concrete mapping between the two structures be specified?
   (Not just "they're similar" — an actual function, functor, or correspondence that
   takes elements of one structure to elements of the other.)

3. mapping_preserves_structure: Does the claimed mapping preserve key operations,
   relations, or properties? (If A has operation *, does the mapping take a*b to
   f(a)*f(b) in the appropriate sense?)

4. is_nontrivial: Is this correspondence non-trivial? (Not just "both use real numbers"
   or "both involve exponentials." The correspondence should reveal something that
   isn't obvious from the definitions alone.)

5. generates_predictions: Does this convergence generate at least one falsifiable
   prediction? (Something that could be checked experimentally, computationally,
   or by future mathematical work, and that could turn out to be wrong.)

Also generate 1-3 specific predictions if criterion 5 is true.

Return JSON:
{{
    "has_formal_definitions": true/false/null,
    "has_concrete_mapping": true/false/null,
    "mapping_preserves_structure": true/false/null,
    "is_nontrivial": true/false/null,
    "generates_predictions": true/false/null,
    "predictions": ["prediction 1", "prediction 2"],
    "assessment_notes": "brief explanation of assessment"
}}"""

        try:
            data = self.api.query_json(
                prompt,
                system=(
                    "You are a mathematical structure analyst. Be rigorous and honest. "
                    "It is perfectly fine if criteria are not met — the goal is accurate "
                    "assessment, not approval. Novel claims that don't yet have formal "
                    "definitions should have has_formal_definitions=false, not null."
                ),
            )

            criteria = ConvergenceCriteria(
                has_formal_definitions=data.get("has_formal_definitions"),
                has_concrete_mapping=data.get("has_concrete_mapping"),
                mapping_preserves_structure=data.get("mapping_preserves_structure"),
                is_nontrivial=data.get("is_nontrivial"),
                generates_predictions=data.get("generates_predictions"),
                predictions=data.get("predictions", []),
                assessment_notes=data.get("assessment_notes", ""),
            )
            criteria.compute_score()
            return criteria

        except Exception as e:
            return ConvergenceCriteria(assessment_notes=f"Assessment failed: {e}")

    def test_counterexamples(self, convergence: dict) -> CounterexampleResult:
        """Generate and run computational counterexample tests.

        Claude generates test cases; NumPy/SymPy runs them (external).
        If the convergence survives all tests, confidence increases.
        If tests fail, confidence decreases (but the convergence is NOT filtered).
        """
        claim = convergence.get("structural_claim", "")
        domains = ", ".join(
            convergence.get("domain_names", convergence.get("domains", []))
        )

        prompt = f"""Generate a Python script that tests this convergence claim with concrete numerical examples.

CLAIM: {claim}
DOMAINS: {domains}

The script should:
1. Instantiate both structures with concrete values where possible
2. Test at least 3 cases where the claimed correspondence should hold
3. Test at least 1 boundary/edge case
4. Print "TEST N: PASSED" or "TEST N: FAILED" for each test
5. Print "TOTAL: X/Y passed" at the end
6. Use only numpy and sympy (both installed)
7. If the claim is too abstract to test numerically (e.g., purely categorical),
   print "NOT_APPLICABLE: [reason]" and exit

RULES:
- Do NOT import anything other than numpy, scipy, sympy, math, random
- Do NOT access network or filesystem
- Set numpy random seed for reproducibility: numpy.random.seed(42)
- Use numpy.testing.assert_allclose for float comparisons (rtol=1e-6)

Return JSON:
{{
    "test_script": "the complete Python script",
    "applicability": "full" | "partial" | "none",
    "tests_planned": N,
    "notes": "explanation"
}}"""

        try:
            data = self.api.query_json(
                prompt,
                system=(
                    "You are a computational mathematician. Generate rigorous test "
                    "scripts that genuinely test the claimed structural correspondence. "
                    "If the claim is too abstract to test numerically, say so honestly."
                ),
            )

            applicability = data.get("applicability", "none")
            if applicability == "none":
                return CounterexampleResult(applicable=False, details="Too abstract for numerical testing")

            script = data.get("test_script", "")
            if not script:
                return CounterexampleResult(applicable=False, details="No test script generated")

            return self._run_test_script(script)

        except Exception as e:
            return CounterexampleResult(applicable=False, details=f"Test generation failed: {e}")

    def _run_test_script(self, script: str) -> CounterexampleResult:
        """Execute a counterexample test script and parse results."""
        try:
            with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
                f.write(script)
                temp_path = f.name

            result = subprocess.run(
                [sys.executable, temp_path],
                capture_output=True, text=True, timeout=60,
            )

            Path(temp_path).unlink(missing_ok=True)
            output = result.stdout.strip()

            if "NOT_APPLICABLE" in output:
                return CounterexampleResult(applicable=False, details=output)

            passed = output.count("PASSED")
            failed = output.count("FAILED")
            total = passed + failed

            cr = CounterexampleResult(
                tests_run=total,
                tests_passed=passed,
                tests_failed=failed,
                applicable=True,
                details=output,
            )
            cr.compute_score()
            return cr

        except subprocess.TimeoutExpired:
            Path(temp_path).unlink(missing_ok=True)
            return CounterexampleResult(applicable=True, details="Script timed out")
        except Exception as e:
            return CounterexampleResult(applicable=True, details=f"Execution error: {e}")

    def full_quality_check(self, convergence: dict) -> dict:
        """Run all quality checks on a convergence. Returns combined quality data.

        Does NOT filter. Adds quality metadata for transparency.
        """
        criteria = self.check_criteria(convergence)
        counter = self.test_counterexamples(convergence)

        # Combined quality score (weighted)
        criteria_weight = 0.6
        counter_weight = 0.4
        combined = (
            criteria.quality_score * criteria_weight
            + counter.resistance_score * counter_weight
        )

        return {
            "convergence_quality_score": round(combined, 3),
            "criteria": criteria.to_dict(),
            "counterexample_testing": counter.to_dict(),
        }
