"""Command line entry point. Runs the four phases in order on one skill folder."""

from __future__ import annotations

import argparse
from pathlib import Path

from skillcard import read_json
from skillcard.collect import collect
from skillcard.compose import compose
from skillcard.identify import identify
from skillcard.render import render
from skillcard.validate import validate


def run(skill_dir: Path, out_dir: Path = Path("runs"), leave_out: tuple[str, ...] = ()) -> Path:
    """Generate the card for one skill folder and return the run folder.

    Each phase reads the run folder and adds its own output to it. A run can be inspected
    step by step, and a phase can be developed against the output of the phase before it.
    """
    run_dir = identify(skill_dir, out_dir, leave_out)
    collect(run_dir)
    compose(run_dir)
    validate(run_dir)
    render(run_dir)
    return run_dir


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="skillcard",
        description="Generate a Skill Card for one agent skill folder.",
    )
    parser.add_argument("skill", type=Path, help="the folder that holds the skill's SKILL.md")
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("runs"),
        help="the folder that run folders are written to (default: runs)",
    )
    parser.add_argument(
        "--leave-out",
        action="append",
        default=[],
        metavar="PATH",
        help="a document about the skill that is stored next to it, listed but not hashed "
        "(may be given more than once)",
    )
    args = parser.parse_args(argv)
    try:
        run_dir = run(args.skill, args.out, tuple(args.leave_out))
    except (ValueError, OSError) as error:
        parser.exit(2, f"skillcard: {error}\n")
    passed = read_json(run_dir / "validation.json")["passed"]
    print(run_dir / "card.md")
    print("validation passed" if passed else f"validation failed, see {run_dir}/validation.json")
    return 0 if passed else 1
