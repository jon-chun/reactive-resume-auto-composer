from __future__ import annotations
from pathlib import Path
from src.compose.resume_builder import to_reactive_resume, write_outputs

def test_resume_builder_schema_and_legal(tmp_path: Path):
    elems = [
        {"type":"basics","fields":{"email":"x@y.com"}},
        {"type":"profiles","fields":{"profiles":[{"network":"GitHub","url":"https://github.com/x"}]}, "provenance_ids":["doc1#b0"]},
        {"type":"work","fields":{"company":"Acme","position":"Eng","highlights":["Did X"]},"provenance_ids":["doc2#b1"]},
        {"type":"publications","fields":{"title":"Paper A"}},
    ]
    rr = to_reactive_resume(elems, legal_notice="LN")
    assert rr["basics"]["email"] == "x@y.com"
    assert rr["basics"]["profiles"][0]["network"] == "GitHub"
    assert rr["meta"]["legal_notice"] == "LN"
    assert "publications" in rr["meta"]["extensions"]
    out = write_outputs(rr, str(tmp_path), "20250101_010101")
    assert out.exists()
