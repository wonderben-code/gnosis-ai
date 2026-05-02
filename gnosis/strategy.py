"""Search Strategy Engine — decides what to explore next in the combinatorial space."""

from __future__ import annotations

import itertools
import random
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from gnosis.data.models import Convergence, Domain
from gnosis.data.taxonomy import Taxonomy, FieldInfo


# ─── Category Distance Scoring ───
# Higher = more disparate = higher discovery value = run first
# Symmetric: stored with sorted() category names
# Category names MUST match taxonomy/fields.json exactly
CATEGORY_DISTANCE = {
    # Original 8 categories
    ("Biology", "Mathematics"): 1.0,
    ("Mathematics", "Social & Cognitive Sciences"): 0.95,
    ("Physics", "Social & Cognitive Sciences"): 1.0,
    ("Biology", "Physics"): 0.95,
    ("Biology", "Social & Cognitive Sciences"): 0.85,
    ("Biology", "Computer Science"): 0.9,
    ("Computer Science", "Social & Cognitive Sciences"): 0.9,
    ("Chemistry", "Social & Cognitive Sciences"): 0.85,
    ("Chemistry", "Mathematics"): 0.8,
    ("Earth & Space Sciences", "Social & Cognitive Sciences"): 0.85,
    ("Earth & Space Sciences", "Mathematics"): 0.8,
    ("Biology", "Earth & Space Sciences"): 0.75,
    ("Earth & Space Sciences", "Physics"): 0.7,
    ("Chemistry", "Physics"): 0.6,
    ("Biology", "Chemistry"): 0.5,
    ("Mathematics", "Physics"): 0.5,
    ("Computer Science", "Mathematics"): 0.4,
    ("Computer Science", "Physics"): 0.5,
    ("Chemistry", "Earth & Space Sciences"): 0.4,
    ("Cross-Disciplinary", "Physics"): 0.3,
    ("Cross-Disciplinary", "Mathematics"): 0.3,
    ("Computer Science", "Cross-Disciplinary"): 0.3,
    ("Biology", "Cross-Disciplinary"): 0.5,
    ("Chemistry", "Cross-Disciplinary"): 0.5,
    ("Cross-Disciplinary", "Social & Cognitive Sciences"): 0.5,
    ("Cross-Disciplinary", "Earth & Space Sciences"): 0.5,
    # v2 new categories: Information Sciences, Engineering & Technology, Medicine & Health
    ("Biology", "Information Sciences"): 0.95,
    ("Information Sciences", "Social & Cognitive Sciences"): 0.85,
    ("Information Sciences", "Physics"): 0.7,
    ("Chemistry", "Information Sciences"): 0.8,
    ("Information Sciences", "Mathematics"): 0.3,
    ("Computer Science", "Information Sciences"): 0.2,
    ("Earth & Space Sciences", "Information Sciences"): 0.75,
    ("Cross-Disciplinary", "Information Sciences"): 0.4,
    ("Engineering & Technology", "Mathematics"): 0.7,
    ("Engineering & Technology", "Social & Cognitive Sciences"): 0.8,
    ("Biology", "Engineering & Technology"): 0.7,
    ("Biology", "Medicine & Health"): 0.3,
    ("Medicine & Health", "Physics"): 0.75,
    ("Mathematics", "Medicine & Health"): 0.85,
    ("Medicine & Health", "Social & Cognitive Sciences"): 0.6,
    ("Engineering & Technology", "Physics"): 0.4,
    ("Chemistry", "Engineering & Technology"): 0.4,
    ("Chemistry", "Medicine & Health"): 0.4,
    ("Earth & Space Sciences", "Medicine & Health"): 0.7,
    ("Engineering & Technology", "Medicine & Health"): 0.5,
    ("Earth & Space Sciences", "Engineering & Technology"): 0.5,
    ("Engineering & Technology", "Information Sciences"): 0.3,
    ("Information Sciences", "Medicine & Health"): 0.7,
    ("Computer Science", "Engineering & Technology"): 0.3,
    ("Computer Science", "Medicine & Health"): 0.8,
    ("Cross-Disciplinary", "Engineering & Technology"): 0.4,
    ("Cross-Disciplinary", "Medicine & Health"): 0.5,
}


def category_distance(cat_a: str, cat_b: str) -> float:
    """Score distance between two categories. Higher = more disparate."""
    if cat_a == cat_b:
        return 0.1
    key = tuple(sorted([cat_a, cat_b]))
    return CATEGORY_DISTANCE.get(key, 0.7)


