from __future__ import annotations
from typing import List, Dict, Any
import re
from .schemas import Element

EMAIL_RE = re.compile(r"[A-Za-z0-9_.+-]+@[A-Za-z0-9_.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"\b(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})\b")
URL_RE = re.compile(r"https?://\S+")

def _confidence(base: float = 0.7) -> float:
    return base

def extract_elements(blocks: List[Dict[str, Any]]) -> List[Element]:
    out: List[Element] = []
    for b in blocks:
        sec = b["section"]
        text = b["text"]
        prov = [b["provenance_id"]]
        if sec == "skills":
            kws = [t.strip() for t in re.split(r"[,\n]", text) if t.strip()]
            if kws:
                out.append(Element(id=f"elem-{len(out)+1}", type="skills", fields={"name":"Skills","keywords":kws}, confidence=_confidence(0.8), provenance_ids=prov, source_authority="unknown"))
        elif sec == "profiles":
            profs = []
            for url in URL_RE.findall(text):
                network = "LinkedIn" if "linkedin" in url.lower() else ("GitHub" if "github" in url.lower() else "Website")
                profs.append({"network": network, "url": url})
            if profs:
                out.append(Element(id=f"elem-{len(out)+1}", type="profiles", fields={"profiles":profs}, confidence=_confidence(0.6), provenance_ids=prov, source_authority="unknown"))
        elif sec == "education":
            # very light heuristic
            m_inst = re.search(r"(University|College|Institute|School)[^\n]*", text, re.I)
            inst = m_inst.group(0).strip() if m_inst else "Unknown Institution"
            out.append(Element(id=f"elem-{len(out)+1}", type="education", fields={"institution":inst, "degree":"", "area":"", "startDate":"", "endDate":""}, confidence=_confidence(0.6), provenance_ids=prov, source_authority="unknown"))
        elif sec == "work":
            # split into simple lines as highlights
            lines = [ln.strip("-• ").strip() for ln in text.splitlines() if ln.strip()]
            if lines:
                out.append(Element(id=f"elem-{len(out)+1}", type="work", fields={"company":"", "position":"", "highlights":lines[1:]}, confidence=_confidence(0.6), provenance_ids=prov, source_authority="unknown"))
        elif sec == "unknown":
            # basics: scan for email/phone
            basics = {}
            email = EMAIL_RE.search(text)
            phone = PHONE_RE.search(text)
            url = URL_RE.search(text)
            if email: basics["email"] = email.group(0)
            if phone: basics["phone"] = phone.group(0)
            if url: basics["website"] = url.group(0)
            if basics:
                out.append(Element(id=f"elem-{len(out)+1}", type="basics", fields=basics, confidence=_confidence(0.5), provenance_ids=prov, source_authority="unknown"))
    return out
