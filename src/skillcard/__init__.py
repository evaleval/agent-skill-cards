"""Generate Skill Cards, documentation cards for agent skills."""

from __future__ import annotations

import json
from pathlib import Path

import yaml

__version__ = "0.1.0.dev0"

SCHEMA = "Skill Card v1.3"
SUPPORTED_SCHEMAS = ("Skill Card v1.2", SCHEMA)

# The name of the rule that turns the files of a skill into one hash. A hash is only compared
# with a hash made by the same rule. The rule itself is described in identify.py.
HASH_SCHEME = "skill-tree-v2"

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
#   none          nothing of this kind exists
#   not declared  the sources that were read do not say
#   not examined  nobody looked
#   unknown       the sources cannot answer
EMPTY_WORDS = ("none", "not declared", "not examined", "unknown")


def read_json(path: Path) -> dict:
    """Read one record of a run folder."""
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: object) -> None:
    """Write one record of a run folder as indented JSON."""
    text = json.dumps(data, indent=2, ensure_ascii=False, allow_nan=False)
    path.write_text(text + "\n", encoding="utf-8")


def schema_dir() -> Path:
    """Return the ``schema/`` folder of this checkout, with the card template and the guides."""
    folder = Path(__file__).resolve().parents[2] / "schema"
    if not (folder / "card-template.json").is_file():
        raise FileNotFoundError(
            "the schema folder was not found, the pipeline runs from a checkout of the repository"
        )
    return folder


def read_template() -> dict:
    """Read the card template, the one place that writes down the shape of ``card.json``."""
    return read_json(schema_dir() / "card-template.json")


def read_frontmatter(text: str) -> dict:
    """Return the frontmatter of a SKILL.md as a dictionary, empty when there is none.

    The loader builds only text, lists and dictionaries. Scalars stay text as the author
    wrote them, so a version such as 1.10 is not read as a number.
    """
    lines = text.lstrip("﻿").splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    end = next((i for i, line in enumerate(lines[1:], 1) if line.strip() == "---"), None)
    if end is None:
        return {}
    try:
        data = yaml.load("\n".join(lines[1:end]), Loader=yaml.BaseLoader)
    except (yaml.YAMLError, RecursionError):
        return {}
    return data if isinstance(data, dict) else {}


def quoted(value: object, empty: str = "not declared") -> str:
    """Return a frontmatter value as the author wrote it, or the empty word when it is absent."""
    return value.strip() if isinstance(value, str) and value.strip() else empty
