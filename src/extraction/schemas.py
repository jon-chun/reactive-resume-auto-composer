from __future__ import annotations
from typing import List, Dict, Any
from pydantic import BaseModel

class Element(BaseModel):
    id: str
    type: str
    fields: Dict[str, Any]
    confidence: float = 0.0
    provenance_ids: List[str] = []
    source_authority: str = "unknown"
    extracted_at: str = ""

class Approval(BaseModel):
    type: str = "APPROVAL"
    group_id: str
    element_type: str
    alternatives: List[Dict[str, Any]]
    chosen: int | None = None
    rationale: str | None = None
    provenance_ids: List[str] = []
    timestamp: str
