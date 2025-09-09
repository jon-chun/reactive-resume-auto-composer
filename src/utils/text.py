from __future__ import annotations
import re

ACTION_VERBS = ["Led", "Built", "Designed", "Created", "Drove", "Launched", "Improved", "Reduced", "Optimized"]

def clean_text(s: str) -> str:
    s = re.sub(r"\s+", " ", s)
    return s.strip()

def to_present_tense(bullet: str) -> str:
    return bullet  # TODO: implement tense conversion

def to_past_tense(bullet: str) -> str:
    return bullet  # TODO: implement tense conversion
