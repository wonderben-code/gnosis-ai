"""Domain Surveyor — surveys a field and extracts established results.

v3: Post-survey verification against 5 external academic databases.
Unverified results are CULLED from the pipeline.
"""

from __future__ import annotations

from gnosis.api.claude import ClaudeAPI
from gnosis.data.models import Domain, Result, _now
from gnosis.data.store import Store
from gnosis.data.taxonomy import FieldInfo
from gnosis.verification.verifier import KnowledgeVerifier

SYSTEM_PROMPT = """You are a component of Gnosis AI, an autonomous knowledge discovery system.
Your role is the Domain Surveyor: you survey fields of science and mathematics to identify
their most important established results.

You must be:
- PRECISE: Only include results that a specialist would recognise as established
- HONEST: Epistemic status must accurately reflect the result's standing
- STRUCTURAL: Extract what each result says about fundamental structure, not just what it computes

Epistemic status categories:
- proven_theorem: Mathematically proven
- experimentally_confirmed: Confirmed by experiment to high precision
- established_framework: Widely accepted theoretical framework
- well_supported_conjecture: Strong evidence but not proven
- candidate_theory: Leading candidate, not yet confirmed
- conjectural: Proposed but unconfirmed
- numerical_result: Computationally verified"""


SURVEY_PROMPT = """Survey the field of **{field_name}** ({field_description}).

Identify the 12-18 most important established results in this field — proven theorems,
experimentally confirmed findings, and landmark frameworks that any specialist would
recognise as foundational.

For each result, provide:
1. "name": The standard name of the result
2. "authors": Key author(s) and year (e.g. "Bell (1964)")
3. "year": Publication year as integer
4. "epistemic_status": One of: proven_theorem, experimentally_confirmed, established_framework, well_supported_conjecture, candidate_theory, conjectural, numerical_result
5. "structural_conclusion": What this result tells us about the FUNDAMENTAL STRUCTURE of its domain. Not what it computes or predicts — what it says about how things are organised, related, or constrained at the deepest level. One or two sentences.
6. "source_citation": Brief citation

Return a JSON object with:
{{
  "field_id": "{field_id}",
  "field_name": "{field_name}",
  "results": [... list of results ...],
  "structural_conclusion": "A synthesis of what this field's results collectively say about fundamental structure. 2-3 sentences."
}}"""


SURVEY_FOCUSED_PROMPT = """Survey the field of **{field_name}** ({field_description})
with specific attention to the question: **{question}**

Identify the 10-15 most important established results in this field that are relevant
to this question — proven theorems, experimentally confirmed findings, and landmark
frameworks that bear on the question.

For each result, provide:
1. "name": The standard name of the result
2. "authors": Key author(s) and year
3. "year": Publication year as integer
4. "epistemic_status": One of: proven_theorem, experimentally_confirmed, established_framework, well_supported_conjecture, candidate_theory, conjectural, numerical_result
5. "structural_conclusion": What this result says about the question. Not what it computes — what it structurally implies about the answer. One or two sentences.
6. "source_citation": Brief citation

Return a JSON object with:
{{
  "field_id": "{field_id}",
  "field_name": "{field_name}",
  "results": [... list of results ...],
  "structural_conclusion": "What this field's results collectively say about the question. 2-3 sentences."
}}"""


class Surveyor:
    """Surveys domains and extracts established results with structural conclusions.

    v3: After survey, each result is verified against 5 external databases.
    Unverified results are automatically culled.
    """

    def __init__(self, api: ClaudeAPI, store: Store, verify: bool = True):
        self.api = api
        self.store = store
        self.verify = verify
        self._verifier = KnowledgeVerifier() if verify else None

    def survey(
        self,
        field: FieldInfo,
        question: str | None = None,
        force: bool = False,
    ) -> Domain:
        """Survey a domain. Returns cached result if already surveyed unless force=True."""

        # Check cache
        if not force and self.store.domain_is_surveyed(field.id):
            return self.store.load_domain(field.id)

        # Choose prompt based on mode
        if question:
            prompt = SURVEY_FOCUSED_PROMPT.format(
                field_name=field.name,
                field_description=field.description,
                field_id=field.id,
                question=question,
            )
        else:
            prompt = SURVEY_PROMPT.format(
                field_name=field.name,
                field_description=field.description,
                field_id=field.id,
            )

        # Query Claude
        data = self.api.query_json(prompt, system=SYSTEM_PROMPT)

        # Build domain
        results = []
        for r in data.get("results", []):
            if not isinstance(r, dict) or "name" not in r:
                continue
            result = Result(
                name=r["name"],
                authors=r.get("authors", ""),
                year=r.get("year", 0),
                domain_id=field.id,
                epistemic_status=r.get("epistemic_status", "established_framework"),
                structural_conclusion=r.get("structural_conclusion", ""),
                source_citation=r.get("source_citation", ""),
            )
            results.append(result)

        domain = Domain(
            id=field.id,
            name=field.name,
            category=field.category,
            description=field.description,
            results=[r.__dict__ for r in results],
            structural_conclusion=data.get("structural_conclusion", ""),
            surveyed=True,
            survey_timestamp=_now(),
        )

        # v3: Verify results against external databases and cull unverified
        if self.verify and self._verifier:
            domain = self._verify_and_cull(domain)

        # Cache
        self.store.save_domain(domain)
        return domain

    def _verify_and_cull(self, domain: Domain) -> Domain:
        """Verify each result against 5 external databases. Cull unverified.

        Adds _verification metadata to each result.
        Removes results that cannot be verified externally.
        """
        verified_results = []
        culled = []

        for r_dict in domain.results:
            name = r_dict.get("name", "")
            authors = r_dict.get("authors", "")
            year = r_dict.get("year", 0)

            structural_conclusion = r_dict.get("structural_conclusion", "")
            vr = self._verifier.verify_result(name, authors, year, structural_conclusion)
            r_dict["_verification"] = vr.to_dict()

            if vr.verdict in ("VERIFIED", "PARTIALLY_VERIFIED"):
                verified_results.append(r_dict)
            else:
                culled.append(r_dict)

        original_count = len(domain.results)
        domain.results = verified_results

        # Store culled results and verification stats as metadata
        if not hasattr(domain, '_verification_stats'):
            domain.__dict__["_verification_stats"] = {}
        domain.__dict__["_verification_stats"] = {
            "original_count": original_count,
            "verified_count": len(verified_results),
            "culled_count": len(culled),
            "verification_rate": len(verified_results) / original_count if original_count else 0,
            "culled_results": [c.get("name", "") for c in culled],
        }

        return domain
