"""Knowledge Verifier — 5-checkpoint external verification for surveyed results.

Every result Claude surveys gets checked against:
  1. Semantic Scholar (200M+ papers, citation counts)
  2. CrossRef (DOI verification, metadata)
  3. OpenAlex (250M+ works, concept mapping)
  4. arXiv (preprints, maths/physics)
  5. Wikipedia (notability signal)

Verdict is purely data-driven — Claude is NOT involved in the decision.
Results that can't be verified externally are CULLED from the pipeline.
"""

from __future__ import annotations

import re
import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from typing import Optional

import requests


@dataclass
class SourceResult:
    """Result from a single verification source."""
    found: bool = False
    title: str = ""
    citation_count: int = 0
    doi: str = ""
    year: int = 0
    url: str = ""
    extra: dict = field(default_factory=dict)


@dataclass
class VerificationResult:
    """Aggregated verification across all 5 sources."""
    result_name: str
    authors: str = ""
    claimed_year: int = 0
    semantic_scholar: SourceResult = field(default_factory=SourceResult)
    crossref: SourceResult = field(default_factory=SourceResult)
    openalex: SourceResult = field(default_factory=SourceResult)
    arxiv: SourceResult = field(default_factory=SourceResult)
    wikipedia: SourceResult = field(default_factory=SourceResult)

    @property
    def sources_confirmed(self) -> int:
        return sum(1 for s in [
            self.semantic_scholar, self.crossref,
            self.openalex, self.arxiv, self.wikipedia
        ] if s.found)

    @property
    def max_citations(self) -> int:
        return max(
            self.semantic_scholar.citation_count,
            self.openalex.citation_count,
            self.crossref.citation_count,
            0,
        )

    @property
    def verdict(self) -> str:
        n = self.sources_confirmed
        if n >= 3:
            return "VERIFIED"
        if n >= 1:
            return "PARTIALLY_VERIFIED"
        return "UNVERIFIED"

    @property
    def confidence(self) -> float:
        """0.0-1.0 confidence based on sources and citations."""
        source_score = min(self.sources_confirmed / 3.0, 1.0)
        cite_score = min(self.max_citations / 500.0, 1.0) if self.max_citations > 0 else 0.0
        return round(source_score * 0.7 + cite_score * 0.3, 3)

    def to_dict(self) -> dict:
        return {
            "result_name": self.result_name,
            "authors": self.authors,
            "claimed_year": self.claimed_year,
            "verdict": self.verdict,
            "sources_confirmed": self.sources_confirmed,
            "max_citations": self.max_citations,
            "confidence": self.confidence,
            "semantic_scholar": {"found": self.semantic_scholar.found, "citations": self.semantic_scholar.citation_count},
            "crossref": {"found": self.crossref.found, "doi": self.crossref.doi},
            "openalex": {"found": self.openalex.found, "citations": self.openalex.citation_count},
            "arxiv": {"found": self.arxiv.found},
            "wikipedia": {"found": self.wikipedia.found},
        }


@dataclass
class DomainVerification:
    """Verification results for an entire domain."""
    field_id: str
    field_name: str
    total_results: int = 0
    verified: int = 0
    partially_verified: int = 0
    unverified: int = 0
    culled: int = 0
    verification_rate: float = 0.0
    domain_verdict: str = ""  # TRUSTED | REVIEW | UNTRUSTED
    results: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "field_id": self.field_id,
            "field_name": self.field_name,
            "total_results": self.total_results,
            "verified": self.verified,
            "partially_verified": self.partially_verified,
            "unverified": self.unverified,
            "culled": self.culled,
            "verification_rate": round(self.verification_rate, 3),
            "domain_verdict": self.domain_verdict,
        }


def _title_similarity(a: str, b: str) -> float:
    """Simple word-overlap similarity between two titles."""
    words_a = set(re.findall(r'\w+', a.lower()))
    words_b = set(re.findall(r'\w+', b.lower()))
    if not words_a or not words_b:
        return 0.0
    overlap = words_a & words_b
    return len(overlap) / max(len(words_a), len(words_b))


