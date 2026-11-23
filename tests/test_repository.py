"""Tests for reading a skill from a commit and for comparing it with existing cards.

The repositories are made on this machine in a temporary folder. No network.
"""

import os
from pathlib import Path

import pytest
from conftest import git

from skillcard import read_json, write_json
from skillcard.identify import (
    compare_with_cards,
    identify,
    identify_repository,
    location_text,
    place_of_location,
    skill_id,
)

EXAMPLE_HASH = "sha256:d2b31cc7479f1659174f058cac37282b078161782ddd4127ed1bd9c15ab7cfb8"
PATH = "skills/hello-skill"


def test_a_skill_in_a_repository_has_the_hash_of_the_same_files_in_a_folder(
    repository: Path, tmp_path: Path
) -> None:
    run_dir = identify_repository(str(repository), PATH, tmp_path / "runs")
    snapshot = read_json(run_dir / "snapshot.json")

    assert snapshot["hash"] == EXAMPLE_HASH
    assert run_dir.name == "hello-skill-d2b31cc7"
    assert [item["path"] for item in snapshot["files"]] == ["SKILL.md", "scripts/greet.py"]
    assert (run_dir / "files" / "scripts" / "greet.py").is_file()
    assert snapshot["source"]["kind"] == "repository"
    assert snapshot["source"]["path"] == PATH
    assert snapshot["source"]["commit"] == git(repository, "rev-parse", "HEAD")


def test_a_repository_on_this_machine_is_recorded_without_its_path(
    repository: Path, tmp_path: Path
) -> None:
    run_dir = identify_repository(str(repository), PATH, tmp_path / "runs")
    text = (run_dir / "snapshot.json").read_text(encoding="utf-8")
    assert str(tmp_path) not in text
    assert read_json(run_dir / "snapshot.json")["source"]["repository"] == "repository"


def test_the_files_are_read_as_the_commit_stores_them(repository: Path, tmp_path: Path) -> None:
    # A change that is not committed, and a stray file, do not reach the snapshot.
    skill_md = repository / PATH / "SKILL.md"
    skill_md.write_text(
        skill_md.read_text(encoding="utf-8") + "\nnot committed\n", encoding="utf-8"
    )
    (repository / PATH / ".env").write_text("STRAY=1\n", encoding="utf-8")

    snapshot = read_json(
        identify_repository(str(repository), PATH, tmp_path / "runs") / "snapshot.json"
    )
    assert snapshot["hash"] == EXAMPLE_HASH


def test_an_earlier_commit_can_be_read(repository: Path, tmp_path: Path) -> None:
    first = git(repository, "rev-parse", "HEAD")
    (repository / PATH / "notes.md").write_text("Added later.\n", encoding="utf-8")
    git(repository, "add", "-A")
    git(repository, "commit", "-q", "-m", "add notes")

    newest = read_json(
        identify_repository(str(repository), PATH, tmp_path / "runs") / "snapshot.json"
    )
    earlier = read_json(
        identify_repository(str(repository), PATH, tmp_path / "runs", commit=first)
        / "snapshot.json"
    )
    assert newest["hash"] != EXAMPLE_HASH
    assert [item["path"] for item in newest["files"]] == [
        "SKILL.md",
        "notes.md",
        "scripts/greet.py",
    ]
    assert earlier["hash"] == EXAMPLE_HASH
    assert earlier["source"]["commit"] == first


def test_the_executable_mark_is_recorded_but_does_not_change_the_hash(
    repository: Path, tmp_path: Path
) -> None:
    git(repository, "update-index", "--chmod=+x", f"{PATH}/scripts/greet.py")
    git(repository, "commit", "-q", "-m", "mark as executable")
    snapshot = read_json(
        identify_repository(str(repository), PATH, tmp_path / "runs") / "snapshot.json"
    )

    assert snapshot["hash"] == EXAMPLE_HASH
    assert {item["path"]: item["executable"] for item in snapshot["files"]} == {
        "SKILL.md": False,
        "scripts/greet.py": True,
    }


@pytest.mark.skipif(os.name == "nt", reason="creating a link needs extra rights on Windows")
def test_a_link_in_a_commit_is_not_followed(repository: Path, tmp_path: Path) -> None:
    (repository / PATH / "link.md").symlink_to("../../README.md")
    git(repository, "add", "-A")
    git(repository, "commit", "-q", "-m", "add a link")
    run_dir = identify_repository(str(repository), PATH, tmp_path / "runs")
    snapshot = read_json(run_dir / "snapshot.json")

    assert snapshot["hash"] == EXAMPLE_HASH
    assert snapshot["skipped"] == [{"path": "link.md", "reason": "symbolic link, not followed"}]
    assert not (run_dir / "files" / "link.md").exists()


