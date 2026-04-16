"""Domain Surveyor — surveys a field and extracts established results."""

from __future__ import annotations

from gnosis.api.claude import ClaudeAPI
from gnosis.data.models import Domain, Result
from gnosis.data.store import Store
from gnosis.data.taxonomy import FieldInfo

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
    """Surveys domains and extracts established results with structural conclusions."""

    def __init__(self, api: ClaudeAPI, store: Store):
        self.api = api
        self.store = store

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
            survey_timestamp=results[0].id[:8] if results else "",  # approximate
        )

        # Cache
        self.store.save_domain(domain)
        return domain
