from __future__ import annotations
from pathlib import Path
from typing import Any, Dict, Iterable

import yaml

REQUIRED_TOP_LEVEL_KEYS: tuple[str, ...] = (
    "runtime",
    "models",
    "limits",
    "normalization",
    "cover_letter",
    "relevance",
    "logging",
    "legal",
    "output",
)

def deep_merge(a: Dict[str, Any], b: Dict[str, Any]) -> Dict[str, Any]:
    """
    Recursively merge dict b into dict a, returning a NEW dict.
    For overlapping keys:
      - if both values are dicts, merge recursively
      - else, b overwrites a
    """
    out: Dict[str, Any] = dict(a)  # shallow copy
    for k, v in b.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_merge(out[k], v)  # type: ignore[arg-type]
        else:
            out[k] = v
    return out

def _validate_config(cfg: Dict[str, Any]) -> None:
    if not isinstance(cfg, dict):
        raise ValueError("Configuration root must be a mapping (YAML dict).")
    missing = [k for k in REQUIRED_TOP_LEVEL_KEYS if k not in cfg]
    if missing:
        raise ValueError(
            "Missing required top-level config keys: "
            + ", ".join(sorted(missing))
        )

def load_config(path: Path, overrides: dict | None = None) -> dict:
    """
    Load YAML config from `path`, deep-merge `overrides`, and validate schema.
    Returns a plain dict. Performs no external I/O beyond reading `path`.
    """
    if not isinstance(path, Path):
        path = Path(path)
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Config file not found: {path}") from e

    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML in config: {path}") from e

    if data is None:
        data = {}

    if not isinstance(data, dict):
        raise ValueError("Config root must be a mapping (YAML dict).")

    cfg = data
    if overrides:
        if not isinstance(overrides, dict):
            raise ValueError("overrides must be a dict if provided.")
        cfg = deep_merge(cfg, overrides)

    _validate_config(cfg)
    return cfg
