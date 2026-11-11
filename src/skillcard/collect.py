"""Phase 2, source collection.

Gathers what is known about the skill from outside its files and stores it unchanged under
``sources/``. That is registry and repository metadata, check reports in the format of the
tool that wrote them, and fetched pages. Every item gets an entry in ``sources/log.json`` with
its address and the date it was retrieved. This phase stores and does not interpret.

Nothing is collected yet. The log is empty, and the card reads "not examined" for every row
that needs a source outside the skill's files.
"""

from __future__ import annotations

from pathlib import Path

from skillcard import write_json


def collect(run_dir: Path) -> list[dict]:
    """Create ``sources/`` in the run folder and return the log of what was collected."""
    sources = run_dir / "sources"
    sources.mkdir(exist_ok=True)
    log: list[dict] = []
    write_json(sources / "log.json", log)
    return log
