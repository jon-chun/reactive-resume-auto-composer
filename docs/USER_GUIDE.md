# Reactive Resume Auto-Composer — User Guide

Welcome! This guide walks you through installing, configuring, and running the CLI to build a Reactive Resume JSON and an evidence-linked cover letter.

---

## 1. Installation

```bash
python3.11 -m venv .venv && source .venv/bin/activate
pip install -U pip
pip install -e ".[web,pdf,docx,llm,dev]"
```

> Optional extras:
> - `web`: fetch public URLs (JD/org pages)
> - `pdf`: parse text-based PDFs
> - `docx`: parse Word documents
> - `dev`: lint/test tooling for local development

---

## 2. Inputs

Supported local files (v1): **.txt, .md, .docx, .pdf (text-based)**.  
Web inputs: **public URLs** to job postings and org/personnel pages.

Sample inputs: `data/samples/*`

---

## 3. Configuration

Edit `config.yaml` (key sections):

- `runtime`: timeouts, deterministic mode.
- `models`: LLM/embedding adapters (`auto` is deterministic, offline-friendly).
- `limits`: bullet caps and lengths.
- `normalization`: date & location formats.
- `cover_letter`: tone and word limits; `mention_ls` and `avoid_ls`.
- `relevance`: authority order & fuzzy thresholds.
- `logging`: PII redaction and retention.
- `legal`: path to legal notice injected into outputs.
- `output`: directories for outputs and logs.

To temporarily override values (at runtime) you can pass overrides programmatically via the pipeline (e.g., from the CLI flags in a future enhancement).

---

## 4. Quick Start

```bash
# From repo root
python resume-cv-create.py run   --inputs ./data/samples/resume_sample.txt ./data/samples/academic_profile.md   --urls https://example.org/job   --job-title "Lead, AI Support Program"   --job-slug ai_support_program   --config ./config.yaml   --deterministic
```

Outputs in `./output`:
- `resume_{timestamp}.json`
- `cover-letter_{timestamp}.json`
- `audit_{timestamp}.json`
- `diff_{job_slug}.json`

Logs in `./logs/log_{timestamp}.json`.

---

## 5. Deterministic Runs

Use `--deterministic` or set `runtime.deterministic: true` in `config.yaml`.  
This pins seeds and uses offline, mock adapters so results are reproducible.

---

## 6. Tailoring & Overrides

- The tool computes semantic similarity between JD pages and extracted resume items using a deterministic hash embedding (offline).
- You can **boost** certain terms via `cover_letter.mention_ls` and **penalize** via `cover_letter.avoid_ls`.

---

## 7. Troubleshooting

- **No text from PDF**: v1 skips scanned PDFs (no OCR). Convert to text-based PDF or .docx.
- **No web output**: ensure `web` extra installed; network blocked tests will still pass due to monkeypatching.
- **PII in logs**: enable `logging.redact_pii: true`.

---

## 8. FAQ

**Q: Can I use actual APIs for LLMs/embeddings?**  
A: Architecture supports this; v1 ships with deterministic offline adapters. Wire real providers in `src/adapters/*`.

**Q: How do I review conflicts?**  
A: See `audit_{timestamp}.json` and grep for `"type": "APPROVAL"` in logs; v1 also supports exporting via CLI in future iterations.

