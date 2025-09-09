from __future__ import annotations
from pathlib import Path
from typing import Any, List, Dict
from .ingestion.file_loader import load_files
from .ingestion import web_fetcher as wf
from .extraction.classifier import classify_blocks
from .extraction.extractor import extract_elements
from .normalization.normalize import normalize_elements
from .merge.deduplicate import deduplicate
from .scoring.relevance import score_items
from .compose.resume_builder import to_reactive_resume, write_outputs
from .compose.cover_letter import render_cover_letter
from .utils.io import write_json

class Result:
    def __init__(self, approvals_json: str = "[]"):
        self.approvals_json = approvals_json

def _gather_jd_text(docs: List[Dict[str, Any]]) -> str:
    # naive: concatenate all URL documents
    return "\n\n".join([d.get("raw_text","") for d in docs if d.get("source_type") == "url"])

def run_pipeline(cfg: dict, inputs: List[Path], urls: List[str], job_title: str, job_slug: str, ts: str, log, dry_run: bool) -> Result:
    log.info("start:ingestion")
    local_docs = list(load_files(inputs))
    web_docs = wf.fetch_urls(urls, cfg["runtime"].get("max_crawl_pages",5), cfg["runtime"].get("api_timeout_sec_max",60))
    docs = local_docs + web_docs
    log.info(f"ingested_docs:{len(docs)}")
    # classify & extract
    blocks = classify_blocks(docs)
    elements_models = extract_elements(blocks)
    # convert Pydantic models to dicts
    elements = [e.model_dump() for e in elements_models]
    # normalize
    elements_norm_models = normalize_elements(elements_models, cfg)
    elements_norm = [e.model_dump() for e in elements_norm_models]
    # deduplicate
    merged, approvals = deduplicate(elements_norm, cfg)
    # scoring (if any JD text)
    jd_text = _gather_jd_text(web_docs)
    if jd_text.strip():
        merged = score_items(merged, jd_text, cfg, mentions=cfg.get("cover_letter",{}).get("mention_ls",[]), avoids=cfg.get("cover_letter",{}).get("avoid_ls",[]))
    # compose outputs
    legal_notice = ""
    ln_path = Path(cfg["legal"]["notice_file"])
    if ln_path.exists():
        legal_notice = ln_path.read_text(encoding="utf-8")
    master = to_reactive_resume(merged, legal_notice=legal_notice)
    if not dry_run:
        # master/tailored are same in v1 (ordering already by score)
        resume_path = write_outputs(master, cfg["output"]["dir_output"], ts)
        # cover letter JSON (stubbed body)
        cl_ctx = {
            "job": {"slug": job_slug, "title": job_title, "org": "", "url": ""},
            "tone": cfg["cover_letter"]["tone"],
            "word_limits": {"min": cfg["cover_letter"]["word_min"], "max": cfg["cover_letter"]["word_max"]},
            "mentions": cfg["cover_letter"]["mention_ls"],
            "avoid": cfg["cover_letter"]["avoid_ls"],
            "body": "TODO: generated letter",
        }
        write_json(Path(cfg["output"]["dir_output"]) / f"cover-letter_{ts}.json", cl_ctx)
        # audit & diff (minimal)
        write_json(Path(cfg["output"]["dir_output"]) / f"audit_{ts}.json", {"approvals_count": len(approvals)})
        write_json(Path(cfg["output"]["dir_output"]) / f"diff_{job_slug}.json", {"added": [], "removed": []})
    # approvals JSON
    import json as _json
    return Result(approvals_json=_json.dumps(approvals, ensure_ascii=False))

def extract_only(cfg: dict, inputs: List[Path], urls: List[str]) -> None:
    docs = list(load_files(inputs)) + wf.fetch_urls(urls, cfg["runtime"].get("max_crawl_pages",5), cfg["runtime"].get("api_timeout_sec_max",60))
    blocks = classify_blocks(docs)
    elements = extract_elements(blocks)
    # write preview to output for debugging
    from .utils.io import write_json, now_ts
    ts = now_ts()
    write_json(Path(cfg["output"]["dir_output"]) / f"elements_{ts}.json", [e.model_dump() for e in elements])

def tailor_only(cfg: dict, job_title: str, job_slug: str) -> None:
    # For v1, just log intention; full tailoring requires persisted master
    pass

def export_approvals(out_path: Path, result: Result | None) -> None:
    data = result.approvals_json if result else "[]"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(data, encoding="utf-8")
