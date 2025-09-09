from __future__ import annotations
from pathlib import Path
from typing import Dict, Any
import hashlib

def _doc(id_hint: str, text: str, meta: dict) -> Dict[str, Any]:
    return {
        "id": id_hint,
        "source_type": "file",
        "path_or_url": meta.get("path"),
        "raw_text": text,
        "meta": meta,
        "timestamp": ""
    }

def parse_txt(path: Path) -> Dict[str, Any]:
    txt = path.read_text(encoding="utf-8", errors="ignore")
    return _doc(f"doc-{hashlib.sha1(str(path).encode()).hexdigest()[:8]}", txt, {"mime": "text/plain", "path": str(path)})

def parse_md(path: Path) -> Dict[str, Any]:
    md = path.read_text(encoding="utf-8", errors="ignore")
    return _doc(f"doc-{hashlib.sha1(str(path).encode()).hexdigest()[:8]}", md, {"mime": "text/markdown", "path": str(path)})

def parse_docx(path: Path) -> Dict[str, Any]:
    try:
        import docx  # type: ignore
        d = docx.Document(str(path))
        txt = "\n".join([p.text for p in d.paragraphs])
    except Exception:
        txt = ""
    return _doc(f"doc-{hashlib.sha1(str(path).encode()).hexdigest()[:8]}", txt, {"mime": "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "path": str(path)})

def parse_pdf(path: Path) -> Dict[str, Any]:
    # minimal text extraction to avoid heavy deps by default
    try:
        import pdfminer.high_level as pdfminer  # type: ignore
        txt = pdfminer.extract_text(str(path)) or ""
    except Exception:
        txt = ""
    return _doc(f"doc-{hashlib.sha1(str(path).encode()).hexdigest()[:8]}", txt, {"mime": "application/pdf", "path": str(path)})
