from __future__ import annotations
from pathlib import Path
from datetime import datetime, timezone
import json

def now_ts() -> str:
    # local timezone formatting; readable and sortable
    return datetime.now(timezone.utc).astimezone().strftime("%Y%m%d_%H%M%S")

def ensure_dirs(cfg: dict) -> None:
    Path(cfg["output"]["dir_output"]).mkdir(parents=True, exist_ok=True)
    Path(cfg["output"]["dir_logs"]).mkdir(parents=True, exist_ok=True)

def write_json(path: Path, data: dict | list) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return path

def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")
