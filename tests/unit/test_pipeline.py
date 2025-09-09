from __future__ import annotations
from pathlib import Path
import json
from src.pipeline import run_pipeline
from src.audit.loggers import LogManager
from src.utils.config_loader import load_config

def test_run_pipeline_smoke(tmp_path: Path, monkeypatch):
    # minimal cfg
    cfg = {
        "runtime":{"max_crawl_pages":1,"api_timeout_sec_max":5},
        "models":{"llm":{"provider":"auto","name":"gpt-5-mini","temperature":0.1},"embedding":{"provider":"auto","name":"gemini-embedding-001"}},
        "limits":{"bullets_per_role_max":6,"chars_per_bullet_max":220,"allow_long_bullets":True},
        "normalization":{"date_format":"YYYY-MM","location_format":"City, State/Province, Country"},
        "cover_letter":{"tone":"standard","word_min":300,"word_max":500,"mention_ls":[],"avoid_ls":[]},
        "relevance":{"authority_order":["recent_signed_resume","older_resumes"],"fuzzy":{"title_similarity_threshold":0.85}},
        "logging":{"redact_pii":True,"retention_days":90,"console_rich":True},
        "legal":{"notice_file": str(tmp_path / "legal.txt")},
        "output":{"dir_output": str(tmp_path / "out"), "dir_logs": str(tmp_path / "logs")}
    }
    Path(cfg["legal"]["notice_file"]).write_text("LN", encoding="utf-8")

    # create local input
    p = tmp_path / "resume.txt"
    p.write_text("Experience\n- Built pipelines\nSkills\nPython, ML", encoding="utf-8")

    # monkeypatch web fetcher (no network)
    from src.ingestion.web_fetcher import fetch_urls as real_fetch
    def fake_fetch(urls, max_pages=1, timeout=5):
        return [{"id":"url-1","source_type":"url","path_or_url":"https://example.org","raw_text":"Responsibilities: build ML systems","meta":{"mime":"text/html"},"timestamp":""}]
    import src.ingestion.web_fetcher as wf
    wf.fetch_urls = fake_fetch

    logger = LogManager(cfg).get_logger()
    from src.utils.io import now_ts, ensure_dirs
    ensure_dirs(cfg)
    ts = now_ts()
    res = run_pipeline(cfg, [p], ["https://example.org"], "Lead, AI", "lead_ai", ts, logger, dry_run=False)
    # outputs created
    out_files = list((tmp_path / "out").glob("*.json"))
    assert any("resume_" in f.name for f in out_files)
    assert any("cover-letter_" in f.name for f in out_files)
    assert res.approvals_json.startswith("[")
