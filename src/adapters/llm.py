from __future__ import annotations
from typing import Optional

class LLMClient:
    def __init__(self, cfg: dict):
        self.cfg = cfg
        self.provider = (cfg.get("models",{}).get("llm",{}).get("provider") or "auto").lower()

    def complete(self, system: str, user: str, temperature: Optional[float] = None) -> str:
        # Deterministic offline mock: produce a simple transformation
        t = temperature if temperature is not None else self.cfg.get("models",{}).get("llm",{}).get("temperature", 0.1)
        # Echo key markers to simulate structured output
        return f"[MOCK-LMM|temp={t}] {system[:40]} :: {user[:80]}"