def test_a_submodule_inside_the_skill_is_refused(repository: Path, tmp_path: Path) -> None:
    commit = git(repository, "rev-parse", "HEAD")
    git(repository, "update-index", "--add", "--cacheinfo", f"160000,{commit},{PATH}/vendor")
    git(repository, "commit", "-q", "-m", "add a submodule")
    with pytest.raises(ValueError, match="submodule"):
        identify_repository(str(repository), PATH, tmp_path / "runs")


def test_a_path_without_skill_md_is_refused(repository: Path, tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="no SKILL.md"):
        identify_repository(str(repository), "skills", tmp_path / "runs")


def test_a_commit_that_does_not_exist_is_refused(repository: Path, tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="git fetch failed"):
        identify_repository(str(repository), PATH, tmp_path / "runs", commit="0" * 40)


def test_a_short_commit_hash_is_refused_with_a_hint(repository: Path, tmp_path: Path) -> None:
    short = git(repository, "rev-parse", "HEAD")[:8]
    with pytest.raises(ValueError, match="full hash"):
        identify_repository(str(repository), PATH, tmp_path / "runs", commit=short)


def test_a_tag_is_recorded_as_the_commit_it_points_to(repository: Path, tmp_path: Path) -> None:
    git(repository, "tag", "-a", "v1.0", "-m", "a release")
    assert git(repository, "rev-parse", "v1.0") != git(repository, "rev-parse", "HEAD")

    run_dir = identify_repository(str(repository), PATH, tmp_path / "runs", commit="v1.0")
    snapshot = read_json(run_dir / "snapshot.json")
    assert snapshot["source"]["commit"] == git(repository, "rev-parse", "HEAD")
    assert snapshot["hash"] == EXAMPLE_HASH


def test_the_path_of_the_skill_can_be_written_in_several_ways(
    repository: Path, tmp_path: Path
) -> None:
    for path in (
        "./skills/hello-skill",
        "skills//hello-skill/",
        "/skills/hello-skill",
        "skills/x/../hello-skill",
    ):
        snapshot = read_json(
            identify_repository(str(repository), path, tmp_path / "runs") / "snapshot.json"
        )
        assert (snapshot["hash"], snapshot["source"]["path"]) == (EXAMPLE_HASH, PATH), path
    with pytest.raises(ValueError, match="outside the repository"):
        identify_repository(str(repository), "../elsewhere", tmp_path / "runs")


