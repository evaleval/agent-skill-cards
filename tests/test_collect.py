"""Tests for the source collection. The answers of GitHub and skills.sh are made up here,
and a function that returns them stands in for the network."""

import io
import json
from pathlib import Path

import pytest

from skillcard import read_json, write_json
from skillcard.collect import collect, describe
from skillcard.collect.shared import Answer, visible_text
from skillcard.identify import identify_repository

REPOSITORY = "https://api.github.com/repos/example/skills"
LISTING = "https://skills.sh/example/skills/hello-skill"

LISTING_PAGE = """<html><head><title>hello-skill</title><script>var hidden = 1;</script></head>
<body><h1>hello-skill</h1><p>Installs</p><p>1.2K</p><p>First Seen</p><p>Jan 5, 2026</p>
<a href="/example/skills/hello-skill/security/snyk">Snyk</a>
<a href="/example/skills/hello-skill/security/socket">Socket</a>
<a href="/example/skills/other-skill/security/snyk">another skill</a></body></html>"""

AUDIT_PAGE = """<html><body><h1>Security Audit</h1><p>Pass</p><p>Audited by</p><p>Snyk</p>
<p>on</p><p>Nov 2, 2026</p><p>Risk Level:</p><p>LOW</p></body></html>"""

NOT_LISTED_PAGE = """<html><body><p>404</p><p>hello-skill</p>
<p>isn’t available in this repository.</p></body></html>"""

ANSWERS = {
    REPOSITORY: {
        "full_name": "example/skills",
        "description": "Example skills",
        "homepage": "",
        "stargazers_count": 42,
        "forks_count": 7,
        "license": {"spdx_id": "MIT", "name": "MIT License"},
        "owner": {"login": "example", "type": "Organization"},
        "archived": False,
        "created_at": "2025-01-01T00:00:00Z",
        "pushed_at": "2026-11-01T00:00:00Z",
    },
    f"{REPOSITORY}/releases?per_page=100": [],
    LISTING: LISTING_PAGE,
    f"{LISTING}/security/snyk": AUDIT_PAGE,
}


def commits(address: str) -> list:
    """Two commits to the skill folder, with the name of a person as GitHub returns it."""
    assert "path=skills%2Fhello-skill" in address
    person = {"name": "A Person", "email": "person@example.invalid"}
    return [
        {
            "sha": "b" * 40,
            "commit": {
                "message": "Fix the greeting\n\nDetails.",
                "committer": {**person, "date": "2026-10-02T10:00:00Z"},
            },
        },
        {
            "sha": "a" * 40,
            "commit": {
                "message": "Add the skill",
                "committer": {**person, "date": "2026-01-05T10:00:00Z"},
            },
        },
    ]


def answering(answers: dict, asked: list | None = None):
    """Return a function that answers like the network would, from made-up answers."""

    def fetch(address: str, headers: dict | None = None) -> Answer:
        if asked is not None:
            asked.append((address, headers or {}))
        if address.startswith(f"{REPOSITORY}/commits?"):
            return Answer(200, address, json.dumps(commits(address)).encode())
        if address not in answers:
            return Answer(404, address, b"not found")
        body = answers[address]
        return Answer(
            200, address, body.encode() if isinstance(body, str) else json.dumps(body).encode()
        )

    return fetch


@pytest.fixture
def run_dir(repository: Path, tmp_path: Path) -> Path:
    """The run folder of the example skill, as if it had been read from github.com."""
    folder = identify_repository(str(repository), "skills/hello-skill", tmp_path / "runs")
    snapshot = read_json(folder / "snapshot.json")
    snapshot["source"]["repository"] = "https://github.com/example/skills"
    write_json(folder / "snapshot.json", snapshot)
    return folder


def outcomes(log: list[dict]) -> dict:
    return {f"{one['source']}, {one['item']}": one["outcome"] for one in log}


