from __future__ import annotations
from src.compose.cover_letter import render_cover_letter
from pathlib import Path

def test_cover_letter_render(tmp_path: Path):
    context = {
        "job": {"slug":"ai_support","title":"Lead, AI Support Program","org":"Example","url":"https://example.org"},
        "tone": "standard",
        "word_limits": {"min": 300, "max": 500},
        "mentions": ["lab","center"],
        "avoid": ["buzzword"],
        "body": "This is a body."
    }
    tpl_dir = str((Path(__file__).resolve().parents[2] / "templates" / "cover_letter"))
    out = render_cover_letter(context, tpl_dir)
    assert "Lead, AI Support Program" in out
    assert "This is a body." in out
