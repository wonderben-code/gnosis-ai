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
    model_fast: str = "claude-opus-4-20250514"
    model_deep: str = "claude-opus-4-20250514"
    model_fallback: str = "claude-sonnet-4-20250514"

    # Paths
    data_dir: Path = field(default_factory=lambda: Path("data"))
    taxonomy_path: Path = field(default_factory=lambda: Path("taxonomy/fields.json"))

    # Limits
    max_cost_usd: float = 50.0
    max_hours: float = 12.0
    max_retries: int = 3

    # Quality
    min_strength: float = 0.3
    min_confidence: float = 0.3

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

        # Load from config file first (if it exists)
        config_file = project_root / "gnosis.json"
        if config_file.exists():
            with open(config_file) as f:
                data = json.load(f)

            # Map JSON keys to config attributes
            key_map = {"anthropic_api_key": "api_key"}

            for key, val in data.items():
                attr = key_map.get(key, key)
                if hasattr(cfg, attr):
                    if attr.endswith("_dir") or attr.endswith("_path"):
                        setattr(cfg, attr, Path(val))
                    else:
                        setattr(cfg, attr, val)

        # Environment variable overrides config file (but only if set)
        env_key = os.environ.get("ANTHROPIC_API_KEY", "")
        if env_key and not cfg.api_key:
            cfg.api_key = env_key

        return cfg

    def ensure_dirs(self):
        """Create data directories if they don't exist."""
        for subdir in ["domains", "runs", "convergences", "findings"]:
            (self.data_dir / subdir).mkdir(parents=True, exist_ok=True)


def _find_project_root() -> Path:
    """Find the project root directory.

    First checks relative to the package location (works for editable
    installs and running from source). Falls back to walking up from cwd.
    """
    # Try relative to this file — works for `pip install -e .`
    pkg_root = Path(__file__).resolve().parent.parent
    if (pkg_root / "taxonomy").is_dir():
        return pkg_root

    # Fall back to walking up from cwd
    current = Path.cwd()
    for parent in [current, *current.parents]:
        if (parent / "taxonomy").is_dir():
            return parent
        if (parent / "gnosis").is_dir() and (parent / "docs").is_dir():
            return parent
    return current
