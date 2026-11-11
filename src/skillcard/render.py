"""Renders ``card.json`` as Markdown and writes ``card.md``.

This is the plain rendering, one list per section. It reads the card and never changes it.
The slots of a list item are separated by a middle dot, as in the examples of the schema.

Text that comes from the skill is shown as text. The characters that would start HTML, a
link or an image are escaped.
"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

from skillcard import SECTIONS, read_json


def _text(value: object) -> str:
    """Return a value as one line of plain text."""
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, dict):
        return " · ".join(_text(item) for item in value.values())
    if isinstance(value, list):
        return ", ".join(_text(item) for item in value)
    text = " ".join(str(value).split())
    return text.replace("&", "&amp;").replace("<", "&lt;").replace("[", "\\[")


def _label(key: str) -> str:
    return _text(key.replace("_", " ").capitalize())


def _lines(value: object, depth: int = 0) -> Iterator[str]:
    """Yield the Markdown list lines for one section, group or list of items."""
    pad = "  " * depth
    if isinstance(value, dict):
        for key, item in value.items():
            if isinstance(item, (dict, list)) and item:
                yield f"{pad}- **{_label(key)}**"
                yield from _lines(item, depth + 1)
            else:
                yield f"{pad}- **{_label(key)}** {_text(item)}"
    elif isinstance(value, list):
        for item in value:
            yield f"{pad}- {_text(item)}"


def render(run_dir: Path) -> str:
    """Write ``card.md`` next to ``card.json`` and return its text."""
    card = read_json(run_dir / "card.json")
    lines = [f"# Skill Card for {_text(card.get('skill', 'unknown'))}", ""]
    for section, title in SECTIONS.items():
        lines += [f"## {title}", "", *_lines(card.get(section, {})), ""]
    text = "\n".join(lines).rstrip() + "\n"
    (run_dir / "card.md").write_text(text, encoding="utf-8")
    return text
