from __future__ import annotations
from typing import List
import re
from ..extraction.schemas import Element

CITY_ALIASES = {
    "nyc": "New York, NY, USA",
    "sf": "San Francisco, CA, USA",
}

DATE_RE = re.compile(r"\b(20\d{2}|19\d{2})(?:[-/](0[1-9]|1[0-2]))?\b", re.I)

def _norm_date(s: str) -> str:
    s = s.strip()
    if s.lower() in {"present","current","now"}:
        return "Present"
    m = DATE_RE.search(s)
    if not m:
        return ""
    year = m.group(1)
    month = m.group(2)
    return f"{year}-{month}" if month else year

def normalize_elements(elements: List[Element], cfg: dict) -> List[Element]:
    out: List[Element] = []
    allow_long = cfg.get("limits", {}).get("allow_long_bullets", True)
    max_chars = cfg.get("limits", {}).get("chars_per_bullet_max", 220)
    for e in elements:
        f = dict(e.fields)
        if e.type in {"work","education"}:
            for k in ("startDate","endDate"):
                if k in f and f[k]:
                    f[k] = _norm_date(str(f[k]))
        if e.type in {"work"} and "highlights" in f and isinstance(f["highlights"], list) and not allow_long:
            f["highlights"] = [h if len(h) <= max_chars else (h[:max_chars-3]+"...") for h in f["highlights"]]
        if e.type in {"work","education"} and "location" in f:
            loc = str(f["location"]).strip()
            key = loc.lower()
            if key in CITY_ALIASES:
                f["location"] = CITY_ALIASES[key]
        out.append(Element(id=e.id, type=e.type, fields=f, confidence=e.confidence, provenance_ids=e.provenance_ids, source_authority=e.source_authority, extracted_at=e.extracted_at))
    return out
