"""Tests for the pipeline, run on the example skill in ``tests/fixtures``. No network."""

import hashlib
import os
import stat
from pathlib import Path
from types import SimpleNamespace

import pytest

from skillcard import HASH_SCHEME, read_json, write_json
from skillcard.cli import main, run
from skillcard.compose import one_line
from skillcard.identify import content_hash, file_entry, identify
from skillcard.validate import validate

# Computed outside this code base, in the example skill's folder, with
#   find . -type f | sed 's|^\./||' | LC_ALL=C sort | xargs shasum -a 256 | shasum -a 256
# It changes whenever a byte of the example skill changes.
EXAMPLE_HASH = "sha256:d2b31cc7479f1659174f058cac37282b078161782ddd4127ed1bd9c15ab7cfb8"


def test_the_hash_follows_the_schema_rule(skill: Path, tmp_path: Path) -> None:
    run_dir = identify(skill, tmp_path / "runs")
    snapshot = read_json(run_dir / "snapshot.json")
    assert snapshot["hash"] == EXAMPLE_HASH
    assert snapshot["hash_scheme"] == HASH_SCHEME
    assert run_dir.name == "hello-skill-d2b31cc7"


def test_hash_schemes_type_links_and_preserve_the_regular_file_digest() -> None:
    regular = file_entry("target.txt", b"target\n", False)
    link = file_entry("target.txt", b"target\n", False, "symbolic link")
    assert content_hash([regular], "skill-tree-v1") == content_hash([regular], "skill-tree-v2")
    assert content_hash([link], "skill-tree-v2") != content_hash([regular], "skill-tree-v2")
    with pytest.raises(ValueError, match="cannot hash symbolic links"):
        content_hash([link], "skill-tree-v1")


def test_untrusted_labels_are_collapsed_and_bounded() -> None:
    assert one_line("  a name\twith\ncontrols\x00 ", 40) == "a name with controls"
    assert one_line("x" * 20, 8) == "xxxxxxx…"


def test_content_reuse_requires_matching_schemes_and_exclusions() -> None:
    from skillcard.index import compatible_content

    file = file_entry("SKILL.md", b"instructions\n", False)
    executable = file_entry("SKILL.md", b"instructions\n", True)
    base = {
        "hash": content_hash([file], "skill-tree-v2"),
        "hash_scheme": "skill-tree-v2",
        "files": [file],
        "exclusions": [],
    }
    assert compatible_content(base, dict(base))
    assert compatible_content(base, dict(base, files=[executable]))
    assert not compatible_content(base, dict(base, hash_scheme="skill-tree-v1"))
    assert not compatible_content(
        base,
        dict(base, exclusions=[{"path": "notes.md", "reason": "local report", "sha256": "none"}]),
    )


def test_a_left_out_file_records_why_it_was_excluded(skill: Path, tmp_path: Path) -> None:
    (skill / "skill-card.md").write_text("A card about this skill.\n", encoding="utf-8")
    snapshot = read_json(
        identify(skill, tmp_path / "runs", leave_out=("skill-card.md",)) / "snapshot.json"
    )
    assert snapshot["exclusions"] == [
        {
            "path": "skill-card.md",
            "reason": "explicit --leave-out",
            "sha256": hashlib.sha256((skill / "skill-card.md").read_bytes()).hexdigest(),
        }
    ]


def test_the_snapshot_holds_the_identity_of_a_local_skill(skill: Path, tmp_path: Path) -> None:
    snapshot = read_json(identify(skill, tmp_path / "runs") / "snapshot.json")

    # A local folder has no place that others can reach.
    assert snapshot["skill_id"] == "none"
    assert snapshot["original_skill_name"] == "hello-skill"
    assert snapshot["source"]["kind"] == "local path"
    assert snapshot["source"]["location"] == "hello-skill"
    assert {item["path"]: item["kind"] for item in snapshot["files"]} == {
        "SKILL.md": "document",
        "scripts/greet.py": "script",
    }


def test_a_run_writes_a_card_that_passes_validation(skill: Path, tmp_path: Path) -> None:
    run_dir = run(skill, tmp_path / "runs")
    card = read_json(run_dir / "card.json")

    # Without a model only the values the pipeline computes are filled.
    assert card["skill"] == "hello-skill"
    assert card["what_it_does"]["name"] == "hello-skill"
    assert card["what_it_does"]["summary"] == "not examined"
    assert card["what_it_needs"]["cost"]["context_tokens"] == {
        "discovery": 17,
        "load": 50,
        "on_demand": "not examined",
        "on_demand_files": "not examined",
    }
    assert card["who_stands_behind_it"]["license"]["frontmatter"] == "MIT"
    assert card["which_files"]["version"]["hash"] == EXAMPLE_HASH
    assert card["which_files"]["version"]["author_version"] == "not declared"
    assert card["which_files"]["counts"] == {"script": 1, "document": 1, "data": 0, "binary": 0}
    assert card["which_files"]["composition"] == "instructions with scripts"
    assert [item["path"] for item in card["which_files"]["files"]] == [
        "SKILL.md",
        "scripts/greet.py",
    ]
    assert "without a model" in card["about_this_card"]["by"]
    assert read_json(run_dir / "validation.json")["passed"] is True
    assert (run_dir / "card.md").read_text(encoding="utf-8").startswith("# Skill Card for")


