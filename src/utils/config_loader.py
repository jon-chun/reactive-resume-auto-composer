from __future__ import annotations
from pathlib import Path
import yaml
from typing import Any, Dict

def deep_merge(a: Dict[str, Any], b: Dict[str, Any]) -> Dict[str, Any]:
    out = dict(a)
    for k, v in b.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = v
    return out

def load_config(path: Path, overrides: dict | None = None) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if overrides:
        data = deep_merge(data, overrides)
    return data
