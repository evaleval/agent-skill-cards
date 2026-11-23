"""What the sources share: the request, the log entry, storing an item and reading a page."""

from __future__ import annotations

import html.parser
import http.client
import re
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urlsplit

from skillcard import __version__, net

CLIENT = f"skillcard/{__version__}"
SECONDS = 30
LARGEST_ANSWER = 5_000_000

# What can happen to an item that a source looks for.
#   stored      the item was fetched and is in the run folder
#   not found   the place answered that it has no such item
#   not looked  nothing was asked, the detail says why
#   failed      the request did not work, the detail says why
OUTCOMES = ("stored", "not found", "not looked", "failed")


@dataclass
class Answer:
    """What came back for one request. ``status`` is 0 when no answer came at all."""

    status: int
    address: str
    body: bytes
    detail: str = ""

    def came_from(self, host: str) -> bool:
        """Say whether the answer came from ``host`` or one of its subdomains."""
        name = urlsplit(self.address).hostname or ""
        return name == host or name.endswith(f".{host}")


def fetch(address: str, headers: dict[str, str] | None = None) -> Answer:
    """Ask for one address and return the answer. The sources use the network only through this.

    A request that does not work is an answer too, with the status 0 and the reason, so that
    it is logged and the run goes on.
    """
    request = urllib.request.Request(address, headers={"User-Agent": CLIENT, **(headers or {})})
    try:
        with net.open_request(request, SECONDS) as response:
            body = response.read(LARGEST_ANSWER + 1)
            if len(body) > LARGEST_ANSWER:
                return Answer(0, response.geturl(), b"", "the answer is too large to store")
            return Answer(response.status, response.geturl(), body)
    except urllib.error.HTTPError as error:
        try:
            body = error.read(LARGEST_ANSWER)
        except (OSError, http.client.HTTPException):
            body = b""
        return Answer(error.code, error.geturl() or address, body)
    except (urllib.error.URLError, TimeoutError, OSError, http.client.HTTPException) as error:
        reason = str(getattr(error, "reason", "") or error) or type(error).__name__
        return Answer(0, address, b"", reason)


def entry(
    source: str, item: str, address: str, outcome: str, detail: str = "", file: str = ""
) -> dict:
    """Return one entry of ``sources/log.json``, which says what was looked for and what came."""
    return {
        "source": source,
        "item": item,
        "address": address,
        "retrieved": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "outcome": outcome,
        "detail": detail,
        "file": file,
    }


def store(sources_dir: Path, name: str, body: bytes) -> str:
    """Store one item exactly as it was fetched and return its path inside the run folder."""
    target = sources_dir / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(body)
    return f"sources/{name}"


def github_repository(snapshot: dict) -> str | None:
    """Return ``owner/repo`` when the skill comes from a repository on github.com."""
    source = snapshot["source"]
    if source["kind"] != "repository":
        return None
    match = re.fullmatch(r"https://github\.com/([\w.-]+/[\w.-]+)", source["repository"])
    return match.group(1) if match else None


class _VisibleText(html.parser.HTMLParser):
    """Collects the text of a page that a reader sees, one piece per line."""

    HIDDEN = frozenset({"script", "style", "noscript", "svg", "template"})

    def __init__(self) -> None:
        super().__init__()
        self.lines: list[str] = []
        self._hidden = 0

    def handle_starttag(self, tag: str, attrs: list) -> None:
        if tag in self.HIDDEN:
            self._hidden += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in self.HIDDEN and self._hidden:
            self._hidden -= 1

    def handle_data(self, data: str) -> None:
        text = " ".join(data.split())
        if text and not self._hidden:
            self.lines.append(text)


def visible_text(page: bytes) -> list[str]:
    """Return the visible text of a stored HTML page, one piece of text per line.

    A page is written by someone else and can hold markup that the parser gives up on. The
    text that was read up to that point is returned then.
    """
    parser = _VisibleText()
    try:
        parser.feed(page.decode("utf-8", "replace"))
        parser.close()
    except (AssertionError, ValueError):
        pass
    return parser.lines
