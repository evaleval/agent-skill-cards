"""Command line entry point. Runs the four phases in order on one skill."""

from __future__ import annotations

import argparse
from pathlib import Path

from skillcard import read_json
from skillcard.collect import collect, handed_over
from skillcard.compose import compose
from skillcard.identify import AlreadyKnown, identify, identify_repository
from skillcard.model import from_environment
from skillcard.render import render
from skillcard.validate import validate


def run(
    skill: Path | str,
    out_dir: Path = Path("runs"),
    leave_out: tuple[str, ...] = (),
    *,
    path: str | None = None,
    commit: str | None = None,
    cards_dir: Path | None = None,
    again: bool = False,
    offline: bool = False,
    reports: tuple[Path, ...] = (),
    model=None,
    fetch=None,
) -> Path:
    """Generate the card for one skill and return the run folder.

    ``skill`` is a folder on this machine, or a repository when ``path`` names the folder of
    the skill inside it. Each phase reads the run folder and adds its own output to it. A
    run can be inspected step by step, and a phase can be developed against the output of
    the phase before it.

    When ``cards_dir`` holds a card for the same place and the same files, ``AlreadyKnown``
    is raised and nothing is written, unless ``again`` is set. ``model`` and ``fetch`` are
    the functions that call a model and the network. Without ``model`` no model is called.
    """
    handed_over.check(reports)
    if path is None:
        run_dir = identify(Path(skill), out_dir, leave_out, cards_dir, stop_if_known=not again)
    else:
        run_dir = identify_repository(
            str(skill), path, out_dir, commit, cards_dir, stop_if_known=not again
        )
    collect(run_dir, fetch=fetch, offline=offline, reports=reports)
    compose(run_dir, model)
    validate(run_dir)
    render(run_dir)
    return run_dir


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="skillcard",
        description="Generate a Skill Card for one agent skill.",
    )
    parser.add_argument(
        "skill",
        help="the folder that holds the skill's SKILL.md, or a repository (an address, a "
        "folder with a git repository, or owner/repo for GitHub) when --path is given",
    )
    parser.add_argument(
        "--path",
        help="the folder of the skill inside the repository, for example skills/pdf",
    )
    parser.add_argument(
        "--commit",
        help="the commit to read, as a full commit hash, a branch or a tag (default: the "
        "newest commit of the default branch)",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("runs"),
        help="the folder that run folders are written to (default: runs)",
    )
    parser.add_argument(
        "--cards",
        type=Path,
        default=Path("cards"),
        help="the folder of existing cards the skill is compared with (default: cards)",
    )
    parser.add_argument(
        "--again",
        action="store_true",
        help="generate the card also when this version of the skill already has one",
    )
    parser.add_argument(
        "--offline",
        action="store_true",
        help="collect nothing from the network",
    )
    parser.add_argument(
        "--report",
        action="append",
        default=[],
        type=Path,
        metavar="FILE",
        help="a report about the skill that is handed over, for example the output of a "
        "skill checker (may be given more than once)",
    )
    parser.add_argument(
        "--no-model",
        action="store_true",
        help="call no model, also when the environment names one",
    )
    parser.add_argument(
        "--leave-out",
        action="append",
        default=[],
        metavar="PATH",
        help="a document about the skill that is stored next to it in a local folder, listed "
        "but not hashed (may be given more than once)",
    )
    args = parser.parse_args(argv)
    remote = "://" in args.skill or args.skill.startswith("git@")
    path = args.path if args.path is not None else ("" if remote else None)
    # An option that would have no effect is refused, so that it is not ignored silently.
    if path is None and args.commit:
        parser.error("--commit reads from a repository, name the folder of the skill with --path")
    if path is not None and args.leave_out:
        parser.error("--leave-out is for a skill in a folder on this machine")
    model = None if args.no_model else from_environment()
    try:
        run_dir = run(
            args.skill,
            args.out,
            tuple(args.leave_out),
            path=path,
            commit=args.commit,
            cards_dir=args.cards if args.cards.is_dir() else None,
            again=args.again,
            offline=args.offline,
            reports=tuple(args.report),
            model=model,
        )
    except AlreadyKnown as known:
        print(known)
        print("nothing was generated, --again generates the card anyway")
        return 0
    except (ValueError, OSError, RuntimeError) as error:
        parser.exit(2, f"skillcard: {error}\n")

    known = read_json(run_dir / "snapshot.json")["known"]
    for case, said in (
        ("same place, other files", "another version of this skill has a card"),
        ("other place, same files", "the same files have a card under another place"),
    ):
        if known[case]:
            print(f"{said}, {', '.join(known[case])}")
    if model is None:
        print("no model was called, the card holds only the values the pipeline computes")
    passed = read_json(run_dir / "validation.json")["passed"]
    print(run_dir / "card.md")
    print("validation passed" if passed else f"validation failed, see {run_dir}/validation.json")
    return 0 if passed else 1
