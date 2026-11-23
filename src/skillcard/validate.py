"""Phase 4, validation.

Checks the card against the frozen files and writes ``validation.json``. No phase changes
the card after this one, so the card that was checked is the card that ships.

The checks here look at the form of the card and need no model. They do not check whether
what a field says is true. A check of that kind is added as one more function that returns
an entry of the same form, and it reports into the same file.
"""

from __future__ import annotations

import functools
import math
from pathlib import Path

from skillcard import EMPTY_WORDS, SCHEMA, SECTIONS, read_json, read_template, write_json
from skillcard.identify import content_hash, list_files


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


@functools.cache
def _card_form() -> dict | None:
    try:
        return read_template()["card"]
    except (OSError, ValueError, KeyError):
        return None


def card_checks(card: dict) -> list[dict]:
    """Checks that need only the card, so they also run on a card that is already committed."""
    which = card.get("which_files")
    which = which if isinstance(which, dict) else {}
    listed = which.get("files")
    listed = listed if isinstance(listed, list) else []
    version = which.get("version")
    stated_hash = version.get("hash") if isinstance(version, dict) else None
    try:
        recomputed_hash = content_hash(listed)
    except (KeyError, TypeError, AttributeError, UnicodeError):
        recomputed_hash = None
    missing = [section for section in SECTIONS if not isinstance(card.get(section), dict)]
    blanks = blank_values(card)
    form = _card_form()
    shape = ["the card template was not found"] if form is None else shape_problems(card, form)
    return [
        {
            "check": "the card names the schema it follows",
            "passed": card.get("schema") == SCHEMA,
            "detail": [] if card.get("schema") == SCHEMA else [str(card.get("schema"))],
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


def validate(run_dir: Path) -> dict:
    """Check the card in ``run_dir`` and write the result to ``validation.json``."""
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
            "passed": len(listed) == len(frozen) and view(listed) == view(frozen),
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
