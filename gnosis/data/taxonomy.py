"""Field taxonomy loader."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from gnosis.config import Config


class FieldInfo:
    """A field in the taxonomy."""

    def __init__(self, id: str, name: str, description: str, category: str):
        self.id = id
        self.name = name
        self.description = description
        self.category = category

    def __repr__(self):
        return f"FieldInfo({self.id!r}, {self.name!r})"


class Taxonomy:
    """The field taxonomy — all domains Gnosis can survey."""

    def __init__(self, config: Config):
        self.fields: dict[str, FieldInfo] = {}
        self.categories: dict[str, list[FieldInfo]] = {}
        self._load(config.taxonomy_path)

    def _load(self, path: Path):
        data = json.loads(path.read_text())
        for cat in data["categories"]:
            cat_name = cat["name"]
            self.categories[cat_name] = []
            for f in cat["fields"]:
                field = FieldInfo(
                    id=f["id"],
                    name=f["name"],
                    description=f["description"],
                    category=cat_name,
                )
                self.fields[f["id"]] = field
                self.categories[cat_name].append(field)

    def get(self, field_id: str) -> Optional[FieldInfo]:
        return self.fields.get(field_id)

    def resolve(self, spec: str) -> list[FieldInfo]:
        """Resolve a field spec to a list of fields.

        Accepts:
        - A field ID: "quantum_foundations"
        - A category: "physics", "mathematics", "all"
        - Comma-separated: "quantum_foundations,topology,ecology"
        """
        spec = spec.strip().lower()

        if spec == "all":
            return list(self.fields.values())

        # Check if it's a category
        for cat_name, cat_fields in self.categories.items():
            if spec == cat_name.lower() or spec == f"all_{cat_name.lower()}":
                return cat_fields

        # Check if it's a single field
        if spec in self.fields:
            return [self.fields[spec]]

        # Try comma-separated
        if "," in spec:
            result = []
            for part in spec.split(","):
                result.extend(self.resolve(part.strip()))
            return result

        raise ValueError(
            f"Unknown field or category: {spec!r}. "
            f"Use 'gnosis fields' to see available fields."
        )

    @property
    def all_ids(self) -> list[str]:
        return list(self.fields.keys())

    @property
    def count(self) -> int:
        return len(self.fields)
