"""Tests for checking committed cards without a run folder. No network."""

import json
from pathlib import Path

import pytest

from skillcard.cli import run
from skillcard.validate import card_checks, main

CARDS = sorted((Path(__file__).parent.parent / "cards").glob("*.json"))
EXAMPLE = Path(__file__).parent / "fixtures" / "hello-skill"


def failed(card: dict) -> list[str]:
    return [check["check"] for check in card_checks(card) if not check["passed"]]


@pytest.mark.parametrize("path", CARDS, ids=lambda path: path.name)
def test_every_committed_card_passes_the_card_checks(path: Path) -> None:
    assert failed(json.loads(path.read_text(encoding="utf-8"))) == []


@pytest.fixture
def card(tmp_path: Path) -> dict:
    run_dir = run(EXAMPLE, tmp_path / "runs")
    return json.loads((run_dir / "card.json").read_text(encoding="utf-8"))


def test_a_generated_card_passes_the_card_checks(card: dict) -> None:
    assert failed(card) == []


def test_a_missing_section_is_caught(card: dict) -> None:
    del card["what_it_needs"]
    assert "the card has the seven sections of the schema" in failed(card)


def test_a_wrong_schema_name_is_caught(card: dict) -> None:
    card["schema"] = "Skill Card v0"
    assert "the card names the schema it follows" in failed(card)


def test_an_edited_file_list_is_caught(card: dict) -> None:
    card["which_files"]["files"][0]["sha256"] = "0" * 64
    assert "the content hash matches the file list" in failed(card)


def test_a_blank_value_is_caught(card: dict) -> None:
    card["what_it_does"]["summary"] = ""
    assert "no value is blank" in failed(card)


def test_the_command_exits_non_zero_for_a_bad_card(card: dict, tmp_path: Path) -> None:
    good = tmp_path / "good.json"
    good.write_text(json.dumps(card), encoding="utf-8")
    del card["about_this_card"]
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps(card), encoding="utf-8")
    assert main([str(good)]) == 0
    assert main([str(good), str(bad)]) == 1
    assert main([str(tmp_path / "missing.json")]) == 1