def test_every_item_is_stored_as_it_was_fetched_and_logged(run_dir: Path) -> None:
    log = collect(run_dir, fetch=answering(ANSWERS))

    assert outcomes(log) == {
        "github, repository record": "stored",
        "github, commits to the skill folder": "stored",
        "github, releases": "stored",
        "skills.sh, listing page": "stored",
        "skills.sh, audit page, snyk": "stored",
        "skills.sh, audit page, socket": "not found",
    }
    assert log == read_json(run_dir / "sources" / "log.json")
    assert (run_dir / "sources" / "skills.sh" / "listing.html").read_text(
        encoding="utf-8"
    ) == LISTING_PAGE
    assert read_json(run_dir / "sources" / "github" / "repository.json") == ANSWERS[REPOSITORY]
    stored = next(one for one in log if one["item"] == "listing page")
    assert stored["address"] == LISTING
    assert stored["file"] == "sources/skills.sh/listing.html"
    assert stored["retrieved"].endswith("Z")


def test_the_history_is_asked_for_up_to_the_commit_of_the_snapshot(run_dir: Path) -> None:
    asked: list = []
    collect(run_dir, fetch=answering(ANSWERS, asked))
    commit = read_json(run_dir / "snapshot.json")["source"]["commit"]
    history = next(address for address, _ in asked if "/commits?" in address)
    assert f"sha={commit}" in history


def test_a_token_is_sent_to_github_only_and_is_not_written(run_dir: Path, monkeypatch) -> None:
    monkeypatch.setenv("GITHUB_TOKEN", "made-up-token-for-this-test")
    asked: list = []
    collect(run_dir, fetch=answering(ANSWERS, asked))

    for address, headers in asked:
        assert ("Authorization" in headers) == address.startswith("https://api.github.com/")
    for path in (run_dir / "sources").rglob("*"):
        if path.is_file():
            assert "made-up-token-for-this-test" not in path.read_text(encoding="utf-8")


def test_a_skill_the_registry_does_not_list_is_logged_as_not_found(run_dir: Path) -> None:
    log = collect(run_dir, fetch=answering({**ANSWERS, LISTING: NOT_LISTED_PAGE}))
    assert outcomes(log)["skills.sh, listing page"] == "not found"
    assert not (run_dir / "sources" / "skills.sh").exists()


def test_a_request_that_fails_is_logged_and_the_run_goes_on(run_dir: Path) -> None:
    def fetch(address: str, headers: dict | None = None) -> Answer:
        if "api.github.com" in address:
            return Answer(403, address, b"rate limit")
        return Answer(0, address, b"", "the name could not be resolved")

    log = collect(run_dir, fetch=fetch)
    assert set(outcomes(log).values()) == {"failed"}
    assert "GITHUB_TOKEN" in log[0]["detail"]
    assert log[-1]["detail"] == "the name could not be resolved"


def test_an_answer_from_another_host_is_not_stored(run_dir: Path) -> None:
    def fetch(address: str, headers: dict | None = None) -> Answer:
        return Answer(200, "https://elsewhere.example/page", b"<html>something else</html>")

    log = collect(run_dir, fetch=fetch)
    assert set(outcomes(log).values()) == {"failed"}
    assert not (run_dir / "sources" / "github").exists()


def test_nothing_is_asked_for_a_skill_from_a_local_folder(skill: Path, tmp_path: Path) -> None:
    from skillcard.identify import identify

    folder = identify(skill, tmp_path / "runs")
    log = collect(folder)  # the network is closed in tests, so a request would fail the test
    assert set(outcomes(log).values()) == {"not looked"}


def test_nothing_is_asked_when_the_run_is_offline(run_dir: Path) -> None:
    log = collect(run_dir, offline=True)
    assert set(outcomes(log).values()) == {"not looked"}


