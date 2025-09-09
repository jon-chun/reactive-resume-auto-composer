from __future__ import annotations
from pathlib import Path
import pytest
from src.ingestion.parsers import parse_txt, parse_md, parse_docx, parse_pdf

def test_parse_txt(tmp_path: Path):
    p = tmp_path / "a.txt"
    p.write_text("hello", encoding="utf-8")
    d = parse_txt(p)
    assert d["raw_text"] == "hello"
    assert d["meta"]["mime"] == "text/plain"

def test_parse_md(tmp_path: Path):
    p = tmp_path / "a.md"
    p.write_text("# title\n\ncontent", encoding="utf-8")
    d = parse_md(p)
    assert "content" in d["raw_text"]
    assert d["meta"]["mime"] == "text/markdown"

@pytest.mark.skipif(__import__("importlib").util.find_spec("docx") is None, reason="python-docx not installed")
def test_parse_docx(tmp_path: Path):
    import docx
    p = tmp_path / "a.docx"
    doc = docx.Document()
    doc.add_paragraph("docx text")
    doc.save(str(p))
    d = parse_docx(p)
    assert "docx text" in d["raw_text"]

@pytest.mark.skipif(__import__("importlib").util.find_spec("pdfminer") is None and __import__("importlib").util.find_spec("pdfminer.six") is None, reason="pdfminer not installed")
def test_parse_pdf(tmp_path: Path):
    # we can't generate a real PDF easily without deps; just call function and ensure it returns dict
    p = tmp_path / "a.pdf"
    p.write_bytes(b"%PDF-1.4\n%...")  # fake header
    d = parse_pdf(p)
    assert "meta" in d and d["meta"]["mime"] == "application/pdf"