class StrategyType(str, Enum):
    CROSS_CATEGORY_PRIORITY = "cross_category_priority"
    EXHAUSTIVE_PAIRWISE = "exhaustive_pairwise"
    TRANSITIVITY_PROBE = "transitivity_probe"
    HUB_EXPANSION = "hub_expansion"
    CLUSTER_GUIDED = "cluster_guided"
    RANDOM_SAMPLE = "random_sample"
    USER_SPECIFIED = "user_specified"


@dataclass
class ComparisonTask:
    """A pending comparison to be executed."""

    fields: list[str]       # Field IDs (2 for pairwise, 3+ for multi-field)
    priority: float         # Higher = run sooner
    strategy: str           # StrategyType value
    reason: str             # Why this task was generated
    field_names: list[str] = field(default_factory=list)
    categories: list[str] = field(default_factory=list)

    @property
    def is_multi_field(self) -> bool:
        return len(self.fields) > 2

    @property
    def pair_key(self) -> tuple[str, ...]:
        return tuple(sorted(self.fields))


class SearchStrategy:
    """Decides what to explore next in the combinatorial space.

    Takes a Taxonomy + existing corpus data, produces a priority-sorted
    list of ComparisonTasks. The orchestrator pulls tasks from the top.
    """

    def __init__(self, taxonomy: Taxonomy, explored_pairs: set[tuple[str, str]] | None = None):
        self.taxonomy = taxonomy
        self.explored_pairs: set[tuple[str, str]] = explored_pairs or set()

    def generate_tasks(
        self,
        strategy: StrategyType,
        domains: list[Domain] | None = None,
        **kwargs,
    ) -> list[ComparisonTask]:
        """Generate comparison tasks for a given strategy."""
        generators = {
            StrategyType.CROSS_CATEGORY_PRIORITY: self._cross_category_priority,
            StrategyType.EXHAUSTIVE_PAIRWISE: self._exhaustive_pairwise,
            StrategyType.TRANSITIVITY_PROBE: self._transitivity_probe,
            StrategyType.HUB_EXPANSION: self._hub_expansion,
            StrategyType.RANDOM_SAMPLE: self._random_sample,
            StrategyType.USER_SPECIFIED: self._user_specified,
        }
        gen = generators.get(strategy)
        if gen is None:
            raise ValueError(f"Unknown strategy: {strategy}")
        return gen(domains=domains, **kwargs)

    def _cross_category_priority(
        self,
        domains: list[Domain] | None = None,
        **kwargs,
    ) -> list[ComparisonTask]:
        """All cross-category pairs, ordered by category distance (most disparate first)."""
        fields = list(self.taxonomy.fields.values()) if domains is None else None
        tasks = []

        if domains is not None:
            # Use provided domains
            for i, da in enumerate(domains):
                for db in domains[i + 1:]:
                    if da.category == db.category:
                        continue
                    pair = tuple(sorted([da.id, db.id]))
                    if pair in self.explored_pairs:
                        continue
                    dist = category_distance(da.category, db.category)
                    tasks.append(ComparisonTask(
                        fields=[da.id, db.id],
                        priority=dist,
                        strategy=StrategyType.CROSS_CATEGORY_PRIORITY.value,
                        reason=f"{da.category} × {db.category} (distance={dist:.2f})",
                        field_names=[da.name, db.name],
                        categories=[da.category, db.category],
                    ))
        else:
            # Use all taxonomy fields
            for i, fa in enumerate(fields):
                for fb in fields[i + 1:]:
                    if fa.category == fb.category:
                        continue
                    pair = tuple(sorted([fa.id, fb.id]))
                    if pair in self.explored_pairs:
                        continue
                    dist = category_distance(fa.category, fb.category)
                    tasks.append(ComparisonTask(
                        fields=[fa.id, fb.id],
                        priority=dist,
                        strategy=StrategyType.CROSS_CATEGORY_PRIORITY.value,
                        reason=f"{fa.category} × {fb.category} (distance={dist:.2f})",
                        field_names=[fa.name, fb.name],
                        categories=[fa.category, fb.category],
                    ))

        tasks.sort(key=lambda t: t.priority, reverse=True)
        return tasks

    def _exhaustive_pairwise(
        self,
        domains: list[Domain] | None = None,
        **kwargs,
    ) -> list[ComparisonTask]:
        """All C(N,2) pairs, cross-category first, then within-category."""
        fields = list(self.taxonomy.fields.values()) if domains is None else None
        tasks = []

        if domains is not None:
            for i, da in enumerate(domains):
                for db in domains[i + 1:]:
                    pair = tuple(sorted([da.id, db.id]))
                    if pair in self.explored_pairs:
                        continue
                    dist = category_distance(da.category, db.category)
                    tasks.append(ComparisonTask(
                        fields=[da.id, db.id],
                        priority=dist,
                        strategy=StrategyType.EXHAUSTIVE_PAIRWISE.value,
                        reason=f"exhaustive {'cross' if da.category != db.category else 'within'}-category",
                        field_names=[da.name, db.name],
                        categories=[da.category, db.category],
                    ))
        else:
            for i, fa in enumerate(fields):
                for fb in fields[i + 1:]:
                    pair = tuple(sorted([fa.id, fb.id]))
                    if pair in self.explored_pairs:
                        continue
                    dist = category_distance(fa.category, fb.category)
                    tasks.append(ComparisonTask(
                        fields=[fa.id, fb.id],
                        priority=dist,
                        strategy=StrategyType.EXHAUSTIVE_PAIRWISE.value,
                        reason=f"exhaustive {'cross' if fa.category != fb.category else 'within'}-category",
                        field_names=[fa.name, fb.name],
                        categories=[fa.category, fb.category],
                    ))

        tasks.sort(key=lambda t: t.priority, reverse=True)
        return tasks

    def _transitivity_probe(
        self,
        convergences: list[Convergence] | None = None,
        **kwargs,
    ) -> list[ComparisonTask]:
        """If A↔B and B↔C share convergences, test A↔C.

        Requires existing convergences as input.
        """
        if not convergences:
            return []

        # Build adjacency: field → set of fields it converges with
        adjacency: dict[str, set[str]] = {}
        for c in convergences:
            if c.negative or len(c.domains) != 2:
                continue
            a, b = c.domains[0], c.domains[1]
            adjacency.setdefault(a, set()).add(b)
            adjacency.setdefault(b, set()).add(a)

        tasks = []
        seen = set()

        for field_b, partners in adjacency.items():
            partner_list = sorted(partners)
            for i, a in enumerate(partner_list):
                for c_field in partner_list[i + 1:]:
                    pair = tuple(sorted([a, c_field]))
                    if pair in self.explored_pairs or pair in seen:
                        continue
                    seen.add(pair)

                    fa = self.taxonomy.get(a)
                    fc = self.taxonomy.get(c_field)
                    fb = self.taxonomy.get(field_b)
                    if not fa or not fc or not fb:
                        continue

                    dist = category_distance(fa.category, fc.category)
                    tasks.append(ComparisonTask(
                        fields=[a, c_field],
                        priority=dist + 0.2,  # boost transitivity probes
                        strategy=StrategyType.TRANSITIVITY_PROBE.value,
                        reason=f"transitivity via {fb.name}: {fa.name}↔{fb.name} and {fb.name}↔{fc.name} exist",
                        field_names=[fa.name, fc.name],
                        categories=[fa.category, fc.category],
                    ))

        tasks.sort(key=lambda t: t.priority, reverse=True)
        return tasks

    def _hub_expansion(
        self,
        convergences: list[Convergence] | None = None,
        min_convergences: int = 5,
        max_group_size: int = 5,
        **kwargs,
    ) -> list[ComparisonTask]:
        """Fields with many convergences → multi-field groups.

        For each hub field, take its top converging partners and create
        a multi-field comparison task.
        """
        if not convergences:
            return []

        # Count convergences per field
        field_counts: dict[str, int] = {}
        field_partners: dict[str, list[str]] = {}

        for c in convergences:
            if c.negative:
                continue
            for d in c.domains:
                field_counts[d] = field_counts.get(d, 0) + 1
                for other in c.domains:
                    if other != d:
                        field_partners.setdefault(d, []).append(other)

        tasks = []
        for field_id, count in sorted(field_counts.items(), key=lambda x: -x[1]):
            if count < min_convergences:
                break

            fi = self.taxonomy.get(field_id)
            if not fi:
                continue

            # Get top partners (most frequent)
            partners = field_partners.get(field_id, [])
            partner_freq: dict[str, int] = {}
            for p in partners:
                partner_freq[p] = partner_freq.get(p, 0) + 1

            top_partners = sorted(partner_freq.keys(), key=lambda p: -partner_freq[p])
            group = [field_id] + top_partners[:max_group_size - 1]

            if len(group) < 3:
                continue

            group_key = tuple(sorted(group))
            field_infos = [self.taxonomy.get(f) for f in group]
            names = [f.name for f in field_infos if f]
            cats = list(set(f.category for f in field_infos if f))

            tasks.append(ComparisonTask(
                fields=list(group),
                priority=0.9 + count * 0.01,  # high priority for hubs
                strategy=StrategyType.HUB_EXPANSION.value,
                reason=f"hub: {fi.name} has {count} convergences, grouping with top partners",
                field_names=names,
                categories=cats,
            ))

        tasks.sort(key=lambda t: t.priority, reverse=True)
        return tasks

    def _random_sample(
        self,
        n: int = 20,
        domains: list[Domain] | None = None,
        **kwargs,
    ) -> list[ComparisonTask]:
        """Random pairs for serendipitous discovery."""
        fields = list(self.taxonomy.fields.values()) if domains is None else None
        all_pairs = []

        if domains is not None:
            for i, da in enumerate(domains):
                for db in domains[i + 1:]:
                    pair = tuple(sorted([da.id, db.id]))
                    if pair not in self.explored_pairs:
                        all_pairs.append((da.id, db.id, da.name, db.name, da.category, db.category))
        else:
            field_list = list(self.taxonomy.fields.values())
            for i, fa in enumerate(field_list):
                for fb in field_list[i + 1:]:
                    pair = tuple(sorted([fa.id, fb.id]))
                    if pair not in self.explored_pairs:
                        all_pairs.append((fa.id, fb.id, fa.name, fb.name, fa.category, fb.category))

        sample = random.sample(all_pairs, min(n, len(all_pairs)))

        return [
            ComparisonTask(
                fields=[a_id, b_id],
                priority=0.5,  # neutral priority
                strategy=StrategyType.RANDOM_SAMPLE.value,
                reason="random serendipity sample",
                field_names=[a_name, b_name],
                categories=[a_cat, b_cat],
            )
            for a_id, b_id, a_name, b_name, a_cat, b_cat in sample
        ]

    def _user_specified(
        self,
        field_ids: list[str] | None = None,
        **kwargs,
    ) -> list[ComparisonTask]:
        """User-specified fields → comparison task."""
        if not field_ids or len(field_ids) < 2:
            return []

        infos = [self.taxonomy.get(f) for f in field_ids]
        names = [f.name for f in infos if f]
        cats = list(set(f.category for f in infos if f))

        if len(field_ids) == 2:
            dist = category_distance(
                infos[0].category if infos[0] else "unknown",
                infos[1].category if infos[1] else "unknown",
            )
        else:
            dist = 0.9  # multi-field always high priority

        return [ComparisonTask(
            fields=field_ids,
            priority=dist,
            strategy=StrategyType.USER_SPECIFIED.value,
            reason="user-specified comparison",
            field_names=names,
            categories=cats,
        )]

    def update_priorities(
        self,
        tasks: list[ComparisonTask],
        new_convergences: list[Convergence],
        boost_per_convergence: float = 0.1,
    ) -> list[ComparisonTask]:
        """After discoveries, boost priority of tasks involving productive fields."""
        if not new_convergences:
            return tasks

        # Count new convergences per field
        field_boost: dict[str, float] = {}
        for c in new_convergences:
            if c.negative:
                continue
            for d in c.domains:
                field_boost[d] = field_boost.get(d, 0) + boost_per_convergence

        # Apply boosts
        for task in tasks:
            for f in task.fields:
                task.priority += field_boost.get(f, 0)

        tasks.sort(key=lambda t: t.priority, reverse=True)
        return tasks

    def summary(self, tasks: list[ComparisonTask]) -> dict:
        """Summary statistics for a task list."""
        by_strategy: dict[str, int] = {}
        cross = 0
        within = 0
        multi = 0

        for t in tasks:
            by_strategy[t.strategy] = by_strategy.get(t.strategy, 0) + 1
            if t.is_multi_field:
                multi += 1
            elif len(set(t.categories)) > 1:
                cross += 1
            else:
                within += 1

        return {
            "total_tasks": len(tasks),
            "cross_category": cross,
            "within_category": within,
            "multi_field": multi,
            "by_strategy": by_strategy,
            "top_priority": tasks[0].priority if tasks else 0,
        }
