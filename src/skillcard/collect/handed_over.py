"""Source: reports that someone hands over, for example the output of a skill checker.

A report is a file on this machine. It is copied into the run folder as it is and gets a log
entry. Nothing is required of its format. The log records the name of the file and not its
path on the machine.
"""

from __future__ import annotations

from pathlib import Path

from skillcard.collect.shared import entry, store

NAME = "handed over"
LONGEST_TEXT = 200_000


def check(reports: tuple[Path, ...]) -> None:
    """Refuse reports that are not there, before the collection writes anything."""
    for report in reports:
        if not Path(report).is_file():
            raise ValueError(f"the report {Path(report).name} was not found")


def collect(reports: tuple[Path, ...], sources_dir: Path) -> list[dict]:
    """Copy each report into ``sources/handed-over/`` and return one log entry for each."""
    check(reports)
    entries, used = [], set()
    for report in reports:
        report = Path(report)
        name = report.name
        while name in used:
            name = f"another-{name}"
        used.add(name)
        file = store(sources_dir, f"handed-over/{name}", report.read_bytes())
        entries.append(entry(NAME, "check report", report.name, "stored", file=file))
    return entries


def describe(run_dir: Path, entries: list[dict]) -> list[dict]:
    """Return the text of the stored reports for the composition, one block per report."""
    blocks = []
    for one in entries:
        if one["outcome"] != "stored":
            continue
        data = (run_dir / one["file"]).read_bytes()
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            text = "This report is not a text file and is not shown."
        if len(text) > LONGEST_TEXT:
            text = (
                text[:LONGEST_TEXT]
                + f"\nThe report is longer. Only its first {LONGEST_TEXT} characters are shown."
            )
        title = (
            f"Report handed over to the pipeline, file {one['address']}, added "
            f"{one['retrieved'][:10]}. The report itself says what it examined and when."
        )
        blocks.append({"title": title, "file": one["file"], "text": text})
    return blocks
