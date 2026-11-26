"""Phase 4, validation.

Checks the card against the frozen files and writes ``validation.json``. No phase changes
the card after this one, so the card that was checked is the card that ships.

The checks here look at the form of the card and need no model. They do not check whether
what a field says is true. A check of that kind is added as one more function that returns
an entry of the same form, and it reports into the same file.
"""

from __future__ import annotations

import copy
import functools
import math
import re
import unicodedata
from pathlib import Path

from skillcard import (
    EMPTY_WORDS,
    SCHEMA,
    SECTIONS,
    SUPPORTED_SCHEMAS,
    read_json,
    read_template,
    write_json,
)
from skillcard.identify import content_hash, list_files
from skillcard.index import card_content_record, compatible_content
from skillcard.source_only import source_only_form


def blank_values(value: object, where: str = "card") -> list[str]:
    """Return the places on the card that hold nothing where an empty word belongs."""
    if isinstance(value, dict) and value:
        return [
            place for key, item in value.items() for place in blank_values(item, f"{where}.{key}")
        ]
    if isinstance(value, list) and value:
        return [
            place for i, item in enumerate(value) for place in blank_values(item, f"{where}[{i}]")
        ]
    if isinstance(value, str):
        return [] if value.strip() else [where]
    if isinstance(value, float) and not math.isfinite(value):
        return [where]  # not a number, which JSON cannot hold
    return [where] if value is None or value in ([], {}) else []


def shape_problems(value: object, form: object, where: str = "card") -> list[str]:
    """Return the places where a card departs from the shape the template writes down.

    A group keeps exactly the keys of the template. A list holds items in one of the forms
    the template shows, or one of the four empty words stands in its place. Every other slot
    holds a single value.
    """
    if isinstance(form, dict):
        if not isinstance(value, dict):
            return [f"{where}: a group is expected"]
        problems = [f"{where}.{key}: missing" for key in form if key not in value]
        problems += [f"{where}.{key}: not in the template" for key in value if key not in form]
        for key, inner in form.items():
            if key in value:
                problems += shape_problems(value[key], inner, f"{where}.{key}")
        return problems
    if isinstance(form, list):
        if isinstance(value, str) and value in EMPTY_WORDS:
            return []
        if not isinstance(value, list):
            return [f"{where}: a list or an empty word is expected"]
        problems = []
        for i, item in enumerate(value):
            # An item follows one of the forms. The closest one is reported.
            problems += min((shape_problems(item, one, f"{where}[{i}]") for one in form), key=len)
        return problems
    return [f"{where}: a single value is expected"] if isinstance(value, (dict, list)) else []


def plain_text_problems(value: object, where: str = "card") -> list[str]:
    """Return fields that violate the card's one-line plain-text rule."""
    if isinstance(value, dict):
        return [
            problem
            for key, item in value.items()
            for problem in plain_text_problems(item, f"{where}.{key}")
        ]
    if isinstance(value, list):
        return [
            problem
            for index, item in enumerate(value)
            for problem in plain_text_problems(item, f"{where}[{index}]")
        ]
    if not isinstance(value, str):
        return []

    reasons = []
    if any(unicodedata.category(character) in {"Cc", "Cf", "Cs"} for character in value):
        reasons.append("control character")
    if re.search(r"(?m)^\s{0,3}#{1,6}(?:\s|$)", value):
        reasons.append("Markdown heading")
    if re.search(r"\[[^\]\r\n]+\]\([^\r\n)]*\)", value):
        reasons.append("Markdown link")
    if re.search(r"</?\s*[A-Za-z][^<>]*>", value):
        reasons.append("HTML tag")
    return [f"{where}: contains {reason}" for reason in reasons]


@functools.cache
def _card_form() -> dict | None:
    try:
        return read_template()["card"]
    except (OSError, ValueError, KeyError):
        return None


