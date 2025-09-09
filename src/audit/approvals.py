from __future__ import annotations
import json
from pathlib import Path

def export_approvals(out_path: Path, approvals: list[dict] | None = None) -> None:
    data = approvals or []
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
