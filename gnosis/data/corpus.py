"""Corpus Manager — indexed convergence corpus for cross-run querying."""

from __future__ import annotations

from gnosis.data.models import Convergence, ConfidenceCategory
from gnosis.data.store import Store
from gnosis.data.taxonomy import Taxonomy


class CorpusManager:
    """Indexed convergence corpus for cross-run querying.

    Loads all convergences from the Store into memory and builds indexes
    for fast querying by field, category, run, type, and confidence.

    Why not a database? Because:
    - Consistent with v1 architecture (no new dependency)
    - ~5,000 convergences × ~2KB = ~10MB — trivially fits in memory
    - Index builds in <1 second
    - Compatible with git versioning and Bitcoin timestamping
    """

    def __init__(self, store: Store, taxonomy: Taxonomy):
        self.store = store
        self.taxonomy = taxonomy

        # In-memory indexes
        self._by_field: dict[str, list[str]] = {}
        self._by_category_pair: dict[str, list[str]] = {}
        self._by_run: dict[str, list[str]] = {}
        self._by_type: dict[str, list[str]] = {}
        self._by_confidence: dict[str, list[str]] = {}
        self._field_convergence_count: dict[str, int] = {}
        self._negative_ids: list[str] = []
        self._all_ids: list[str] = []

        self._build_index()

    def _build_index(self):
        """Build in-memory indexes from stored convergences."""
        for conv in self.store.list_convergences():
            self._index_convergence(conv)

    def _index_convergence(self, conv: Convergence):
        """Add a convergence to all indexes."""
        cid = conv.id
        self._all_ids.append(cid)

        # Track negatives separately
        if conv.negative:
            self._negative_ids.append(cid)
            return

        # Field index
        for field_id in conv.domains:
            self._by_field.setdefault(field_id, []).append(cid)
            self._field_convergence_count[field_id] = (
                self._field_convergence_count.get(field_id, 0) + 1
            )

        # Category pair index
        cats = sorted(set(self.field_category(d) for d in conv.domains))
        cat_key = "×".join(cats) if len(cats) > 1 else cats[0] if cats else "unknown"
        self._by_category_pair.setdefault(cat_key, []).append(cid)

        # Run index
        if conv.discovered_in_run:
            self._by_run.setdefault(conv.discovered_in_run, []).append(cid)

        # Comparison type index
        comp_type = getattr(conv, "comparison_type", "pairwise")
        self._by_type.setdefault(comp_type, []).append(cid)

        # Confidence index
        ea = conv.get_ea()
        if ea.confidence > 0:
            tier = ConfidenceCategory.from_score(ea.confidence).value
            self._by_confidence.setdefault(tier, []).append(cid)

    def add(self, conv: Convergence):
        """Add a convergence to the corpus (indexes + store)."""
        self.store.save_convergence(conv)
        self._index_convergence(conv)

    # ─── Query Methods ───

    def field_category(self, field_id: str) -> str:
        """Look up the category for a field."""
        field = self.taxonomy.get(field_id)
        return field.category if field else "unknown"

    def convergences_for_field(self, field_id: str) -> list[Convergence]:
        """All convergences involving a specific field."""
        ids = self._by_field.get(field_id, [])
        return [c for cid in ids if (c := self.store.load_convergence(cid)) is not None]

    def convergences_for_category_pair(self, cat_a: str, cat_b: str) -> list[Convergence]:
        """All convergences between two categories."""
        cats = sorted(set([cat_a, cat_b]))
        key = "×".join(cats) if len(cats) > 1 else cats[0] if cats else "unknown"
        ids = self._by_category_pair.get(key, [])
        return [c for cid in ids if (c := self.store.load_convergence(cid)) is not None]

    def convergences_for_run(self, run_id: str) -> list[Convergence]:
        """All convergences from a specific run."""
        ids = self._by_run.get(run_id, [])
        return [c for cid in ids if (c := self.store.load_convergence(cid)) is not None]

    def convergences_by_type(self, comparison_type: str) -> list[Convergence]:
        """All convergences of a specific comparison type."""
        ids = self._by_type.get(comparison_type, [])
        return [c for cid in ids if (c := self.store.load_convergence(cid)) is not None]

    def convergences_by_confidence(self, tier: str) -> list[Convergence]:
        """All convergences at a specific confidence tier."""
        ids = self._by_confidence.get(tier, [])
        return [c for cid in ids if (c := self.store.load_convergence(cid)) is not None]

    def all_convergences(self, include_negative: bool = False) -> list[Convergence]:
        """All convergences in the corpus."""
        convs = []
        for cid in self._all_ids:
            c = self.store.load_convergence(cid)
            if c is not None:
                if include_negative or not c.negative:
                    convs.append(c)
        return convs

    def hub_fields(self, min_convergences: int = 5) -> list[tuple[str, int]]:
        """Fields with the most convergences (sorted descending)."""
        hubs = [
            (f, c)
            for f, c in self._field_convergence_count.items()
            if c >= min_convergences
        ]
        return sorted(hubs, key=lambda x: -x[1])

    def explored_pairs(self) -> set[tuple[str, str]]:
        """Set of all (field_a, field_b) pairs already compared (including negatives)."""
        pairs: set[tuple[str, str]] = set()
        for cid in self._all_ids:
            c = self.store.load_convergence(cid)
            if c is not None and len(c.domains) == 2:
                pairs.add(tuple(sorted(c.domains)))
        return pairs

    def transitivity_candidates(self) -> list[tuple[str, str, str]]:
        """Find (A, B, C) where A↔B and B↔C converge but A↔C hasn't been explored.

        Returns list of (field_a, hub_field, field_c) tuples.
        """
        explored = self.explored_pairs()
        candidates = []

        for field_b, count in self._field_convergence_count.items():
            if count < 2:
                continue

            # Get all fields that converge with B
            partners = set()
            for conv_id in self._by_field.get(field_b, []):
                conv = self.store.load_convergence(conv_id)
                if conv is not None:
                    for d in conv.domains:
                        if d != field_b:
                            partners.add(d)

            partner_list = sorted(partners)
            for i, a in enumerate(partner_list):
                for c in partner_list[i + 1:]:
                    if tuple(sorted([a, c])) not in explored:
                        candidates.append((a, field_b, c))

        return candidates

    def negatives(self) -> list[Convergence]:
        """All negative convergences (informative absences)."""
        return [
            c
            for cid in self._negative_ids
            if (c := self.store.load_convergence(cid)) is not None
        ]

    def save_negative(self, field_a: str, field_b: str, reason: str, run_id: str = ""):
        """Record that a comparison found NO convergence."""
        neg = Convergence(
            structural_claim=f"No convergence: {reason}",
            convergence_type="none",
            domains=[field_a, field_b],
            domain_names=[
                (self.taxonomy.get(field_a) or type("", (), {"name": field_a})).name,
                (self.taxonomy.get(field_b) or type("", (), {"name": field_b})).name,
            ],
            comparison_type="negative",
            source_categories=sorted(set([
                self.field_category(field_a),
                self.field_category(field_b),
            ])),
            negative=True,
            discovered_in_run=run_id,
        )
        self.add(neg)
        return neg

    def category_pair_counts(self) -> list[tuple[str, int]]:
        """Convergence count per category pair, sorted descending."""
        return sorted(
            [(k, len(v)) for k, v in self._by_category_pair.items()],
            key=lambda x: -x[1],
        )

    def stats(self) -> dict:
        """Corpus statistics."""
        total_non_neg = sum(
            len(v) for v in self._by_field.values()
        ) // max(1, len(set(
            d for ids in self._by_field.values() for d in ids
        )) // max(1, len(self._by_field)))

        return {
            "total_convergences": len(self._all_ids) - len(self._negative_ids),
            "total_negative": len(self._negative_ids),
            "total_fields_explored": len(self._field_convergence_count),
            "total_category_pairs": len(self._by_category_pair),
            "total_runs": len(self._by_run),
            "by_confidence": {k: len(v) for k, v in self._by_confidence.items()},
            "by_comparison_type": {k: len(v) for k, v in self._by_type.items()},
            "hubs": self.hub_fields(min_convergences=3),
            "top_category_pairs": self.category_pair_counts()[:10],
        }
