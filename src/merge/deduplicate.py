from __future__ import annotations
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
from datetime import datetime
try:
    from rapidfuzz import fuzz
except Exception:
    fuzz = None

def _title(e: Dict[str, Any]) -> str:
    # try common fields for title-ish comparison
    f = e.get("fields", {})
    return (f.get("position") or f.get("title") or "").lower()

def _company(e: Dict[str, Any]) -> str:
    return (e.get("fields", {}).get("company") or "").lower()

def _date_key(e: Dict[str, Any]) -> str:
    f = e.get("fields", {})
    return (f.get("endDate") or f.get("startDate") or "")

def is_same_item(a: Dict[str, Any], b: Dict[str, Any], threshold: float = 0.85) -> bool:
    if fuzz is None:
        return False
    t_sim = fuzz.token_set_ratio(_title(a), _title(b)) / 100.0
    c_sim = fuzz.token_set_ratio(_company(a), _company(b)) / 100.0
    return (t_sim >= threshold) or (c_sim >= threshold)

def cluster(elements: List[Dict[str, Any]], cfg: dict) -> List[list[Dict[str, Any]]]:
    clusters: List[list[Dict[str, Any]]] = []
    thr = cfg.get("relevance", {}).get("fuzzy", {}).get("title_similarity_threshold", 0.85)
    for e in elements:
        placed = False
        for c in clusters:
            if is_same_item(e, c[0], thr):
                c.append(e); placed = True; break
        if not placed:
            clusters.append([e])
    return clusters

def _authority_weight(src: str, order: list[str]) -> float:
    if src in order:
        # higher weight for earlier in the list
        idx = order.index(src)
        return max(0.1, 1.0 - idx * (0.9 / max(1, len(order)-1)))
    return 0.1

def merge_cluster(cluster: List[Dict[str, Any]], cfg: dict) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    approvals: List[Dict[str, Any]] = []
    if not cluster:
        return {}, approvals
    order = cfg.get("relevance", {}).get("authority_order", [])
    # choose best by composite score
    scored = []
    for e in cluster:
        w = _authority_weight(e.get("source_authority","unknown"), order) * 0.6
        conf = float(e.get("confidence", 0.0)) * 0.2
        rec = 0.2  # placeholder recency
        scored.append((w+conf+rec, e))
    scored.sort(key=lambda x: x[0], reverse=True)
    winner = scored[0][1].copy()
    # merge highlights conservatively
    highlights = []
    for _, e in scored:
        hs = e.get("fields", {}).get("highlights", [])
        if isinstance(hs, list):
            highlights.extend(h for h in hs if h not in highlights)
    if highlights:
        winner.setdefault("fields", {}).setdefault("highlights", highlights[: cfg.get("limits", {}).get("bullets_per_role_max", 6)])
    # create approval if there are conflicting companies/positions
    companies = {e.get("fields",{}).get("company") for _, e in scored if e.get("fields",{}).get("company")}
    positions = {e.get("fields",{}).get("position") for _, e in scored if e.get("fields",{}).get("position")}
    if len(companies) > 1 or len(positions) > 1:
        approvals.append({
            "type":"APPROVAL",
            "group_id": f"grp-{id(cluster)}",
            "element_type": winner.get("type"),
            "alternatives": [{"candidate": e.get("fields",{}), "confidence": float(e.get("confidence",0.0)), "source": e.get("source_authority","unknown")} for _, e in scored],
            "chosen": 0,
            "rationale": "Conflicting fields; chose highest composite",
            "provenance_ids": [pid for _, e in scored for pid in e.get("provenance_ids",[])],
            "timestamp": datetime.utcnow().isoformat()+"Z"
        })
    return winner, approvals

def deduplicate(elements: List[Dict[str, Any]], cfg: dict) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    merged: List[Dict[str, Any]] = []
    approvals: List[Dict[str, Any]] = []
    for cl in cluster(elements, cfg):
        w, ap = merge_cluster(cl, cfg)
        if w:
            merged.append(w)
        approvals.extend(ap)
    return merged, approvals
