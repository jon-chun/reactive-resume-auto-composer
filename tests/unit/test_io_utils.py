from __future__ import annotations
from pathlib import Path
import json
from src.utils.io import now_ts, ensure_dirs, write_json, read_text

def test_now_ts_format():
    ts = now_ts()
    assert len(ts) == 15  # YYYYMMDD_HHMMSS
    assert ts.isdigit() or (ts.replace("_","").isdigit())

def test_ensure_dirs(tmp_path: Path):
    cfg = {"output": {"dir_output": str(tmp_path / "out"), "dir_logs": str(tmp_path / "logs")}}
    ensure_dirs(cfg)
    assert (tmp_path / "out").exists()
    assert (tmp_path / "logs").exists()

def test_json_roundtrip(tmp_path: Path):
    p = tmp_path / "a" / "b" / "c.json"
    data = {"x": 1, "y": ["a", "b"]}
    write_json(p, data)
    s = read_text(p)
    assert json.loads(s) == data
