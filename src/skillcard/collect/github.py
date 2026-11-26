"""Source: GitHub. What the repository of the skill says, and the history of the skill folder.

Three items are stored as the GitHub API returns them: the record of the repository, the
commits to the skill folder up to the commit the files were read at, and the releases. A
record of the repository describes the whole repository, which can hold many skills.

The stored answers hold names and addresses of the people who made the commits. They stay in
the run folder, which is not committed, and ``describe`` leaves them out.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from urllib.parse import urlencode

from skillcard.collect.shared import Answer, entry, github_repository, store

NAME = "github"
API = "https://api.github.com"
PER_PAGE = 100


def collect(snapshot: dict, sources_dir: Path, fetch) -> list[dict]:
    """Fetch the three items and return one log entry for each."""
    repository = github_repository(snapshot)
    if not repository:
        why = "the skill does not come from a repository on github.com"
        return [entry(NAME, "all items", "", "not looked", why)]
    headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
    if token := os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {token}"
    source = snapshot["source"]
    history = {"sha": source["commit"], "per_page": PER_PAGE}
    if source["path"]:
        history["path"] = source["path"]
    items = [
        ("repository record", f"{API}/repos/{repository}", "repository.json"),
        (
            "commits to the skill folder",
            f"{API}/repos/{repository}/commits?{urlencode(history)}",
            "commits-to-folder.json",
        ),
        ("releases", f"{API}/repos/{repository}/releases?per_page={PER_PAGE}", "releases.json"),
    ]
    return [
        _record(item, address, fetch(address, headers), sources_dir, name)
        for item, address, name in items
    ]


def _record(item: str, address: str, answer: Answer, sources_dir: Path, name: str) -> dict:
    """Store one answer when it is usable and return its log entry."""
    if answer.status == 0:
        return entry(NAME, item, address, "failed", answer.detail)
    if not answer.came_from("api.github.com"):
        return entry(NAME, item, address, "failed", f"answered from {answer.address}")
    if answer.status == 404:
        return entry(NAME, item, address, "not found", "HTTP 404")
    if answer.status in (403, 429):
        why = f"HTTP {answer.status}, the limit of requests may be reached, see GITHUB_TOKEN"
        return entry(NAME, item, address, "failed", why)
    if answer.status != 200:
        return entry(NAME, item, address, "failed", f"HTTP {answer.status}")
    return entry(
        NAME, item, address, "stored", file=store(sources_dir, f"{NAME}/{name}", answer.body)
    )


def _load(run_dir: Path, one: dict) -> object:
    try:
        return json.loads((run_dir / one["file"]).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def _counted(number: int) -> str:
    """Say how many items a list holds. A list that is full was cut off by the API."""
    if number < PER_PAGE:
        return str(number)
    return f"{PER_PAGE} or more, the list stops at {PER_PAGE} and older ones may exist"


def describe(run_dir: Path, entries: list[dict]) -> list[dict]:
    """Return the stored items as plain text for the composition, one block per item."""
    blocks = []
    for one in entries:
        if one["outcome"] != "stored":
            continue
        data, day = _load(run_dir, one), one["retrieved"][:10]
        if one["item"] == "repository record" and isinstance(data, dict):
            license_ = data.get("license") or {}
            owner = data.get("owner") or {}
            detected = f"{license_.get('spdx_id') or 'none'} ({license_.get('name') or 'no name'})"
            lines = [
                f"repository: {data.get('full_name')}",
                f"owner: {owner.get('login')}, a GitHub {str(owner.get('type')).lower()}",
                f"description: {data.get('description')}",
                f"homepage: {data.get('homepage') or 'none given'}",
                f"stars: {data.get('stargazers_count')}",
                f"forks: {data.get('forks_count')}",
                f"license GitHub detects: {detected}",
                f"archived: {data.get('archived')}",
                f"created: {str(data.get('created_at'))[:10]}",
                f"last push: {str(data.get('pushed_at'))[:10]}",
            ]
            title = (
                f"GitHub record of the repository, read {day}. It describes the whole repository."
            )
        elif one["item"] == "commits to the skill folder" and isinstance(data, list):
            rows = []
            for commit in data:
                inner = commit.get("commit") or {}
                when = str((inner.get("committer") or {}).get("date"))[:10]
                message = (str(inner.get("message") or "").splitlines() or [""])[0]
                rows.append((when, f"{when} {str(commit.get('sha'))[:8]} {message[:120]}"))
            dates = sorted(when for when, _ in rows)
            lines = [f"number of commits to the skill folder: {_counted(len(rows))}"]
            if dates:
                lines += [f"oldest commit in this list: {dates[0]}", f"newest: {dates[-1]}"]
            lines += [row for _, row in rows]
            title = (
                f"GitHub commits to the skill folder, up to the commit the files were read at, "
                f"read {day}."
            )
        elif one["item"] == "releases" and isinstance(data, list):
            dates = sorted(str(r.get("published_at"))[:10] for r in data if r.get("published_at"))
            lines = [f"number of releases of the repository: {_counted(len(data))}"]
            lines.append(f"newest release: {dates[-1] if dates else 'none'}")
            lines += [f"{str(r.get('published_at'))[:10]} {r.get('tag_name')}" for r in data[:20]]
            title = f"GitHub releases of the repository, read {day}. They are not releases of the skill."
        else:
            continue
        blocks.append({"title": title, "file": one["file"], "text": "\n".join(lines)})
    return blocks
