"""Generate Skill Cards, documentation cards for agent skills."""

from __future__ import annotations

import json
from pathlib import Path

__version__ = "0.1.0.dev0"

SCHEMA = "Skill Card v1.2"

# The sections of a card in the order of the schema, with the titles the schema gives them.
SECTIONS = {
    "what_it_does": "Overview",
    "what_it_needs": "Requirements",
    "what_it_touches": "Permissions",
    "what_is_known": "Checks and Evaluations",
    "who_stands_behind_it": "Ownership",
    "which_files": "Version",
    "about_this_card": "About this card",
}

# A field or slot that holds nothing carries one of these words and is never left blank.
EMPTY_WORDS = ("none", "not declared", "not examined", "unknown")


def read_json(path: Path) -> dict:
    """Read one record of a run folder."""
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: object) -> None:
    """Write one record of a run folder as indented JSON."""
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
