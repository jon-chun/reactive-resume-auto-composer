from __future__ import annotations
from pathlib import Path
from src.ingestion.file_loader import load_files

def test_load_files(tmp_path: Path):
    (tmp_path/"a.txt").write_text("t", encoding="utf-8")
    (tmp_path/"b.md").write_text("m", encoding="utf-8")
    (tmp_path/"c.xyz").write_text("x", encoding="utf-8")  # ignored
    docs = list(load_files([tmp_path/"a.txt", tmp_path/"b.md", tmp_path/"c.xyz"]))
    assert len(docs) == 2
    ids = {d["id"] for d in docs}
    assert len(ids) == 2
