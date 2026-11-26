"""Source: skills.sh. The listing of the skill at this registry and its audit pages.

The listing page is stored as it was fetched. It links to one audit page per audit partner,
and each of these is stored too. An audit is made by the partner on the copy of the skill
that skills.sh holds, on the date its page states.
"""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import quote

from skillcard import EMPTY_WORDS
from skillcard.collect.shared import entry, github_repository, store, visible_text

NAME = "skills.sh"
SITE = "https://skills.sh"


def _missing(lines: list[str]) -> bool:
    """Say whether a page that answered is the registry's page for a skill it does not list."""
    return "404" in lines and any("available in this repository" in line for line in lines)


def collect(snapshot: dict, sources_dir: Path, fetch) -> list[dict]:
    """Fetch the listing and its audit pages and return one log entry for each."""
    repository = github_repository(snapshot)
    if not repository:
        why = "the skill does not come from a repository on github.com"
        return [entry(NAME, "listing page", "", "not looked", why)]
    declared = snapshot["original_skill_name"]
    skill = snapshot["skill"] if declared in EMPTY_WORDS else declared
    listing = f"{SITE}/{repository}/{quote(skill, safe='')}"
    answer = fetch(listing)
    if answer.status == 0:
        return [entry(NAME, "listing page", listing, "failed", answer.detail)]
    if not answer.came_from("skills.sh"):
        return [entry(NAME, "listing page", listing, "failed", f"answered from {answer.address}")]
    if answer.status == 404 or (answer.status == 200 and _missing(visible_text(answer.body))):
        return [entry(NAME, "listing page", listing, "not found", "the registry does not list it")]
    if answer.status != 200:
        return [entry(NAME, "listing page", listing, "failed", f"HTTP {answer.status}")]
    entries = [
        entry(NAME, "listing page", listing, "stored", file=store(sources_dir, f"{NAME}/listing.html", answer.body))
    ]  # fmt: skip

    # The registry writes owner and repository in its own spelling, which can differ in case.
    link = re.compile(
        'href="' + re.escape(f"/{repository}/{skill}/security/") + '([a-z0-9-]+)"', re.IGNORECASE
    )
    page = answer.body.decode("utf-8", "replace")
    partners = sorted({partner.lower() for partner in link.findall(page)})
    if not partners:
        entries.append(
            entry(NAME, "audit pages", listing, "not found", "the listing links to none")
        )
    for partner in partners:
        address, item = f"{listing}/security/{partner}", f"audit page, {partner}"
        page = fetch(address)
        if page.status == 200 and page.came_from("skills.sh"):
            file = store(sources_dir, f"{NAME}/audit-{partner}.html", page.body)
            entries.append(entry(NAME, item, address, "stored", file=file))
        elif page.status == 404:
            entries.append(entry(NAME, item, address, "not found", "HTTP 404"))
        else:
            why = page.detail or f"HTTP {page.status} from {page.address}"
            entries.append(entry(NAME, item, address, "failed", why))
    return entries


def describe(run_dir: Path, entries: list[dict]) -> list[dict]:
    """Return the visible text of the stored pages for the composition, one block per page."""
    blocks = []
    for one in entries:
        if one["outcome"] != "stored":
            continue
        lines = visible_text((run_dir / one["file"]).read_bytes())
        day = one["retrieved"][:10]
        if one["item"] == "listing page":
            title = (
                f"skills.sh listing page of the skill, {one['address']}, read {day}. "
                "It describes the entry of the skill at this registry."
            )
        else:
            partner = one["item"].removeprefix("audit page, ")
            title = (
                f"skills.sh audit page by {partner}, {one['address']}, read {day}. The audit was "
                "made on the copy of the skill that skills.sh held on the date the page states."
            )
        blocks.append({"title": title, "file": one["file"], "text": "\n".join(lines)})
    return blocks
