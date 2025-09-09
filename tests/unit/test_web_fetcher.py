from __future__ import annotations
from pathlib import Path
import types
import sys

def test_fetch_urls_monkeypatch(monkeypatch):
    from src.ingestion.web_fetcher import fetch_urls

    class FakeResp:
        def __init__(self, text, headers=None):
            self.text = text
            self.headers = headers or {"content-type": "text/html"}
        def raise_for_status(self): pass

    class FakeClient:
        def __init__(self, timeout=None, follow_redirects=True): pass
        def __enter__(self): return self
        def __exit__(self, *a): pass
        def get(self, u):
            return FakeResp("<html><body><h1>JD Page</h1></body></html>")

    fake_httpx = types.SimpleNamespace(Client=FakeClient)
    monkeypatch.setitem(sys.modules, "httpx", fake_httpx)

    docs = fetch_urls(["https://example.com/a", "https://example.com/b"], max_pages=1, timeout=5)
    assert len(docs) == 1
    assert docs[0]["source_type"] == "url"
    assert "html" in docs[0]["meta"]["mime"]
