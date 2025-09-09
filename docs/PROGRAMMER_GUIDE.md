# Reactive Resume Auto-Composer — Programmer Guide

This guide accelerates onboarding for engineers extending or debugging the system.

---

## 1. Architecture Overview

```
Ingestion (files+urls)
  ↓
Normalization (cleaning, sectioning)
  ↓
Classifier (block → section labels)
  ↓
Extractor (sections → structured Elements)
  ↓
Normalization (dates/locations/bullets)
  ↓
Deduplication & Conflict Resolution (clusters + APPROVALs)
  ↓
Relevance Scoring (JD similarity + boosts/penalties)
  ↓
Composer (Reactive Resume JSON + Cover Letter)
  ↓
Logging & Audit (JSON logs, audit doc, approvals JSON)
```

- **Deterministic-first:** Offline mocks for LLM/embeddings keep tests green.
- **Provenance:** `provenance_id="docX#bY"` per block → carried into elements → used for meta.sources.

---

## 2. Repo Layout

```
project-root/
  resume-cv-create.py        # Typer CLI
  config.yaml                # runtime knobs
  pyproject.toml
  data/samples/              # sample inputs
  docs/
    USER_GUIDE.md
    PROGRAMMER_GUIDE.md
    legal_notice.txt
  src/
    adapters/
      embeddings.py          # deterministic hash embeddings; cosine
      llm.py                 # deterministic mock LLM
    ingestion/
      parsers.py             # txt/md/docx/pdf parsers
      file_loader.py         # dispatch by extension
      web_fetcher.py         # httpx client (monkeypatchable in tests)
    extraction/
      schemas.py             # Pydantic Element, Approval
      classifier.py          # rule-first section tagging
      extractor.py           # heuristic element extraction
    normalization/
      normalize.py           # dates, bullets, location aliases
    merge/
      deduplicate.py         # clustering & APPROVALs
    scoring/
      relevance.py           # JD similarity and ordering
    compose/
      resume_builder.py      # map elements → Reactive Resume JSON
      cover_letter.py        # Jinja renderer
    audit/
      loggers.py             # JSON logger w/ PII redaction
      approvals.py           # export utility
    utils/
      config_loader.py       # deep-merge & validation
      io.py                  # ts, dir creation, json helpers
      ids.py                 # hashes, ids (hooks for future)
  tests/
    conftest.py
    unit/                    # per-module tests
.github/workflows/ci.yml     # CI
```

---

## 3. Data Models

- **Element (intermediate)**: `id, type, fields, confidence, provenance_ids, source_authority, extracted_at`
- **Approval**: conflict docket with alternatives and chosen index
- **Reactive Resume JSON**: assembled in `compose/resume_builder.py` with academic/industry extensions under `meta.extensions`.

---

## 4. Pipeline Walkthrough (`src/pipeline.py`)

1. **Ingest**: `file_loader.load_files` + `web_fetcher.fetch_urls`  
2. **Classify**: `classifier.classify_blocks`  
3. **Extract**: `extractor.extract_elements` → `Element[]`  
4. **Normalize**: `normalize_elements` (dates/locations/bullets)  
5. **Deduplicate**: `deduplicate` → merged elements + `APPROVAL`s  
6. **Score**: `score_items` using JD text from fetched URLs  
7. **Compose**: `to_reactive_resume` → write outputs; generate cover letter JSON stub  
8. **Audit**: Writes `audit_{ts}.json` with counts; logs every step in JSON

---

## 5. Adding Features

### 5.1 New Section Extractor
- Extend `extraction/classifier.py` with header keywords.
- Implement parsing in `extraction/extractor.py`.
- Add normalization in `normalization/normalize.py` if needed.
- Extend composer mapping in `compose/resume_builder.py` (or `meta.extensions`).

### 5.2 Real Embedding/LLM Providers
- Add client calls in `adapters/embeddings.py` or `adapters/llm.py`.
- Gate via `cfg["models"]["embedding"]["provider"]` / `cfg["models"]["llm"]["provider"]`.
- Keep deterministic fallback when providers unavailable.

### 5.3 Authority & Conflicts
- Tune list in `config.yaml.relevance.authority_order`.
- Enhance `merge/deduplicate.py` scoring and approval rationale.

### 5.4 Logging
- Use `LogManager(cfg).get_logger()`; messages are JSON and PII-redacted if enabled.

---

## 6. Testing & CI

- Run `pytest -q` locally.  
- CI runs `ruff`, `black --check`, `mypy` (non-blocking for now), and full tests with coverage.
- Mock network in tests by monkeypatching `web_fetcher`.

---

## 7. Debugging Tips

- Inspect `./logs/log_*.json` for pipeline steps and messages.
- Dump intermediate elements by calling `extract_only` and inspecting `output/elements_{ts}.json`.
- If clustering is off, print token_set_ratio scores within `deduplicate.py`.

---

## 8. Roadmap Hooks

- OCR, private connectors, Docker/GPU, real provider adapters, Scholar/ORCID integration, and a web UI for APPROVAL triage are planned; skeletons are ready for expansion.

