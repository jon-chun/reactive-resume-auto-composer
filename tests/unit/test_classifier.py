from __future__ import annotations
from src.extraction.classifier import classify_blocks

def test_classify_blocks_simple():
    docs = [{
        "id":"doc1",
        "raw_text":"Education\n\nKenyon College...\n\nExperience\n\nCompany X...\n\nSkills\n\nPython, ML"
    }]
    blocks = classify_blocks(docs)
    sects = {b["section"] for b in blocks}
    assert {"education","work","skills"}.issubset(sects)
    assert all("#b" in b["provenance_id"] for b in blocks)
