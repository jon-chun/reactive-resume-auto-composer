from __future__ import annotations
from pathlib import Path
from typing import Iterator, Dict, Any
from .parsers import parse_txt, parse_md, parse_docx, parse_pdf

def load_files(paths: list[Path]) -> Iterator[Dict[str, Any]]:
    for p in paths:
        ext = p.suffix.lower()
        if ext == ".txt":
            yield parse_txt(p)
        elif ext == ".md":
            yield parse_md(p)
        elif ext == ".docx":
            yield parse_docx(p)
        elif ext == ".pdf":
            yield parse_pdf(p)
        else:
            continue
