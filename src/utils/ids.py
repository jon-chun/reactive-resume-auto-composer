from __future__ import annotations
import hashlib, time, os

def sha1(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8")).hexdigest()

def new_run_id() -> str:
    return f"run-{int(time.time())}-{os.getpid()}"
