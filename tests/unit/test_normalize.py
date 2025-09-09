from __future__ import annotations
from src.extraction.schemas import Element
from src.normalization.normalize import normalize_elements

def test_normalize_dates_and_bullets():
    elems = [
        Element(id="1", type="work", fields={"startDate":"2020-01","endDate":"Present","highlights":["A"*300]}, confidence=1.0),
        Element(id="2", type="education", fields={"startDate":"2018","endDate":"2020"}, confidence=1.0),
    ]
    cfg = {"limits":{"allow_long_bullets": False, "chars_per_bullet_max": 120}}
    out = normalize_elements(elems, cfg)
    assert out[0].fields["endDate"] == "Present"
    assert len(out[0].fields["highlights"][0]) <= 120
    assert out[1].fields["startDate"].startswith("2018")
