from __future__ import annotations
from pathlib import Path
import json
from typing import List, Dict, Any

def to_reactive_resume(master_elements: List[Dict[str, Any]], legal_notice: str) -> Dict[str, Any]:
    # TODO: map typed elements → Reactive Resume JSON
    return {
        "basics": {},
        "work": [],
        "education": [],
        "skills": [],
        "meta": {"legal_notice": legal_notice, "extensions": {}}
    }

def write_outputs(data: Dict[str, Any], out_dir: str, ts: str) -> Path:
    p = Path(out_dir)
    p.mkdir(parents=True, exist_ok=True)
    out = p / f"resume_{ts}.json"
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return out
