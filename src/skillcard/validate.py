"""Phase 4, validation.

Checks the card against the frozen files and writes ``validation.json``. No phase changes
the card after this one, so the card that was checked is the card that ships.

The checks here need no model. Checks that need a model or a person are added as further
tiers and report into the same file.
"""

from __future__ import annotations

from pathlib import Path

from skillcard import SCHEMA, SECTIONS, read_json, write_json
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
    return [where] if value is None or value in ("", [], {}) else []


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
        2,
        {
            "check": "the file list matches the frozen files",
            "passed": len(listed) == len(frozen) and view(listed) == view(frozen),
            "detail": [],
        },
    )
    result = {"passed": all(check["passed"] for check in checks), "checks": checks}
    write_json(run_dir / "validation.json", result)
    return result


def main(argv: list[str] | None = None) -> int:
    """Check committed cards (``card.json`` files) without a run folder."""
    import sys

    paths = [Path(arg) for arg in (sys.argv[1:] if argv is None else argv)]
    failed = 0
    for path in paths:
        try:
            checks = card_checks(read_json(path))
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
