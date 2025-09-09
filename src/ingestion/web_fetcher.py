from __future__ import annotations
from typing import List, Dict, Any
import time
try:
    import httpx
except Exception:
    httpx = None

def readable_text(html: str) -> str:
    # TODO: implement readability/trafilatura extraction
    return html

def fetch_urls(urls: list[str], max_pages: int = 5, timeout: int = 60) -> List[Dict[str, Any]]:
    if not urls:
        return []
    out = []
    if httpx is None:
        return out  # httpx not installed; skip
    with httpx.Client(timeout=timeout, follow_redirects=True) as client:
        for u in urls[:max_pages]:
            r = client.get(u)
            r.raise_for_status()
            out.append({
                "id": f"url-{len(out)+1}",
                "source_type": "url",
                "path_or_url": u,
                "raw_text": readable_text(r.text),
                "meta": {"mime": r.headers.get("content-type","text/html")},
                "timestamp": ""
            })
            time.sleep(0.3)
    return out
