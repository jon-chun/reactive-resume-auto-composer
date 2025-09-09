from __future__ import annotations
from pathlib import Path
from typing import Any, List, Dict
from .ingestion.file_loader import load_files
from .ingestion.web_fetcher import fetch_urls
from .compose.resume_builder import to_reactive_resume, write_outputs
from .compose.cover_letter import render_cover_letter

class Result:
    def __init__(self):
        self.approvals_json = "[]"

def run_pipeline(cfg: dict, inputs: List[Path], urls: List[str], job_title: str, job_slug: str, ts: str, log, dry_run: bool) -> Result:
    log.info("start:ingestion")
    docs = list(load_files(inputs)) + fetch_urls(urls, cfg["runtime"]["max_crawl_pages"], cfg["runtime"]["api_timeout_sec_max"])
    log.info(f"ingested_docs:{len(docs)}")

    # TODO: normalize → classify → extract → deduplicate → normalize fields → score → compose
    rr = to_reactive_resume([], legal_notice=Path(cfg["legal"]["notice_file"]).read_text(encoding="utf-8") if Path(cfg["legal"]["notice_file"]).exists() else "")

    if not dry_run:
        write_outputs(rr, cfg["output"]["dir_output"], ts)
        # Minimal cover letter stub
        cl_ctx = {
            "job": {"slug": job_slug, "title": job_title, "org": "", "url": ""},
            "tone": cfg["cover_letter"]["tone"],
            "word_limits": {"min": cfg["cover_letter"]["word_min"], "max": cfg["cover_letter"]["word_max"]},
            "mentions": cfg["cover_letter"]["mention_ls"],
            "avoid": cfg["cover_letter"]["avoid_ls"],
            "body": "TODO: generated letter",
        }
        cl_path = Path(cfg["output"]["dir_output"]) / f"cover-letter_{ts}.json"
        import json
        cl_path.write_text(json.dumps(cl_ctx, ensure_ascii=False, indent=2), encoding="utf-8")

    res = Result()
    return res

def extract_only(cfg: dict, inputs: List[Path], urls: List[str]) -> None:
    # TODO: implement
    pass

def tailor_only(cfg: dict, job_title: str, job_slug: str) -> None:
    # TODO: implement
    pass

def export_approvals(out_path: Path, result: Result | None) -> None:
    data = result.approvals_json if result else "[]"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(data, encoding="utf-8")
