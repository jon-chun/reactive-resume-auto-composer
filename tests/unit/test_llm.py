from __future__ import annotations
from src.adapters.llm import LLMClient

def test_llm_offline_deterministic():
    cfg = {"models":{"llm":{"provider":"auto","temperature":0.1}}}
    llm = LLMClient(cfg)
    out1 = llm.complete("SYS","USER")
    out2 = llm.complete("SYS","USER")
    assert out1 == out2
    out3 = llm.complete("SYS","USER", temperature=0.5)
    assert "temp=0.5" in out3
