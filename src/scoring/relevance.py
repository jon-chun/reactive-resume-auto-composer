from __future__ import annotations
from typing import List, Dict, Any
from ..adapters.embeddings import EmbeddingClient, cosine

def _textify(el: Dict[str, Any]) -> str:
    f = el.get("fields", {})
    if el.get("type") == "work":
        return " ".join([f.get("company",""), f.get("position","")] + (f.get("highlights",[]) or []))
    if el.get("type") == "skills":
        return " ".join(f.get("keywords",[]))
    if el.get("type") == "education":
        return " ".join([f.get("institution",""), f.get("degree",""), f.get("area","")])
    return " ".join(str(v) for v in f.values())

def score_items(elements: List[Dict[str, Any]], jd_text: str, cfg: dict, mentions: List[str] | None = None, avoids: List[str] | None = None) -> List[Dict[str, Any]]:
    emb = EmbeddingClient(cfg)
    jd_vec = emb.embed_texts([jd_text])[0]
    out: List[Dict[str, Any]] = []
    for el in elements:
        vec = emb.embed_texts([_textify(el)])[0]
        s = cosine(jd_vec, vec)
        # boosts and penalties
        t = _textify(el).lower()
        if mentions:
            for m in mentions:
                if m.lower() in t:
                    s += 0.02
        if avoids:
            for a in avoids:
                if a.lower() in t:
                    s -= 0.02
        el2 = dict(el)
        el2["score"] = float(s)
        out.append(el2)
    return sorted(out, key=lambda e: e["score"], reverse=True)
