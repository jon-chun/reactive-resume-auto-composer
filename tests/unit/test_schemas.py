from __future__ import annotations
from src.extraction.schemas import Element, Approval

def test_element_model_defaults():
    e = Element(id="e1", type="work", fields={"company":"Acme"})
    assert e.confidence == 0.0
    assert e.source_authority == "unknown"

def test_approval_model():
    a = Approval(group_id="g1", element_type="work", alternatives=[{"candidate":{"company":"Acme"}, "confidence":0.9, "source":"resume"}], chosen=0, rationale="better", timestamp="2025-01-01T00:00:00Z")
    assert a.type == "APPROVAL"
    assert a.chosen == 0
