# Reactive Resume Auto-Composer

Reactive Resume Auto Composer: Create customized resumes, cover letters and emails tailored to your experiences and a particular job. A CLI tool to ingest resumes, JDs, and related sources, then compose a Reactive Resume JSON and evidence-linked cover letter.

## Quickstart

```bash
python3.11 -m venv .venv && source .venv/bin/activate
pip install -U pip
pip install -e ".[web,pdf,docx,llm,dev]"
python resume-cv-create.py --help
```

See `config.yaml` for runtime knobs. Outputs go to `./output`, logs to `./logs`.