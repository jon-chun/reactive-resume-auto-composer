from __future__ import annotations
from pathlib import Path
import pytest
import yaml

from src.utils.config_loader import load_config, deep_merge, REQUIRED_TOP_LEVEL_KEYS

def _minimal_config_dict() -> dict:
    return {
        "runtime": {"timezone": "America/New_York", "deterministic": True, "seed": 42, "api_timeout_sec_max": 60, "max_crawl_pages": 5},
        "models": {
            "llm": {"provider": "auto", "name": "gpt-5-mini", "temperature": 0.1, "topp": 1.0, "topk": 0},
            "embedding": {"provider": "auto", "name": "gemini-embedding-001"},
        },
        "limits": {"bullets_per_role_max": 6, "chars_per_bullet_max": 220, "allow_long_bullets": True},
        "normalization": {"date_format": "YYYY-MM", "location_format": "City, State/Province, Country"},
        "cover_letter": {"tone": "standard", "word_min": 300, "word_max": 500, "mention_ls": [], "avoid_ls": []},
        "relevance": {
            "authority_order": [
                "custom_instructions",
                "recent_signed_resume",
                "official_institutional_orcid_scholar",
                "personal_site",
                "github",
                "older_resumes",
                "news_media",
            ],
            "fuzzy": {"title_similarity_threshold": 0.85},
        },
        "logging": {"redact_pii": True, "retention_days": 90, "console_rich": True},
        "legal": {"notice_file": "./docs/legal_notice.txt"},
        "output": {"dir_output": "./output", "dir_logs": "./logs"},
    }

def test_deep_merge_basic():
    a = {"a": {"b": 1, "c": 2}, "x": 1}
    b = {"a": {"b": 99}, "y": 2}
    merged = deep_merge(a, b)
    # original untouched
    assert a["a"]["b"] == 1
    # merged has overrides and preserved keys
    assert merged["a"]["b"] == 99
    assert merged["a"]["c"] == 2
    assert merged["x"] == 1
    assert merged["y"] == 2

def test_load_config_happy_path(tmp_path: Path):
    cfg_path = tmp_path / "config.yaml"
    base_cfg = _minimal_config_dict()
    cfg_path.write_text(yaml.safe_dump(base_cfg), encoding="utf-8")

    overrides = {"relevance": {"fuzzy": {"title_similarity_threshold": 0.9}}}
    cfg = load_config(cfg_path, overrides=overrides)

    # required keys present
    for key in REQUIRED_TOP_LEVEL_KEYS:
        assert key in cfg

    # deep-merge applied
    assert cfg["relevance"]["fuzzy"]["title_similarity_threshold"] == 0.9
    # unchanged leaf remains
    assert cfg["limits"]["bullets_per_role_max"] == 6

def test_missing_key_triggers_value_error(tmp_path: Path):
    cfg_path = tmp_path / "config.yaml"
    base_cfg = _minimal_config_dict()
    # Remove one required key
    base_cfg.pop("legal")
    cfg_path.write_text(yaml.safe_dump(base_cfg), encoding="utf-8")

    with pytest.raises(ValueError) as ei:
        load_config(cfg_path)

    assert "Missing required top-level config keys" in str(ei.value)
    assert "legal" in str(ei.value)
