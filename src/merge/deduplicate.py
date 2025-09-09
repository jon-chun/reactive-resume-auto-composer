from __future__ import annotations
from typing import List, Dict, Any
try:
    from rapidfuzz import fuzz
except Exception:
    fuzz = None

def is_same_item(a: Dict[str, Any], b: Dict[str, Any], threshold: float = 0.85) -> bool:
    if fuzz is None:
        return False
    title_sim = fuzz.token_set_ratio(a.get("title",""), b.get("title","")) / 100.0
    return title_sim >= threshold

def cluster(elements: List[Dict[str, Any]], cfg: dict) -> List[list[Dict[str, Any]]]:
    clusters: List[list[Dict[str, Any]]] = []
    for e in elements:
        placed = False
        for c in clusters:
            if is_same_item(e, c[0], cfg["relevance"]["fuzzy"]["title_similarity_threshold"]):
                c.append(e); placed = True; break
        if not placed:
            clusters.append([e])
    return clusters
