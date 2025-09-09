from __future__ import annotations
import json, sys, logging, re
from pathlib import Path
from datetime import datetime

EMAIL_RE = re.compile(r"([A-Za-z0-9_.+-]+)@([A-Za-z0-9_.-]+\.[A-Za-z]{2,})")
PHONE_RE = re.compile(r"\b(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})\b")

class PiiRedactor(logging.Filter):
    def __init__(self, enabled: bool):
        super().__init__()
        self.enabled = enabled

    def filter(self, record: logging.LogRecord) -> bool:
        if not self.enabled:
            return True
        msg = record.getMessage()
        msg = EMAIL_RE.sub("***@***.***", msg)
        msg = PHONE_RE.sub("***-***-****", msg)
        record.msg = msg
        return True

class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "ts": datetime.utcnow().isoformat()+"Z",
            "level": record.levelname,
            "msg": record.getMessage(),
            "name": record.name,
        }
        return json.dumps(payload, ensure_ascii=False)

class LogManager:
    _initialized = False

    def __init__(self, cfg: dict):
        self.cfg = cfg
        self.logger = logging.getLogger("rrac")
        self.logger.setLevel(logging.INFO)
        if not LogManager._initialized:
            # prevent duplicate handlers
            self.logger.handlers.clear()
            # Console
            ch = logging.StreamHandler(sys.stdout)
            ch.setFormatter(JsonFormatter())
            ch.addFilter(PiiRedactor(bool(self.cfg.get("logging", {}).get("redact_pii", False))))
            self.logger.addHandler(ch)
            # File
            log_dir = Path(self.cfg["output"]["dir_logs"]).resolve()
            log_dir.mkdir(parents=True, exist_ok=True)
            logfile = log_dir / f"log_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
            fh = logging.FileHandler(logfile, encoding="utf-8")
            fh.setFormatter(JsonFormatter())
            fh.addFilter(PiiRedactor(bool(self.cfg.get("logging", {}).get("redact_pii", False))))
            self.logger.addHandler(fh)
            LogManager._initialized = True

    def get_logger(self):
        return self.logger