def card_checks(card: dict) -> list[dict]:
    """Checks that need only the card, so they also run on a card that is already committed."""
    card = copy.deepcopy(card)
    which = card.get("which_files")
    if isinstance(which, dict):
        version = which.get("version")
        files = which.get("files")
        if isinstance(version, dict):
            version.setdefault("hash_scheme", "skill-tree-v1")
            if "exclusions" not in version:
                version["exclusions"] = (
                    [
                        {
                            "path": item.get("path", ""),
                            "reason": "legacy exclusion reason not recorded",
                            "sha256": item.get("sha256", "none"),
                        }
                        for item in files
                        if isinstance(item, dict) and not item.get("in_hash", True)
                    ]
                    if isinstance(files, list)
                    else "none"
                )
                if version["exclusions"] == []:
                    version["exclusions"] = "none"
        if isinstance(files, list):
            for item in files:
                if isinstance(item, dict):
                    item.setdefault("file_type", "regular")
                    item.setdefault(
                        "exclusion_reason",
                        (
                            "none"
                            if item.get("in_hash", True)
                            else "legacy exclusion reason not recorded"
                        ),
                    )
    which = card.get("which_files")
    which = which if isinstance(which, dict) else {}
    listed = which.get("files")
    listed = listed if isinstance(listed, list) else []
    version = which.get("version")
    stated_hash = version.get("hash") if isinstance(version, dict) else None
    scheme = (
        version.get("hash_scheme", "skill-tree-v1")
        if isinstance(version, dict)
        else "skill-tree-v1"
    )
    try:
        recomputed_hash = content_hash(listed, scheme)
    except (KeyError, TypeError, AttributeError, UnicodeError, ValueError):
        recomputed_hash = None
    missing = [section for section in SECTIONS if not isinstance(card.get(section), dict)]
    blanks = blank_values(card)
    form = _card_form()
    shape = ["the card template was not found"] if form is None else shape_problems(card, form)
    plain_text = plain_text_problems(card) if card.get("schema") == SCHEMA else []
    return [
        {
            "check": "the card names the schema it follows",
            "passed": card.get("schema") in SUPPORTED_SCHEMAS,
            "detail": [] if card.get("schema") in SUPPORTED_SCHEMAS else [str(card.get("schema"))],
        },
        {
            "check": "the card has the seven sections of the schema",
            "passed": not missing,
            "detail": missing,
        },
        {
            "check": "the card has the slots of the template",
            "passed": not shape,
            "detail": shape,
        },
        {
            "check": "card values are single-line plain text",
            "passed": not plain_text,
            "detail": plain_text,
        },
        {
            "check": "the content hash matches the file list",
            "passed": recomputed_hash is not None and recomputed_hash == stated_hash,
            "detail": [],
        },
        {
            "check": "no value is blank",
            "passed": not blanks,
            "detail": blanks,
        },
    ]


def evidence_check(run_dir: Path) -> dict:
    """Check that every file ``evidence.json`` names as a source exists in the run folder."""
    try:
        evidence = read_json(run_dir / "evidence.json")
    except (OSError, ValueError):
        evidence = None
    root = run_dir.resolve()

    def exists(path: object) -> bool:
        """Say whether ``path`` names a file inside the run folder. Any other text does not."""
        if not isinstance(path, str) or not path:
            return False
        try:
            target = (root / path).resolve()
            return target.is_relative_to(root) and target.is_file()
        except (OSError, ValueError):
            return False

    if not isinstance(evidence, list):
        missing = ["evidence.json is missing or cannot be read"]
    else:
        missing = []
        for one in evidence:
            paths = one.get("from") if isinstance(one, dict) else None
            for path in paths if isinstance(paths, list) else [None]:
                if not exists(path):
                    field = one.get("field") if isinstance(one, dict) else one
                    missing.append(f"{field}: {str(path)[:200]!r}")
    return {
        "check": "every source that evidence.json names exists in the run folder",
        "passed": not missing,
        "detail": missing,
    }


