from __future__ import annotations
import json
from pathlib import Path
import logging
from src.utils.config_loader import load_config
from src.audit.loggers import LogManager

def test_logger_creates_file_and_redacts(tmp_path: Path, monkeypatch):
    # minimal config for logs
    cfg = {
        "output": {"dir_output": str(tmp_path / "out"), "dir_logs": str(tmp_path / "logs")},
        "logging": {"redact_pii": True}
    }
    logger = LogManager(cfg).get_logger()
    logger.info("Contact me at jane.doe@example.com or 555-123-4567")
    # ensure file exists and contains redacted content
    files = list((tmp_path / "logs").glob("log_*.json"))
    assert files, "log file should be created"
    content = files[0].read_text(encoding="utf-8").splitlines()
    # last line should be JSON with redacted msg
    last = json.loads(content[-1])
    assert "***@***.***" in last["msg"]
    assert "***-***-****" in last["msg"]

def test_logger_idempotent_handlers(tmp_path: Path):
    cfg = {"output": {"dir_output": str(tmp_path / "out"), "dir_logs": str(tmp_path / "logs")}, "logging": {"redact_pii": False}}
    lm1 = LogManager(cfg).get_logger()
    h1 = len(lm1.handlers)
    lm2 = LogManager(cfg).get_logger()
    h2 = len(lm2.handlers)
    assert h1 == h2  # no duplicate handlers