def test_a_report_that_is_handed_over_is_copied_and_logged(run_dir: Path, tmp_path: Path) -> None:
    report = tmp_path / "elsewhere" / "checker-report.json"
    report.parent.mkdir()
    report.write_text('{"verdict": "pass"}', encoding="utf-8")
    log = collect(run_dir, offline=True, reports=(report,))

    entry = log[-1]
    assert (entry["source"], entry["item"], entry["outcome"]) == (
        "handed over",
        "check report",
        "stored",
    )
    assert entry["address"] == "checker-report.json"
    assert (run_dir / entry["file"]).read_text(encoding="utf-8") == '{"verdict": "pass"}'
    assert str(tmp_path) not in (run_dir / "sources" / "log.json").read_text(encoding="utf-8")
    with pytest.raises(ValueError, match="was not found"):
        collect(run_dir, offline=True, reports=(tmp_path / "missing.json",))


def test_the_stored_items_are_described_as_text_without_the_names_of_people(run_dir: Path) -> None:
    collect(run_dir, fetch=answering(ANSWERS))
    blocks = {block["file"]: block for block in describe(run_dir)}

    assert list(blocks) == [
        "sources/github/repository.json",
        "sources/github/commits-to-folder.json",
        "sources/github/releases.json",
        "sources/skills.sh/listing.html",
        "sources/skills.sh/audit-snyk.html",
    ]
    assert "stars: 42" in blocks["sources/github/repository.json"]["text"]
    assert "whole repository" in blocks["sources/github/repository.json"]["title"]
    history = blocks["sources/github/commits-to-folder.json"]["text"]
    assert "number of commits to the skill folder: 2" in history
    assert "2026-10-02 bbbbbbbb Fix the greeting" in history
    assert "A Person" not in history and "person@example.invalid" not in history
    assert "1.2K" in blocks["sources/skills.sh/listing.html"]["text"]
    assert "hidden" not in blocks["sources/skills.sh/listing.html"]["text"]
    assert "LOW" in blocks["sources/skills.sh/audit-snyk.html"]["text"]


def test_the_visible_text_of_a_page_leaves_out_scripts() -> None:
    assert visible_text(LISTING_PAGE.encode())[:4] == [
        "hello-skill",
        "hello-skill",
        "Installs",
        "1.2K",
    ]


def test_audit_pages_are_found_when_the_registry_spells_the_repository_differently(
    run_dir: Path,
) -> None:
    page = LISTING_PAGE.replace("/example/skills/hello-skill/", "/Example/Skills/hello-skill/")
    log = collect(run_dir, fetch=answering({**ANSWERS, LISTING: page}))
    assert outcomes(log)["skills.sh, audit page, snyk"] == "stored"


def test_a_page_the_parser_gives_up_on_does_not_stop_the_run(run_dir: Path) -> None:
    broken = "<html><body><p>Installs</p><![foo <p>never closed"
    assert visible_text(broken.encode())[:1] == ["Installs"]
    log = collect(run_dir, fetch=answering({**ANSWERS, LISTING: broken}))
    assert outcomes(log)["skills.sh, listing page"] == "stored"
    assert (run_dir / "sources" / "log.json").is_file()
    assert describe(run_dir)[-1]["text"].startswith("Installs")


def test_a_report_that_is_not_there_is_refused_before_anything_is_removed(
    run_dir: Path, tmp_path: Path
) -> None:
    collect(run_dir, fetch=answering(ANSWERS))
    with pytest.raises(ValueError, match="was not found"):
        collect(run_dir, offline=True, reports=(tmp_path / "missing.json",))
    assert (run_dir / "sources" / "skills.sh" / "listing.html").is_file()


