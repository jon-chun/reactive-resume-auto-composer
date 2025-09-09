from __future__ import annotations
from src.scoring.relevance import score_items

def test_relevance_scoring_with_mentions_and_avoids():
    elements = [
        {"type":"work","fields":{"company":"Acme","position":"ML Engineer","highlights":["Built ML pipelines"]}},
        {"type":"work","fields":{"company":"Acme","position":"Pianist","highlights":["Performed concerts"]}},
    ]
    jd = "We need a machine learning engineer with pipelines experience."
    scored = score_items(elements, jd, cfg={}, mentions=["pipelines"], avoids=["concerts"])
    assert scored[0]["fields"]["position"] == "ML Engineer"
