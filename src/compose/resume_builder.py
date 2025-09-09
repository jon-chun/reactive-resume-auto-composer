from __future__ import annotations
from pathlib import Path
import json
from typing import List, Dict, Any
from ..utils.io import write_json

def _collect_sources(elements: List[Dict[str, Any]]) -> list[str]:
    s = set()
    for e in elements:
        for pid in e.get("provenance_ids",[]) or []:
            s.add(pid.split("#")[0])
    return sorted(s)

def to_reactive_resume(master_elements: List[Dict[str, Any]], legal_notice: str) -> Dict[str, Any]:
    rr = {
        "basics": {},
        "work": [],
        "education": [],
        "skills": [],
        "languages": [],
        "awards": [],
        "projects": [],
        "interests": [],
        "references": [],
        "meta": {"legal_notice": legal_notice, "extensions": {}, "sources": _collect_sources(master_elements), "conflicts": []}
    }
    for e in master_elements:
        t = e.get("type")
        f = e.get("fields", {})
        if t == "basics":
            rr["basics"] = {**rr["basics"], **f}
        elif t == "profiles":
            rr.setdefault("basics", {}).setdefault("profiles", [])
            rr["basics"]["profiles"] = rr["basics"].get("profiles", []) + f.get("profiles", [])
        elif t in rr:
            rr[t].append(f)
        else:
            # extensions bucket heuristic
            rr["meta"]["extensions"].setdefault(t or "unknown", []).append(f)
    return rr

def write_outputs(data: Dict[str, Any], out_dir: str, ts: str) -> Path:
    p = Path(out_dir) / f"resume_{ts}.json"
    write_json(p, data)
    return p