def test_a_run_writes_every_file_the_readme_lists(skill: Path, tmp_path: Path) -> None:
    run_dir = run(skill, tmp_path / "runs")
    for name in (
        "snapshot.json",
        "sources/log.json",
        "card.json",
        "evidence.json",
        "validation.json",
    ):
        assert (run_dir / name).is_file(), name
    assert (run_dir / "files" / "SKILL.md").is_file()


def test_the_card_does_not_carry_the_path_on_this_machine(skill: Path, tmp_path: Path) -> None:
    run_dir = run(skill, tmp_path / "runs")
    for name in ("card.json", "snapshot.json", "evidence.json", "sources/log.json"):
        assert str(tmp_path) not in (run_dir / name).read_text(encoding="utf-8"), name


def test_a_left_out_document_is_listed_but_not_hashed(skill: Path, tmp_path: Path) -> None:
    (skill / "skill-card.md").write_text("A card about this skill.\n", encoding="utf-8")
    run_dir = identify(skill, tmp_path / "runs", leave_out=("skill-card.md",))
    snapshot = read_json(run_dir / "snapshot.json")

    assert snapshot["hash"] == EXAMPLE_HASH
    assert {item["path"]: item["in_hash"] for item in snapshot["files"]} == {
        "SKILL.md": True,
        "scripts/greet.py": True,
        "skill-card.md": False,
    }


