from __future__ import annotations
import json, sys, logging
from pathlib import Path
from datetime import datetime

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
    def __init__(self, cfg: dict):
        self.cfg = cfg
        self.logger = logging.getLogger("rrac")
        self.logger.setLevel(logging.INFO)

        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(JsonFormatter())
        self.logger.addHandler(ch)

        log_dir = Path(self.cfg["output"]["dir_logs"]).resolve()
        log_dir.mkdir(parents=True, exist_ok=True)
        logfile = log_dir / f"log_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        fh = logging.FileHandler(logfile, encoding="utf-8")
        fh.setFormatter(JsonFormatter())
        self.logger.addHandler(fh)

    def get_logger(self):
        return self.logger
