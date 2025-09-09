# Reactive Resume Auto-Composer

CLI tool to ingest resumes, JDs, and related sources, then compose a **Reactive Resume JSON** and an **evidence-linked cover letter**.  
Deterministic-first, offline-friendly by default; easily swap to real LLM/embedding providers later.

---

## ✨ Features
- Ingest **.txt / .md / .docx / .pdf (text-based only)** + **public URLs** (JD/org pages)
- Extract **REACTIVE_RESUME_ELEMENTS**, deduplicate with **APPROVAL** conflict dockets
- Normalize to **Reactive Resume JSON** (+ academic/industry extensions)
- Score relevance vs **Job Descriptions** (deterministic hash embeddings)
- Generate a structured **cover letter** JSON using Jinja2 templates
- Full **JSON logging** with **PII redaction**, audit artifacts, reproducible runs

---

## 🚀 Quick Start (with `uv`)
[`uv`](https://github.com/astral-sh/uv) is a fast Python package & virtualenv manager.

```bash
# 0) Install uv (one-time)
# macOS / Linux: 
curl -LsSf https://astral.sh/uv/install.sh | sh
# Windows (PowerShell):
# iwr https://astral.sh/uv/install.ps1 | iex

# 1) Clone and enter the repo
git clone <your-fork-url> reactive-resume-auto-composer
cd reactive-resume-auto-composer

# 2) Create & activate a virtualenv managed by uv
uv venv
source .venv/bin/activate  # (on Windows: .venv\Scripts\activate)

# 3) Install runtime + optional extras + dev tools
uv pip install -r requirements.txt
uv pip install -r requirements-dev.txt
# (optional) install the project in editable mode
uv pip install -e .

# 4) Try it with the included samples
python resume-cv-create.py run \
  --inputs ./data/samples/resume_sample.txt ./data/samples/academic_profile.md \
  --urls https://example.org/job \
  --job-title "Lead, AI Support Program" \
  --job-slug ai_support_program \
  --config ./config.yaml \
  --deterministic
```

**Outputs:** written to `./output/`  
- `resume_{timestamp}.json`  
- `cover-letter_{timestamp}.json`  
- `audit_{timestamp}.json`  
- `diff_{job_slug}.json`  

**Logs:** JSON lines in `./logs/log_{timestamp}.json`

---

## ⚙️ Configuration (`config.yaml`)
Key sections you may tune:

- `runtime`: timeouts, deterministic mode, crawl depth
- `models`: provider names for `llm` / `embedding` (v1 uses deterministic mocks)
- `limits`: bullets per role, char limits, allow long bullets
- `normalization`: date format (`YYYY-MM`), location formatting
- `cover_letter`: `tone`, word bounds, `mention_ls`, `avoid_ls`
- `relevance`: `authority_order` and fuzzy similarity threshold
- `logging`: `redact_pii`, retention
- `legal`: path to `docs/legal_notice.txt` injected into outputs
- `output`: `dir_output`, `dir_logs`

---

## 🧪 Testing
```bash
uv pip install -r requirements-dev.txt
pytest -q
```

CI: See `.github/workflows/ci.yml` for a GitHub Actions pipeline that installs via `uv`, lints, types, and tests.

---

## 🗂️ Project Layout
```
project-root/
  resume-cv-create.py           # Typer CLI
  config.yaml                   # Knobs & GLOBAL_VARs
  requirements.txt              # runtime deps (uv-friendly)
  requirements-dev.txt          # dev/test tooling
  pyproject.toml                # project metadata (PEP 621)
  data/samples/                 # sample inputs
  docs/
    USER_GUIDE.md
    PROGRAMMER_GUIDE.md
    legal_notice.txt
  src/
    adapters/                   # embeddings, LLM (deterministic mocks)
    ingestion/                  # parsers, loaders, web fetcher
    extraction/                 # schemas, classifier, extractor
    normalization/              # normalize dates/locations/bullets
    merge/                      # dedup + APPROVAL conflicts
    scoring/                    # JD relevance scoring
    compose/                    # resume JSON + cover letter
    audit/                      # logging + approvals export
    utils/                      # config loader, I/O helpers
  tests/
    unit/                       # per-module tests
  .github/workflows/ci.yml
```

---

## 🔧 Common Tasks

### Run end-to-end pipeline
```bash
python resume-cv-create.py run --inputs <files...> --urls <urls...> --job-title "..." --job-slug <slug> --config ./config.yaml --deterministic
```

### Extract-only (debug intermediate elements)
```bash
python resume-cv-create.py extract --inputs <files...> --urls <urls...> --config ./config.yaml
# Check ./output/elements_{timestamp}.json
```

### Tailor-only (future hook)
```bash
python resume-cv-create.py tailor --job-title "..." --job-slug <slug> --config ./config.yaml
```

---

## 🔍 Troubleshooting
- **Scanned PDFs**: Not supported in v1 (no OCR). Use text-based PDFs or convert to `.docx`/`.txt`.
- **No network in tests/CI**: Web fetch is monkeypatched in tests. For real runs, ensure `httpx` is installed (in `requirements.txt`).
- **PII in logs**: Set `logging.redact_pii: true` in `config.yaml`.

---

## 📚 More Docs
- [User Guide](./docs/USER_GUIDE.md) — click-by-click usage
- [Programmer Guide](./docs/PROGRAMMER_GUIDE.md) — architecture & extension points
