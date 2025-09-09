#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import typer
from src.utils.config_loader import load_config
from src.utils.io import now_ts, ensure_dirs
from src.audit.loggers import LogManager
from src.pipeline import run_pipeline, extract_only, tailor_only, export_approvals as export_approvals_fn

app = typer.Typer(add_completion=False, no_args_is_help=True)

@app.command()
def run(
    # NOTE: list types tell Typer/Click to accept the option multiple times.
    # Usage: -i file1 -i file2   and   -u https://a -u https://b
    inputs: list[Path] = typer.Option([], "--inputs", "-i", help="Local files: txt/pdf/docx/md"),
    urls: list[str] = typer.Option([], "--urls", "-u", help="Public URLs to fetch"),
    job_title: str = typer.Option("", help="Job title"),
    job_slug: str = typer.Option("", help="Job slug"),
    config: Path = typer.Option(Path("config.yaml")),
    deterministic: bool = typer.Option(False, help="Force deterministic run"),
    dry_run: bool = typer.Option(False, help="Do everything but write outputs"),
    max_pages: int | None = typer.Option(None, help="Limit pages to crawl"),
    export_approvals: Path | None = typer.Option(None, help="Write APPROVAL docket here"),
):
    # ---- Build overrides without duplicate keys ----
    overrides: dict = {}
    if deterministic:
        overrides = {"runtime": {"deterministic": True}}
    if max_pages is not None:
        overrides = {
            **overrides,
            "runtime": {
                **overrides.get("runtime", {}),
                "max_crawl_pages": max_pages,
            },
        }

    cfg = load_config(config, overrides=overrides if overrides else None)
    ensure_dirs(cfg)
    logger = LogManager(cfg).get_logger()
    ts = now_ts()

    # Typer/Click pattern: repeat flags to accumulate values.
    # Convenience: also allow comma-separated fallback (e.g., --inputs a,b)
    if len(inputs) == 1 and isinstance(inputs[0], Path) and "," in str(inputs[0]):
        inputs = [Path(s) for s in str(inputs[0]).split(",") if s.strip()]

    if len(urls) == 1 and isinstance(urls[0], str) and "," in urls[0]:
        urls = [u.strip() for u in urls[0].split(",") if u.strip()]

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
