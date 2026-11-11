"""Phase 3, composition.

Fills the card from the run folder and writes ``card.json``. Rows that can be computed or
quoted from the skill's files are filled here without a model. Every other row holds
"not examined" until a later step fills it from the collected sources or with a model.

Text from the skill's files is data. It is quoted and is never followed as an instruction.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

import yaml

from skillcard import EMPTY_WORDS, SCHEMA, SECTIONS, __version__, read_json, write_json

NOT_EXAMINED = "not examined"


def empty_card() -> dict:
    """Return a card in which every row holds "not examined".

    This is the one place that fixes the shape of a card as data.
    """
    return {
        "schema": SCHEMA,
        "skill": NOT_EXAMINED,
        "version": NOT_EXAMINED,
        "what_it_does": {
            "name": NOT_EXAMINED,
            "summary": NOT_EXAMINED,
            "tasks": NOT_EXAMINED,
            "author_description": NOT_EXAMINED,
            "outputs": NOT_EXAMINED,
            "sample_output": NOT_EXAMINED,
            "inputs": NOT_EXAMINED,
            "when_input_is_missing": NOT_EXAMINED,
            "exclusions": NOT_EXAMINED,
            "adoption": NOT_EXAMINED,
        },
        "what_it_needs": {
            "compatibility": NOT_EXAMINED,
            "software_dependencies": NOT_EXAMINED,
            "credentials": NOT_EXAMINED,
            "cost": {
                "context_tokens": {
                    "discovery": NOT_EXAMINED,
                    "load": NOT_EXAMINED,
                    "on_demand": NOT_EXAMINED,
                },
                "run_tokens": NOT_EXAMINED,
                "services": NOT_EXAMINED,
            },
        },
        "what_it_touches": {
            "side_effects": NOT_EXAMINED,
            "network_access": NOT_EXAMINED,
            "tools_and_permissions": NOT_EXAMINED,
            "machine_access": NOT_EXAMINED,
        },
        "what_is_known": {
            "checks": NOT_EXAMINED,
            "vulnerabilities": NOT_EXAMINED,
            "risks": NOT_EXAMINED,
            "limitations": NOT_EXAMINED,
            "known_problems": NOT_EXAMINED,
            "evaluations": NOT_EXAMINED,
        },
        "who_stands_behind_it": {
            "authorship": NOT_EXAMINED,
            "license": {
                "frontmatter": NOT_EXAMINED,
                "registry": NOT_EXAMINED,
                "repository": NOT_EXAMINED,
            },
            "maintenance": NOT_EXAMINED,
        },
        "which_files": {
            "version": {
                "hash": NOT_EXAMINED,
                "author_version": NOT_EXAMINED,
                "registry_version": NOT_EXAMINED,
                "commit": NOT_EXAMINED,
            },
            "source": NOT_EXAMINED,
            "files": NOT_EXAMINED,
            "composition": NOT_EXAMINED,
        },
        "about_this_card": {},
    }


def read_frontmatter(skill_md: Path) -> dict:
    """Return the frontmatter of a SKILL.md as a dictionary, empty when there is none.

    The loader builds only text, lists and dictionaries. Scalars stay text as the author
    wrote them, so a version such as 1.10 is not read as a number.
    """
    lines = skill_md.read_text(encoding="utf-8-sig", errors="replace").splitlines()
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


def estimate_tokens(size_in_bytes: int) -> int:
    """Estimate tokens at four bytes per token, the rule of schema v1.2."""
    return (size_in_bytes + 2) // 4


def count_empty(value: object) -> int:
    """Count the fields and slots that hold one of the four empty words."""
    if isinstance(value, dict):
        return sum(count_empty(item) for item in value.values())
    if isinstance(value, list):
        return sum(count_empty(item) for item in value)
    return int(isinstance(value, str) and value in EMPTY_WORDS)


def compose(run_dir: Path) -> dict:
    """Fill the card for the skill frozen in ``run_dir`` and write ``card.json``."""
    snapshot = read_json(run_dir / "snapshot.json")
    skill_md = run_dir / "files" / "SKILL.md"
    frontmatter = read_frontmatter(skill_md)
    metadata = frontmatter.get("metadata")
    metadata = metadata if isinstance(metadata, dict) else {}

    # The folder name stands in when the frontmatter has no name.
    name = quoted(frontmatter.get("name"), empty=snapshot["skill"])
    description = quoted(frontmatter.get("description"))
    version = quoted(frontmatter.get("version"), empty=quoted(metadata.get("version")))
    discovery_bytes = len(description.encode("utf-8")) if description != "not declared" else 0

    card = empty_card()
    card["skill"] = name
    card["version"] = version
    card["what_it_does"]["name"] = name
    card["what_it_does"]["author_description"] = description
    card["what_it_needs"]["cost"]["context_tokens"].update(
        discovery=estimate_tokens(discovery_bytes),
        load=estimate_tokens(skill_md.stat().st_size),
    )
    card["who_stands_behind_it"]["license"]["frontmatter"] = quoted(frontmatter.get("license"))
    card["which_files"]["version"].update(
        hash=snapshot["hash"],
        author_version=version,
        commit="none",
    )
    card["which_files"]["source"] = snapshot["source"]
    card["which_files"]["files"] = snapshot["files"]
    card["about_this_card"] = {
        "schema": SCHEMA,
        "date": date.today().isoformat(),
        "by": f"skillcard {__version__}",
        "skill_run": False,
        "scripts_analysed": False,
        "security_check_run": False,
        "external_service_contacted": False,
        "registry_read": False,
        "empty_values": sum(count_empty(card[section]) for section in SECTIONS),
    }
    write_json(run_dir / "card.json", card)
    return card
