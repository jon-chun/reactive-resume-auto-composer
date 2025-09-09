#!/usr/bin/env python3
from __future__ import annotations
import typer
from pathlib import Path
from src.utils.config_loader import load_config
from src.utils.io import now_ts, ensure_dirs
from src.audit.loggers import LogManager
from src.pipeline import run_pipeline, extract_only, tailor_only, export_approvals as export_approvals_fn

app = typer.Typer(add_completion=False, no_args_is_help=True)

@app.command()
def run(
    inputs: list[Path] = typer.Option([], help="Local files: txt/pdf/docx/md"),
    urls: list[str] = typer.Option([], help="Public URLs to fetch"),
    job_title: str = typer.Option("", help="Job title"),
    job_slug: str = typer.Option("", help="Job slug"),
    config: Path = typer.Option(Path("config.yaml")),
    deterministic: bool = typer.Option(False, help="Force deterministic run"),
    dry_run: bool = typer.Option(False, help="Do everything but write outputs"),
    max_pages: int | None = typer.Option(None, help="Limit pages to crawl"),
    export_approvals: Path | None = typer.Option(None, help="Write APPROVAL docket here"),
):
    cfg = load_config(config, overrides={
        "runtime": {"deterministic": deterministic} if deterministic else {},
        "runtime": {"max_crawl_pages": max_pages} if max_pages is not None else {},
    })
    ensure_dirs(cfg)
    logger = LogManager(cfg).get_logger()
    ts = now_ts()
    result = run_pipeline(cfg, inputs, urls, job_title, job_slug, ts, logger, dry_run)
    if export_approvals and getattr(result, "approvals_json", None):
        export_approvals_fn(export_approvals, result)

@app.command()
def extract(
    inputs: list[Path] = typer.Option([]),
    urls: list[str] = typer.Option([]),
    config: Path = Path("config.yaml"),
):
    cfg = load_config(config)
    LogManager(cfg).get_logger()
    extract_only(cfg, inputs, urls)

@app.command()
def tailor(job_title: str, job_slug: str, config: Path = Path("config.yaml")):
    cfg = load_config(config)
    LogManager(cfg).get_logger()
    tailor_only(cfg, job_title, job_slug)

@app.command()
def approvals(out: Path = Path("./output/approvals.json")):
    export_approvals_fn(out, None)

if __name__ == "__main__":
    app()
