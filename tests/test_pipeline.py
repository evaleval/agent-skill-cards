"""Tests for the pipeline, run on the example skill in ``tests/fixtures``. No network."""

import os
import shutil
from pathlib import Path

import pytest

from skillcard import read_json
from skillcard.cli import main, run
from skillcard.identify import identify
from skillcard.validate import validate

EXAMPLE = Path(__file__).parent / "fixtures" / "hello-skill"

# Computed outside this code base, in the example skill's folder, with
#   find . -type f | sed 's|^\./||' | LC_ALL=C sort | xargs shasum -a 256 | shasum -a 256
# It changes whenever a byte of the example skill changes.
EXAMPLE_HASH = "sha256:d2b31cc7479f1659174f058cac37282b078161782ddd4127ed1bd9c15ab7cfb8"


@pytest.fixture
def skill(tmp_path: Path) -> Path:
    """A clean copy of the example skill, so that stray files next to it cannot change the hash."""
    stray = shutil.ignore_patterns(".DS_Store", "__pycache__")
    return Path(shutil.copytree(EXAMPLE, tmp_path / "hello-skill", ignore=stray))


def test_the_hash_follows_the_schema_rule(skill: Path, tmp_path: Path) -> None:
    run_dir = identify(skill, tmp_path / "runs")
    assert read_json(run_dir / "snapshot.json")["hash"] == EXAMPLE_HASH
    assert run_dir.name == "hello-skill-d2b31cc7"


def test_a_run_writes_a_card_that_passes_validation(skill: Path, tmp_path: Path) -> None:
    run_dir = run(skill, tmp_path / "runs")
    card = read_json(run_dir / "card.json")

    assert card["what_it_does"]["name"] == "hello-skill"
    assert card["what_it_does"]["author_description"] == (
        "Greets a person by name. Use it when the user asks for a greeting."
    )
    assert card["what_it_does"]["summary"] == "not examined"
    assert card["what_it_needs"]["cost"]["context_tokens"] == {
        "discovery": 17,
        "load": 50,
        "on_demand": "not examined",
    }
    assert card["who_stands_behind_it"]["license"]["frontmatter"] == "MIT"
    assert card["which_files"]["version"]["hash"] == EXAMPLE_HASH
    assert card["which_files"]["version"]["author_version"] == "not declared"
    assert [item["path"] for item in card["which_files"]["files"]] == [
        "SKILL.md",
        "scripts/greet.py",
    ]
    assert card["about_this_card"]["skill_run"] is False
    assert read_json(run_dir / "validation.json")["passed"] is True
    assert (run_dir / "card.md").read_text(encoding="utf-8").startswith("# Skill Card for")


def test_the_card_does_not_carry_the_path_on_this_machine(skill: Path, tmp_path: Path) -> None:
    run_dir = run(skill, tmp_path / "runs")
    assert str(tmp_path) not in (run_dir / "card.json").read_text(encoding="utf-8")


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


@pytest.mark.skipif(os.name == "nt", reason="creating a link needs extra rights on Windows")
def test_a_link_is_not_followed(skill: Path, tmp_path: Path) -> None:
    outside = tmp_path / "outside.txt"
    outside.write_text("not part of the skill\n", encoding="utf-8")
    (skill / "link.txt").symlink_to(outside)
    run_dir = identify(skill, tmp_path / "runs")
    snapshot = read_json(run_dir / "snapshot.json")

    assert snapshot["hash"] == EXAMPLE_HASH
    assert snapshot["skipped"] == [{"path": "link.txt", "reason": "symbolic link, not followed"}]
    assert not (run_dir / "files" / "link.txt").exists()


def test_validation_fails_when_a_frozen_file_changes(skill: Path, tmp_path: Path) -> None:
    run_dir = run(skill, tmp_path / "runs")
    (run_dir / "files" / "SKILL.md").write_text("changed\n", encoding="utf-8")
    assert validate(run_dir)["passed"] is False


def test_a_folder_without_skill_md_is_refused(tmp_path: Path) -> None:
    (tmp_path / "not-a-skill").mkdir()
    with pytest.raises(ValueError, match="no SKILL.md"):
        identify(tmp_path / "not-a-skill", tmp_path / "runs")


def test_the_command_reports_the_card(skill: Path, tmp_path: Path, capsys) -> None:
    assert main([str(skill), "--out", str(tmp_path / "runs")]) == 0
    assert "validation passed" in capsys.readouterr().out