def test_reports_are_described_as_text_and_a_long_one_says_that_it_is_cut(
    run_dir: Path, tmp_path: Path
) -> None:
    from skillcard.collect import handed_over

    text, long, binary = tmp_path / "report.txt", tmp_path / "long.txt", tmp_path / "report.bin"
    text.write_text("verdict: pass\n", encoding="utf-8")
    long.write_text("x" * (handed_over.LONGEST_TEXT + 10), encoding="utf-8")
    binary.write_bytes(b"\xff\xfe\x00\x01")
    collect(run_dir, offline=True, reports=(text, long, binary, text))
    blocks = {block["file"]: block["text"] for block in describe(run_dir)}

    assert blocks["sources/handed-over/report.txt"] == text.read_bytes().decode("utf-8")
    assert blocks["sources/handed-over/another-report.txt"] == (text.read_bytes().decode("utf-8"))
    assert blocks["sources/handed-over/long.txt"].endswith("characters are shown.")
    assert (
        blocks["sources/handed-over/report.bin"]
        == "This report is not a text file and is not shown."
    )


class Response(io.BytesIO):
    """What the network hands back for one request, as far as ``fetch`` reads it."""

    status = 200

    def geturl(self) -> str:
        return "https://skills.sh/a/page"


def test_fetch_turns_every_kind_of_answer_into_an_answer(monkeypatch) -> None:
    import http.client
    import urllib.error

    from skillcard.collect import shared

    asked: list = []

    def opening(result):
        def open_request(request, seconds):
            asked.append(request)
            if isinstance(result, Exception):
                raise result
            return result

        return open_request

    monkeypatch.setattr("skillcard.net.open_request", opening(Response(b"a page")))
    answer = shared.fetch("https://skills.sh/a", {"Accept": "text/html"})
    assert (answer.status, answer.address, answer.body) == (
        200,
        "https://skills.sh/a/page",
        b"a page",
    )
    assert asked[0].get_header("User-agent").startswith("skillcard/")
    assert asked[0].get_header("Accept") == "text/html"

    monkeypatch.setattr(
        "skillcard.net.open_request", opening(Response(b"x" * (shared.LARGEST_ANSWER + 1)))
    )
    assert shared.fetch("https://skills.sh/a").detail == "the answer is too large to store"

    missing = urllib.error.HTTPError("https://skills.sh/a", 404, "Not Found", {}, io.BytesIO(b"no"))
    monkeypatch.setattr("skillcard.net.open_request", opening(missing))
    answer = shared.fetch("https://skills.sh/a")
    assert (answer.status, answer.body) == (404, b"no")

    for failure in (
        urllib.error.URLError("the name could not be resolved"),
        TimeoutError("timed out"),
        http.client.IncompleteRead(b"half a page"),
        http.client.BadStatusLine("nonsense"),
    ):
        monkeypatch.setattr("skillcard.net.open_request", opening(failure))
        answer = shared.fetch("https://skills.sh/a")
        assert answer.status == 0 and answer.detail, failure


def test_a_redirect_never_carries_a_token_to_another_host() -> None:
    import urllib.request

    from skillcard.net import _CarefulRedirects

    def followed(address: str, new: str, headers: dict) -> bool:
        request = urllib.request.Request(address, headers=headers)
        return (
            _CarefulRedirects().redirect_request(request, None, 302, "Found", {}, new) is not None
        )

    secret = {"Authorization": "Bearer made-up"}
    assert followed("https://skills.sh/a", "https://www.skills.sh/a", {})
    assert followed("https://api.github.com/a", "https://api.github.com/b", secret)
    assert not followed("https://api.github.com/a", "https://elsewhere.example/b", secret)
    assert not followed("https://api.github.com/a", "http://api.github.com/b", secret)
    assert not followed("https://skills.sh/a", "http://skills.sh/a", {})


def test_a_list_that_the_api_cut_off_is_described_as_a_hundred_or_more(run_dir: Path) -> None:
    releases = [{"tag_name": f"v{n}", "published_at": "2026-01-01T00:00:00Z"} for n in range(100)]
    collect(run_dir, fetch=answering({**ANSWERS, f"{REPOSITORY}/releases?per_page=100": releases}))
    text = {block["file"]: block["text"] for block in describe(run_dir)}[
        "sources/github/releases.json"
    ]
    assert text.startswith(
        "number of releases of the repository: 100 or more, the list stops at 100"
    )