class KnowledgeVerifier:
    """Verifies surveyed results against 5 independent academic databases.

    Usage:
        verifier = KnowledgeVerifier()
        result = verifier.verify_result("Bell's theorem", "Bell", 1964)
        print(result.verdict)  # "VERIFIED"
        print(result.sources_confirmed)  # 4
    """

    def __init__(self, rate_limit_delay: float = 0.3):
        self.rate_limit_delay = rate_limit_delay
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "GnosisAI/3.0 (knowledge-verification; mailto:contact@infinitography.com)"
        })
        self.stats = {"calls": 0, "errors": 0, "verified": 0, "culled": 0}

    def _wait(self):
        """Rate-limit pause between API calls."""
        time.sleep(self.rate_limit_delay)

    # ─── SOURCE 1: SEMANTIC SCHOLAR ───

    def _search_semantic_scholar(self, query: str) -> SourceResult:
        """Search Semantic Scholar for a result. Returns citation count and metadata."""
        try:
            self._wait()
            self.stats["calls"] += 1
            resp = self.session.get(
                "https://api.semanticscholar.org/graph/v1/paper/search",
                params={
                    "query": query[:200],
                    "limit": 3,
                    "fields": "title,citationCount,year,externalIds,authors",
                },
                timeout=15,
            )
            if resp.status_code == 429:
                time.sleep(3)
                resp = self.session.get(
                    "https://api.semanticscholar.org/graph/v1/paper/search",
                    params={"query": query[:200], "limit": 3,
                            "fields": "title,citationCount,year,externalIds,authors"},
                    timeout=15,
                )
            if resp.status_code != 200:
                return SourceResult()

            data = resp.json()
            papers = data.get("data", [])
            if not papers:
                return SourceResult()

            # Find best match by title similarity
            best = max(papers, key=lambda p: _title_similarity(query, p.get("title", "")))
            sim = _title_similarity(query, best.get("title", ""))
            if sim < 0.2:
                return SourceResult()

            ext_ids = best.get("externalIds", {}) or {}
            return SourceResult(
                found=True,
                title=best.get("title", ""),
                citation_count=best.get("citationCount", 0) or 0,
                year=best.get("year", 0) or 0,
                doi=ext_ids.get("DOI", ""),
                url=f"https://www.semanticscholar.org/paper/{best.get('paperId', '')}",
            )
        except Exception:
            self.stats["errors"] += 1
            return SourceResult()

    # ─── SOURCE 2: CROSSREF ───

    def _search_crossref(self, query: str, year: int = 0) -> SourceResult:
        """Search CrossRef for DOI verification."""
        try:
            self._wait()
            self.stats["calls"] += 1
            params = {
                "query": query[:200],
                "rows": 3,
                "mailto": "contact@infinitography.com",
            }
            resp = self.session.get(
                "https://api.crossref.org/works",
                params=params,
                timeout=15,
            )
            if resp.status_code != 200:
                return SourceResult()

            items = resp.json().get("message", {}).get("items", [])
            if not items:
                return SourceResult()

            # Find best match
            best = None
            best_sim = 0.0
            for item in items:
                titles = item.get("title", [])
                title = titles[0] if titles else ""
                sim = _title_similarity(query, title)
                if sim > best_sim:
                    best_sim = sim
                    best = item

            if not best or best_sim < 0.2:
                return SourceResult()

            titles = best.get("title", [])
            date_parts = best.get("published-print", best.get("published-online", {}))
            pub_year = 0
            if date_parts and date_parts.get("date-parts"):
                parts = date_parts["date-parts"][0]
                if parts:
                    pub_year = parts[0]

            ref_count = best.get("is-referenced-by-count", 0)

            return SourceResult(
                found=True,
                title=titles[0] if titles else "",
                citation_count=ref_count or 0,
                doi=best.get("DOI", ""),
                year=pub_year,
                url=f"https://doi.org/{best.get('DOI', '')}",
            )
        except Exception:
            self.stats["errors"] += 1
            return SourceResult()

    # ─── SOURCE 3: OPENALEX ───

    def _search_openalex(self, query: str) -> SourceResult:
        """Search OpenAlex for independent verification."""
        try:
            self._wait()
            self.stats["calls"] += 1
            resp = self.session.get(
                "https://api.openalex.org/works",
                params={
                    "search": query[:200],
                    "per_page": 3,
                    "mailto": "contact@infinitography.com",
                },
                timeout=15,
            )
            if resp.status_code != 200:
                return SourceResult()

            results = resp.json().get("results", [])
            if not results:
                return SourceResult()

            # Find best match
            best = max(results, key=lambda r: _title_similarity(query, r.get("title", "") or ""))
            sim = _title_similarity(query, best.get("title", "") or "")
            if sim < 0.2:
                return SourceResult()

            concepts = best.get("concepts", [])
            concept_names = [c.get("display_name", "") for c in concepts[:5]]

            return SourceResult(
                found=True,
                title=best.get("title", "") or "",
                citation_count=best.get("cited_by_count", 0) or 0,
                year=best.get("publication_year", 0) or 0,
                doi=(best.get("doi", "") or "").replace("https://doi.org/", ""),
                url=best.get("id", ""),
                extra={"concepts": concept_names},
            )
        except Exception:
            self.stats["errors"] += 1
            return SourceResult()

    # ─── SOURCE 4: ARXIV ───

    def _search_arxiv(self, query: str) -> SourceResult:
        """Search arXiv for preprints (maths/physics focus)."""
        try:
            self._wait()
            self.stats["calls"] += 1
            # arXiv API uses Atom XML
            clean_query = re.sub(r'[^\w\s]', ' ', query)
            resp = self.session.get(
                "http://export.arxiv.org/api/query",
                params={
                    "search_query": f"all:{clean_query[:150]}",
                    "max_results": 3,
                },
                timeout=15,
            )
            if resp.status_code != 200:
                return SourceResult()

            # Parse Atom XML
            ns = {"atom": "http://www.w3.org/2005/Atom"}
            root = ET.fromstring(resp.text)
            entries = root.findall("atom:entry", ns)
            if not entries:
                return SourceResult()

            # Find best match
            best = None
            best_sim = 0.0
            for entry in entries:
                title_el = entry.find("atom:title", ns)
                title = (title_el.text or "").strip().replace("\n", " ") if title_el is not None else ""
                sim = _title_similarity(query, title)
                if sim > best_sim:
                    best_sim = sim
                    best = entry

            if not best or best_sim < 0.15:
                return SourceResult()

            title_el = best.find("atom:title", ns)
            title = (title_el.text or "").strip().replace("\n", " ") if title_el is not None else ""
            id_el = best.find("atom:id", ns)
            arxiv_url = id_el.text if id_el is not None else ""
            published_el = best.find("atom:published", ns)
            pub_year = 0
            if published_el is not None and published_el.text:
                pub_year = int(published_el.text[:4])

            categories = []
            for cat in best.findall("{http://arxiv.org/schemas/atom}primary_category"):
                term = cat.get("term", "")
                if term:
                    categories.append(term)

            return SourceResult(
                found=True,
                title=title,
                year=pub_year,
                url=arxiv_url,
                extra={"categories": categories},
            )
        except Exception:
            self.stats["errors"] += 1
            return SourceResult()

    # ─── SOURCE 5: WIKIPEDIA ───

    def _search_wikipedia(self, query: str) -> SourceResult:
        """Check Wikipedia for notability (does this result have an article?)."""
        try:
            self._wait()
            self.stats["calls"] += 1
            resp = self.session.get(
                "https://en.wikipedia.org/w/api.php",
                params={
                    "action": "query",
                    "list": "search",
                    "srsearch": query[:150],
                    "srlimit": 3,
                    "format": "json",
                },
                timeout=10,
            )
            if resp.status_code != 200:
                return SourceResult()

            results = resp.json().get("query", {}).get("search", [])
            if not results:
                return SourceResult()

            # Check if any result title is a close match
            best = max(results, key=lambda r: _title_similarity(query, r.get("title", "")))
            sim = _title_similarity(query, best.get("title", ""))
            if sim < 0.25:
                return SourceResult()

            title = best.get("title", "")
            return SourceResult(
                found=True,
                title=title,
                url=f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}",
            )
        except Exception:
            self.stats["errors"] += 1
            return SourceResult()

    # ─── MAIN VERIFICATION ───

    def verify_result(
        self, name: str, authors: str = "", year: int = 0
    ) -> VerificationResult:
        """Verify a single surveyed result against all 5 sources.

        Args:
            name: The standard name of the result (e.g., "Bell's theorem")
            authors: Author(s) and year string (e.g., "Bell (1964)")
            year: Publication year

        Returns:
            VerificationResult with verdict: VERIFIED, PARTIALLY_VERIFIED, or UNVERIFIED
        """
        # Build search queries
        primary_query = name
        author_query = f"{name} {authors}".strip() if authors else name

        return VerificationResult(
            result_name=name,
            authors=authors,
            claimed_year=year,
            semantic_scholar=self._search_semantic_scholar(author_query),
            crossref=self._search_crossref(author_query, year),
            openalex=self._search_openalex(author_query),
            arxiv=self._search_arxiv(primary_query),
            wikipedia=self._search_wikipedia(primary_query),
        )

    def verify_domain(self, domain_data: dict) -> DomainVerification:
        """Verify all results in a domain survey. Cull unverified results.

        Args:
            domain_data: The domain survey dict from Surveyor (has "results" list)

        Returns:
            DomainVerification with verified/culled counts and domain verdict.
            The domain_data dict is MODIFIED IN PLACE — unverified results are removed.
        """
        field_id = domain_data.get("field_id", "unknown")
        field_name = domain_data.get("field_name", "unknown")
        results = domain_data.get("results", [])

        dv = DomainVerification(
            field_id=field_id,
            field_name=field_name,
            total_results=len(results),
        )

        verified_results = []
        culled_results = []

        for r in results:
            name = r.get("name", "")
            authors = r.get("authors", "")
            year = r.get("year", 0)

            vr = self.verify_result(name, authors, year)
            r["_verification"] = vr.to_dict()

            if vr.verdict == "VERIFIED":
                dv.verified += 1
                verified_results.append(r)
                self.stats["verified"] += 1
            elif vr.verdict == "PARTIALLY_VERIFIED":
                dv.partially_verified += 1
                verified_results.append(r)
                self.stats["verified"] += 1
            else:
                dv.unverified += 1
                dv.culled += 1
                culled_results.append(r)
                self.stats["culled"] += 1

        # Update domain data — keep only verified results
        domain_data["results"] = verified_results
        domain_data["_culled_results"] = culled_results
        dv.verification_rate = len(verified_results) / len(results) if results else 0.0

        # Domain verdict (purely data-driven, no Claude involvement)
        if dv.verification_rate >= 0.80:
            dv.domain_verdict = "TRUSTED"
        elif dv.verification_rate >= 0.60:
            dv.domain_verdict = "REVIEW"
        else:
            dv.domain_verdict = "UNTRUSTED"

        dv.results = [r.get("_verification", {}) for r in verified_results]
        return dv

    def audit_taxonomy(self, all_domains: list[dict]) -> dict:
        """Audit all domains in the taxonomy. Returns domains categorised by trust level.

        This is a purely data-driven audit — no Claude involvement.
        Domains are judged solely by what percentage of their results
        can be verified in external academic databases.

        Args:
            all_domains: List of domain survey dicts

        Returns:
            Dict with trusted/review/untrusted domain lists and summary stats.
        """
        trusted = []
        review = []
        untrusted = []

        for domain in all_domains:
            dv = self.verify_domain(domain)
            entry = dv.to_dict()

            if dv.domain_verdict == "TRUSTED":
                trusted.append(entry)
            elif dv.domain_verdict == "REVIEW":
                review.append(entry)
            else:
                untrusted.append(entry)

        return {
            "total_domains": len(all_domains),
            "trusted": len(trusted),
            "review": len(review),
            "untrusted": len(untrusted),
            "trusted_domains": trusted,
            "review_domains": review,
            "untrusted_domains": untrusted,
            "overall_verification_rate": (
                sum(d["verification_rate"] for d in trusted + review + untrusted)
                / len(all_domains) if all_domains else 0.0
            ),
            "stats": dict(self.stats),
        }
