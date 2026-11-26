"""Phase 2, source collection.

Gathers what is known about the skill from outside its files and stores it unchanged under
``sources/``. Every item that was looked for gets an entry in ``sources/log.json`` with its
address, the time it was retrieved and what came of it, also when nothing was found. This
phase stores and does not interpret.

Each source is one file in this folder with two functions. ``collect`` fetches the items of
the source and returns their log entries. ``describe`` turns the stored items into plain
text for the composition. A further source is added by writing such a file and naming it in
``SOURCES`` below.

Only a skill that comes from a repository on github.com is looked up. A skill that was read
from a local folder has no place to look it up, and the log says so.
"""

from __future__ import annotations

import shutil
from pathlib import Path

from skillcard import read_json, write_json
from skillcard.collect import github, handed_over, skills_sh
from skillcard.collect.shared import entry
from skillcard.collect.shared import fetch as fetch_from_network

SOURCES = (github, skills_sh)


def collect(
    run_dir: Path,
    fetch=None,
    offline: bool = False,
    reports: tuple[Path, ...] = (),
) -> list[dict]:
    """Collect the sources for the skill in ``run_dir`` and return the log.

    ``fetch`` is the function that asks for one address. Tests pass their own, so that they
    run without a network. ``reports`` are files handed over on this machine, for example
    the report of a skill checker. The phase writes its folder anew each time it runs.
    """
    snapshot = read_json(run_dir / "snapshot.json")
    handed_over.check(tuple(reports))
    sources_dir = run_dir / "sources"
    if sources_dir.exists():
        shutil.rmtree(sources_dir)
    sources_dir.mkdir()
    log: list[dict] = []
    for source in SOURCES:
        if offline:
            why = "the run was started without access to the network"
            log.append(entry(source.NAME, "all items", "", "not looked", why))
        else:
            log += source.collect(snapshot, sources_dir, fetch or fetch_from_network)
    log += handed_over.collect(tuple(reports), sources_dir)
    write_json(sources_dir / "log.json", log)
    return log


def describe(run_dir: Path) -> list[dict]:
    """Return every stored item as a block of plain text, in the order of the log.

    A block has a title that says what the item is and when it was read, the path of the
    stored item inside the run folder, and the text.
    """
    log = read_json(run_dir / "sources" / "log.json")
    blocks: list[dict] = []
    for source in (*SOURCES, handed_over):
        blocks += source.describe(run_dir, [one for one in log if one["source"] == source.NAME])
    return blocks
