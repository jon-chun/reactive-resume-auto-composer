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

def fetch_urls(urls: list[str], max_pages: int = 5, timeout: int = 60) -> list[dict]:
    """
    Best-effort public fetch: returns zero or more 'Document' dicts.
    - Never raises on HTTP errors (4xx/5xx) or network issues.
    - Skips failing URLs and continues.
    """
    try:
        import httpx
    except Exception:
        return []

    out: list[dict] = []
    try:
        with httpx.Client(timeout=timeout, follow_redirects=True) as client:
            for u in urls[: max(0, int(max_pages))]:
                try:
                    r = client.get(u)
                    # don't raise; just skip non-OK
                    if r.status_code >= 400:
                        continue
                    mime = r.headers.get("content-type", "text/html")
                    html = r.text or ""
                    text = readable_text(html)
                    out.append({
                        "id": f"url-{len(out)+1}",
                        "source_type": "url",
                        "path_or_url": u,
                        "raw_text": text,
                        "meta": {"mime": mime},
                        "timestamp": "",
                    })
                except Exception:
                    # swallow network/parse errors per-URL
                    continue
    except Exception:
        # global client errors: return what we have
        return out
    return out