def test_a_repository_is_found_by_a_path_relative_to_the_current_folder(
    repository: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(repository.parent)
    for address in ("repository", "./repository"):
        snapshot = read_json(
            identify_repository(address, PATH, tmp_path / "runs") / "snapshot.json"
        )
        assert snapshot["hash"] == EXAMPLE_HASH
        assert snapshot["source"]["repository"] == "repository"
    with pytest.raises(
        ValueError, match="does not appear to be a git repository|not a git repository"
    ):
        identify_repository(str(tmp_path / "hello-skill"), "", tmp_path / "runs")


def test_version_control_data_planted_in_a_commit_is_not_written(
    repository: Path, tmp_path: Path
) -> None:
    # git refuses to add a folder named .git, so the commit is put together by hand, the way
    # someone with bad intent would do it. The folder holds a setting that runs a command.
    blob = git(
        repository, "hash-object", "-w", "--stdin", given="[core]\n\tfsmonitor = touch planted\n"
    )
    planted = git(repository, "mktree", given=f"100644 blob {blob}\tconfig\n")
    skill = git(repository, "ls-tree", f"HEAD:{PATH}") + f"\n040000 tree {planted}\t.GIT\n"
    skills = git(
        repository,
        "mktree",
        given=f"040000 tree {git(repository, 'mktree', given=skill)}\thello-skill\n",
    )
    root = "\n".join(
        line
        for line in git(repository, "ls-tree", "HEAD").splitlines()
        if not line.endswith("\tskills")
    )
    tree = git(repository, "mktree", given=f"{root}\n040000 tree {skills}\tskills\n")
    commit = git(repository, "commit-tree", tree, "-p", "HEAD", "-m", "plant a folder")
    git(repository, "update-ref", "refs/heads/main", commit)

    run_dir = identify_repository(str(repository), PATH, tmp_path / "runs")
    snapshot = read_json(run_dir / "snapshot.json")
    assert snapshot["source"]["commit"] == commit
    assert snapshot["hash"] == EXAMPLE_HASH
    assert snapshot["skipped"] == [{"path": ".GIT", "reason": "version control data"}]
    assert sorted(path.name for path in (run_dir / "files").iterdir()) == ["SKILL.md", "scripts"]


def test_version_control_data_in_a_folder_is_skipped_whatever_its_case(
    skill: Path, tmp_path: Path
) -> None:
    (skill / ".Git").mkdir()
    (skill / ".Git" / "config").write_text("[core]\n", encoding="utf-8")
    run_dir = identify(skill, tmp_path / "runs")
    snapshot = read_json(run_dir / "snapshot.json")
    assert snapshot["hash"] == EXAMPLE_HASH
    assert snapshot["skipped"] == [{"path": ".Git", "reason": "version control data"}]
    assert not (run_dir / "files" / ".Git").exists()


def test_a_file_name_that_leaves_the_run_folder_is_refused(tmp_path: Path) -> None:
    from skillcard.identify import _write_run

    snapshot = {"hash": "sha256:" + "0" * 64}
    for name in ("../outside.txt", "scripts/../../outside.txt", str(tmp_path / "outside.txt")):
        with pytest.raises(ValueError, match="outside the run folder"):
            _write_run(tmp_path / "runs", "a-skill", snapshot, {"SKILL.md": b"x", name: b"x"})
    for name in (".git/config", "scripts/.GIT/hooks/pre-commit"):
        with pytest.raises(ValueError, match="version control data"):
            _write_run(tmp_path / "runs", "a-skill", snapshot, {"SKILL.md": b"x", name: b"x"})
    assert not (tmp_path / "runs").exists()
    assert not (tmp_path / "outside.txt").exists()


def test_the_place_of_a_skill_is_the_repository_and_the_path() -> None:
    assert skill_id("https://github.com/Example/skills.git", "skills/pdf") == (
        "github.com/Example/skills#skills/pdf"
    )
    assert skill_id("git@github.com:example/skills.git", "") == "github.com/example/skills#."
    assert (
        skill_id("https://someone@gitlab.com/group/project", "pdf")
        == "gitlab.com/group/project#pdf"
    )
    assert skill_id("/a/folder/on/this/machine", "skills/pdf") == "none"


def test_the_place_can_be_read_back_from_the_location_of_a_card() -> None:
    for repository, path in (
        ("https://github.com/example/skills", "skills/pdf"),
        ("https://gitlab.com/group/project", "pdf"),
    ):
        source = {"kind": "repository", "repository": repository, "path": path}
        assert place_of_location(location_text(source)) == skill_id(repository, path)
    assert place_of_location("hello-skill") is None


def _card(folder: Path, name: str, location: str, files: list[dict], digest: str) -> None:
    """Write the part of a card that the comparison reads."""
    folder.mkdir(exist_ok=True)
    card = {
        "which_files": {
            "version": {"hash": digest},
            "source": {"location": location},
            "files": files,
        }
    }
    write_json(folder / name, card)


def test_a_skill_is_compared_with_the_cards_by_place_and_by_files(
    skill: Path, tmp_path: Path
) -> None:
    snapshot = read_json(identify(skill, tmp_path / "runs") / "snapshot.json")
    snapshot["skill_id"] = "github.com/example/skills#skills/hello-skill"
    here, elsewhere = (
        "GitHub Example/skills, path skills/hello-skill",
        "GitHub other/copies, path hello",
    )
    changed = [
        dict(item, sha256="0" * 64) if item["path"] != "SKILL.md" else item
        for item in snapshot["files"]
    ]
    cards = tmp_path / "cards"
    _card(cards, "same.json", here, snapshot["files"], snapshot["hash"])
    _card(cards, "earlier.json", here, changed, "sha256:" + "1" * 64)
    _card(cards, "copy.json", elsewhere, snapshot["files"], snapshot["hash"])
    _card(cards, "variant.json", elsewhere, changed, "sha256:" + "2" * 64)
    _card(cards, "unrelated.json", elsewhere, [], "sha256:" + "3" * 64)
    (cards / "broken.json").write_text("not a card", encoding="utf-8")

    assert compare_with_cards(snapshot, cards) == {
        "compared_with": 5,
        "same place, same files": ["same.json"],
        "same place, other files": ["earlier.json"],
        "other place, same files": ["copy.json"],
        "other files, same SKILL.md": ["variant.json"],
    }


def test_a_local_folder_is_never_the_same_place_as_a_card(skill: Path, tmp_path: Path) -> None:
    snapshot = read_json(identify(skill, tmp_path / "runs") / "snapshot.json")
    _card(
        tmp_path / "cards",
        "copy.json",
        "GitHub example/skills, path hello",
        snapshot["files"],
        snapshot["hash"],
    )

    known = read_json(
        identify(skill, tmp_path / "runs", cards_dir=tmp_path / "cards") / "snapshot.json"
    )["known"]
    assert known["same place, same files"] == []
    assert known["other place, same files"] == ["copy.json"]


def test_a_committed_card_is_found_for_its_own_place_and_files() -> None:
    cards = Path(__file__).parent.parent / "cards"
    card = read_json(cards / "anthropics-frontend-design-2c5958ec.json")
    snapshot = {
        "skill_id": "github.com/anthropics/skills#skills/frontend-design",
        "hash": card["which_files"]["version"]["hash"],
        "files": card["which_files"]["files"],
    }
    known = compare_with_cards(snapshot, cards)
    assert known["compared_with"] == len(list(cards.glob("*.json")))
    assert known["same place, same files"] == ["anthropics-frontend-design-2c5958ec.json"]
