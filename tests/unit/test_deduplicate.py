from __future__ import annotations
from src.merge.deduplicate import deduplicate

def test_deduplicate_clusters_and_approvals():
    e1 = {"id":"e1","type":"work","fields":{"company":"Acme","position":"PI","highlights":["Did X"]},"confidence":0.9,"provenance_ids":["doc#b1"],"source_authority":"recent_signed_resume"}
    e2 = {"id":"e2","type":"work","fields":{"company":"ACME Inc.","position":"Principal Investigator","highlights":["Did Y"]},"confidence":0.7,"provenance_ids":["doc#b2"],"source_authority":"older_resumes"}
    cfg = {"relevance":{"fuzzy":{"title_similarity_threshold":0.5},"authority_order":["recent_signed_resume","older_resumes"]}, "limits":{"bullets_per_role_max":5}}
    merged, approvals = deduplicate([e1,e2], cfg)
    assert len(merged) == 1
    assert merged[0]["fields"]["highlights"]
    assert approvals and approvals[0]["type"] == "APPROVAL"
