from __future__ import annotations
from src.extraction.extractor import extract_elements

def test_extractor_from_blocks():
    blocks = [
        {"section":"skills","text":"Python, ML, NLP","provenance_id":"doc#b0"},
        {"section":"profiles","text":"https://github.com/jon https://www.linkedin.com/in/jon","provenance_id":"doc#b1"},
        {"section":"education","text":"Education\nKenyon College","provenance_id":"doc#b2"},
        {"section":"work","text":"Experience\n- Built models\n- Shipped things","provenance_id":"doc#b3"},
        {"section":"unknown","text":"Contact: me@example.com, (555) 111-2222","provenance_id":"doc#b4"},
    ]
    elems = extract_elements(blocks)
    types = [e.type for e in elems]
    assert {"skills","profiles","education","work","basics"}.issubset(set(types))
