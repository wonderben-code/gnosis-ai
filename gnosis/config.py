"""Configuration management for Gnosis AI."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Config:
    """Runtime configuration."""

    # API
    api_key: str = ""
    model_fast: str = "claude-sonnet-4-20250514"
    model_deep: str = "claude-opus-4-20250514"

    # Paths
    data_dir: Path = field(default_factory=lambda: Path("data"))
    taxonomy_path: Path = field(default_factory=lambda: Path("taxonomy/fields.json"))

    # Limits
    max_cost_usd: float = 100.0
    max_hours: float = 12.0
    max_retries: int = 3

    # Quality
    min_strength: float = 0.3
    min_confidence: float = 0.4

    # Auto mode
    min_discovery_rate: float = 0.5  # stop if < this many discoveries per cycle

    @classmethod
    def load(cls, project_root: Path | None = None) -> Config:
        """Load config from environment and optional config file."""
        if project_root is None:
            project_root = _find_project_root()

        cfg = cls()
        cfg.data_dir = project_root / "data"
        cfg.taxonomy_path = project_root / "taxonomy" / "fields.json"

        # API key from environment
        cfg.api_key = os.environ.get("ANTHROPIC_API_KEY", "")

        # Load from config file if it exists
        config_file = project_root / "gnosis.json"
        if config_file.exists():
            with open(config_file) as f:
                data = json.load(f)
            for key, val in data.items():
                if hasattr(cfg, key):
                    if key.endswith("_dir") or key.endswith("_path"):
                        setattr(cfg, key, Path(val))
                    else:
                        setattr(cfg, key, val)

        return cfg

    def ensure_dirs(self):
        """Create data directories if they don't exist."""
        for subdir in ["domains", "runs", "convergences", "findings"]:
            (self.data_dir / subdir).mkdir(parents=True, exist_ok=True)


def _find_project_root() -> Path:
    """Walk up from cwd to find the project root (has taxonomy/ dir)."""
    current = Path.cwd()
    for parent in [current, *current.parents]:
        if (parent / "taxonomy").is_dir():
            return parent
        if (parent / "gnosis").is_dir() and (parent / "docs").is_dir():
            return parent
    return current
