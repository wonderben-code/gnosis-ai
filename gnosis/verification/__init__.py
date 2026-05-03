"""Gnosis v3 — External Knowledge Verification + Quality Assurance.

Verifies every surveyed result against 5 independent academic databases.
Checks convergence quality via formal criteria and counterexample testing.
Zero reliance on Claude for verification verdicts — purely external data.
"""

from gnosis.verification.verifier import KnowledgeVerifier, VerificationResult, SourceResult
from gnosis.verification.convergence_quality import ConvergenceQualityChecker
