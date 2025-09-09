from __future__ import annotations
from jinja2 import Environment, FileSystemLoader
from pathlib import Path

def render_cover_letter(context: dict, templates_dir: str) -> str:
    env = Environment(loader=FileSystemLoader(templates_dir), autoescape=False, trim_blocks=True, lstrip_blocks=True)
    tmpl = env.get_template("default.j2")
    return tmpl.render(**context)
