from __future__ import annotations
from typing import List, Dict, Any

HEADERS = {
    "education": ["education", "academics"],
    "work": ["experience", "employment", "work history"],
    "skills": ["skills", "technical skills"],
    "projects": ["projects", "selected projects"],
    "awards": ["awards", "honors"],
    "profiles": ["profiles", "online", "links"],
    "languages": ["languages"],
    "references": ["references"],
    "JD_requirements": ["responsibilities", "requirements", "qualifications"],
    "JD_mission": ["mission", "about us", "our values"],
}

def classify_blocks(documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    blocks: List[Dict[str, Any]] = []
    for doc in documents:
        doc_id = doc.get("id", "")
        text = doc.get("raw_text", "") or ""
        parts = [p.strip() for p in text.split("\n\n") if p.strip()]
        for idx, part in enumerate(parts):
            lower = part.lower()
            section = "unknown"
            for sec, keys in HEADERS.items():
                if any(k in lower for k in keys):
                    section = sec
                    break
            blocks.append({
                "doc_id": doc_id,
                "section": section,
                "text": part,
                "provenance_id": f"{doc_id}#b{idx}"
            })
    return blocks
