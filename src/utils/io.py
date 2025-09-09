from __future__ import annotations
from pathlib import Path
from datetime import datetime, timezone

def now_ts() -> str:
    return datetime.now(timezone.utc).astimezone().strftime("%Y%m%d_%H%M%S")

def ensure_dirs(cfg: dict) -> None:
    Path(cfg["output"]["dir_output"]).mkdir(parents=True, exist_ok=True)
    Path(cfg["output"]["dir_logs"]).mkdir(parents=True, exist_ok=True)