def _validate_source_only(run_dir: Path, snapshot: dict) -> dict:
    """Check a source-specific supplement and its link to an existing content card."""
    supplement = read_json(run_dir / "source-card.json")
    template = read_template()
    shape = shape_problems(supplement.get("sections"), source_only_form(template["card"]))
    blanks = blank_values(supplement.get("sections"))
    plain_text = plain_text_problems(supplement)
    expected_reference = snapshot.get("known", {}).get("reuse_card")
    reference = supplement.get("content_card")
    compatible = False
    if isinstance(reference, str) and reference == expected_reference:
        target = (run_dir.parent / reference).resolve()
        try:
            compatible = target.is_file() and compatible_content(
                snapshot, card_content_record(read_json(target))
            )
        except (OSError, ValueError, KeyError, TypeError, AttributeError):
            compatible = False
    checks = [
        {
            "check": "the source supplement names the current schema",
            "passed": supplement.get("schema") == SCHEMA,
            "detail": [] if supplement.get("schema") == SCHEMA else [str(supplement.get("schema"))],
        },
        {
            "check": "the source supplement has only the source-specific template fields",
            "passed": not shape,
            "detail": shape,
        },
        {
            "check": "the source supplement references a compatible content card",
            "passed": compatible,
            "detail": [] if compatible else [str(reference)],
        },
        {
            "check": "the source supplement records the current source",
            "passed": (
                supplement.get("source") == snapshot.get("source")
                and supplement.get("source_identity") == snapshot.get("source_identity")
            ),
            "detail": [],
        },
        {
            "check": "no source-specific value is blank",
            "passed": not blanks,
            "detail": blanks,
        },
        {
            "check": "source-specific values are single-line plain text",
            "passed": not plain_text,
            "detail": plain_text,
        },
        evidence_check(run_dir),
    ]
    result = {"passed": all(check["passed"] for check in checks), "checks": checks}
    write_json(run_dir / "validation.json", result)
    return result


def validate(run_dir: Path) -> dict:
    """Check the card in ``run_dir`` and write the result to ``validation.json``."""
    snapshot = read_json(run_dir / "snapshot.json")
    if snapshot.get("known", {}).get("action") == "SOURCE_ONLY":
        return _validate_source_only(run_dir, snapshot)
    card = read_json(run_dir / "card.json")
    which = card.get("which_files")
    which = which if isinstance(which, dict) else {}
    listed = which.get("files")
    listed = listed if isinstance(listed, list) else []
    frozen, _ = list_files(run_dir / "files")

    def view(files: list) -> set[tuple]:
        return {
            (item.get("path"), item.get("bytes"), item.get("sha256"))
            for item in files
            if isinstance(item, dict)
        }

    checks = card_checks(card)
    checks.insert(
        3,
        {
            "check": "the file list matches the frozen files",
            "passed": (
                len([one for one in listed if one.get("file_type", "regular") == "regular"])
                == len(frozen)
                and view([one for one in listed if one.get("file_type", "regular") == "regular"])
                == view(frozen)
            ),
            "detail": [],
        },
    )
    checks.insert(
        4,
        {
            "check": "the card identity metadata matches the snapshot",
            "passed": compatible_content(snapshot, card_content_record(card)),
            "detail": [],
        },
    )
    checks.append(evidence_check(run_dir))
    result = {"passed": all(check["passed"] for check in checks), "checks": checks}
    write_json(run_dir / "validation.json", result)
    return result


def main(argv: list[str] | None = None) -> int:
    """Check committed cards (``card.json`` files), or run this phase on run folders."""
    import sys

    paths = [Path(arg) for arg in (sys.argv[1:] if argv is None else argv)]
    failed = 0
    for path in paths:
        try:
            checks = validate(path)["checks"] if path.is_dir() else card_checks(read_json(path))
        except (OSError, ValueError) as error:
            print(f"FAIL {path}: {error}")
            failed += 1
            continue
        bad = [check for check in checks if not check["passed"]]
        failed += bool(bad)
        print(f"{'FAIL' if bad else 'ok  '} {path}")
        for check in bad:
            print(f"     {check['check']}: {check['detail']}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