def test_a_link_is_not_followed(
    skill: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    outside = tmp_path / "outside.txt"
    outside.write_text("not part of the skill\n", encoding="utf-8")
    link = skill / "link.txt"
    link.write_text("placeholder that must not be read", encoding="utf-8")
    target = "../outside.txt"
    original_lstat = Path.lstat
    original_readlink = os.readlink

    def lstat(path: Path):
        return SimpleNamespace(st_mode=stat.S_IFLNK) if path == link else original_lstat(path)

    def readlink(path: str | bytes | os.PathLike):
        return target if Path(path) == link else original_readlink(path)

    # Simulate the OS link metadata so this local-folder case also runs on Windows
    # machines where creating symlinks requires an elevated privilege.
    monkeypatch.setattr(Path, "lstat", lstat)
    monkeypatch.setattr(os, "readlink", readlink)
    run_dir = identify(skill, tmp_path / "runs")
    snapshot = read_json(run_dir / "snapshot.json")

    link = next(item for item in snapshot["files"] if item["path"] == "link.txt")
    assert snapshot["hash"] != EXAMPLE_HASH
    assert link["file_type"] == "symbolic link"
    assert link["bytes"] == len(os.fsencode(target))
    assert link["sha256"] == hashlib.sha256(os.fsencode(target)).hexdigest()
    assert "link.txt" not in [item["path"] for item in snapshot["skipped"]]
    assert not (run_dir / "files" / "link.txt").exists()


def test_validation_fails_when_a_frozen_file_changes(skill: Path, tmp_path: Path) -> None:
    run_dir = run(skill, tmp_path / "runs")
    (run_dir / "files" / "SKILL.md").write_text("changed\n", encoding="utf-8")
    assert validate(run_dir)["passed"] is False


def test_validation_fails_when_evidence_names_a_file_that_is_not_there(
    skill: Path, tmp_path: Path
) -> None:
    run_dir = run(skill, tmp_path / "runs")
    evidence = read_json(run_dir / "evidence.json")
    evidence.append({"field": "what_it_does.summary", "by": "model", "from": ["files/README.md"]})
    write_json(run_dir / "evidence.json", evidence)

    result = validate(run_dir)
    failed = [check for check in result["checks"] if not check["passed"]]
    assert [check["detail"] for check in failed] == [["what_it_does.summary: 'files/README.md'"]]


def test_a_folder_without_skill_md_is_refused(tmp_path: Path) -> None:
    (tmp_path / "not-a-skill").mkdir()
    with pytest.raises(ValueError, match="no SKILL.md"):
        identify(tmp_path / "not-a-skill", tmp_path / "runs")


def test_the_command_reports_the_card(skill: Path, tmp_path: Path, capsys) -> None:
    assert main([str(skill), "--out", str(tmp_path / "runs")]) == 0
    printed = capsys.readouterr().out
    assert "validation passed" in printed
    assert "no model was called" in printed


def test_a_phase_can_be_called_alone_on_an_existing_run_folder(skill: Path, tmp_path: Path) -> None:
    from skillcard.collect import collect
    from skillcard.compose import compose
    from skillcard.validate import main as check

    run_dir = run(skill, tmp_path / "runs")
    before = read_json(run_dir / "card.json")
    collect(run_dir)
    assert compose(run_dir) == before
    assert validate(run_dir)["passed"] is True
    assert check([str(run_dir)]) == 0


def test_the_command_reads_a_skill_from_a_repository(
    repository: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys
) -> None:
    out = str(tmp_path / "runs")
    assert main([str(repository), "--path", "skills/hello-skill", "--out", out]) == 0
    card = read_json(tmp_path / "runs" / "hello-skill-d2b31cc7" / "card.json")
    assert card["which_files"]["version"]["hash"] == EXAMPLE_HASH
    assert card["which_files"]["source"]["kind"] == "repository"
    assert card["which_files"]["source"]["location"] == "repository, path skills/hello-skill"
    assert card["version"].startswith("repository at ")
    assert "validation passed" in capsys.readouterr().out

    # The repository can also be named by a path that is relative to the current folder.
    monkeypatch.chdir(tmp_path)
    assert main(["repository", "--path", "./skills//hello-skill/", "--out", out]) == 0
    assert main(["./repository", "--path", "skills/hello-skill", "--out", out]) == 0


def test_an_option_that_would_have_no_effect_is_refused(
    skill: Path, repository: Path, tmp_path: Path, capsys
) -> None:
    out = str(tmp_path / "runs")
    with pytest.raises(SystemExit) as stopped:
        main([str(skill), "--commit", "main", "--out", out])
    assert stopped.value.code == 2
    with pytest.raises(SystemExit) as stopped:
        main(
            [
                str(repository),
                "--path",
                "skills/hello-skill",
                "--leave-out",
                "SKILL.md",
                "--out",
                out,
            ]
        )
    assert stopped.value.code == 2
    assert not (tmp_path / "runs").exists()


def test_a_report_that_is_not_there_stops_the_run_before_anything_is_written(
    skill: Path, tmp_path: Path
) -> None:
    with pytest.raises(SystemExit) as stopped:
        main(
            [
                str(skill),
                "--report",
                str(tmp_path / "missing.json"),
                "--out",
                str(tmp_path / "runs"),
            ]
        )
    assert stopped.value.code == 2
    assert not (tmp_path / "runs").exists()


def test_the_run_stops_when_this_version_already_has_a_card(
    skill: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys
) -> None:
    out = str(tmp_path / "runs")
    assert main([str(skill), "--out", out]) == 0
    run_dir = tmp_path / "runs" / "hello-skill-d2b31cc7"
    before = {path: path.read_bytes() for path in run_dir.rglob("*") if path.is_file()}
    capsys.readouterr()

    # From here on the comparison says that a card for this place and these files exists.
    def compared(snapshot: dict, cards_dir: Path | None) -> dict:
        return {
            "compared_with": 1,
            "same place, same files": ["hello-skill-d2b31cc7.json"],
            "same place, other files": [],
            "other place, same files": [],
            "other files, same SKILL.md": [],
            "file_comparisons": [],
        }

    monkeypatch.setattr("skillcard.identify.compare_with_cards", compared)
    assert main([str(skill), "--out", out]) == 0
    printed = capsys.readouterr().out
    assert "already has a card, hello-skill-d2b31cc7.json" in printed
    assert "nothing was generated" in printed
    # The files of the earlier run are all still there and unchanged.
    assert {path: path.read_bytes() for path in run_dir.rglob("*") if path.is_file()} == before

    assert main([str(skill), "--out", out, "--again"]) == 0
    known = read_json(run_dir / "snapshot.json")["known"]
    assert known["same place, same files"] == ["hello-skill-d2b31cc7.json"]
    assert (run_dir / "card.json").is_file()


def test_a_value_of_spaces_only_is_blank(skill: Path, tmp_path: Path) -> None:
    run_dir = run(skill, tmp_path / "runs")
    card = read_json(run_dir / "card.json")
    card["what_it_does"]["summary"] = "   "
    write_json(run_dir / "card.json", card)
    failed = [check["check"] for check in validate(run_dir)["checks"] if not check["passed"]]
    assert failed == ["no value is blank"]


def test_evidence_with_a_name_that_no_file_can_have_fails_the_check_and_nothing_else(
    skill: Path, tmp_path: Path
) -> None:
    run_dir = run(skill, tmp_path / "runs")
    evidence = read_json(run_dir / "evidence.json")
    for name in ("files/SKILL.md\x00", "x" * 5000, "", "../outside.txt", 7):
        evidence.append({"field": "what_it_does.summary", "by": "model", "from": [name]})
    evidence.append({"field": "what_it_does.tasks", "by": "model", "from": "files/SKILL.md"})
    write_json(run_dir / "evidence.json", evidence)

    result = validate(run_dir)
    failed = [check for check in result["checks"] if not check["passed"]]
    assert [check["check"] for check in failed] == [
        "every source that evidence.json names exists in the run folder"
    ]
    assert len(failed[0]["detail"]) == 6
