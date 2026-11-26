"""Tests for checking committed cards without a run folder. No network."""

import json
from pathlib import Path

import pytest

from skillcard.cli import run
from skillcard.identify import place_of_location
from skillcard.validate import card_checks, main

CARDS = sorted((Path(__file__).parent.parent / "cards").glob("*.json"))
SHAPE = "the card has the slots of the template"


def failed(card: dict) -> list[str]:
    return [check["check"] for check in card_checks(card) if not check["passed"]]


@pytest.mark.parametrize("path", CARDS, ids=lambda path: path.name)
def test_every_committed_card_passes_the_card_checks(path: Path) -> None:
    assert failed(json.loads(path.read_text(encoding="utf-8"))) == []


@pytest.mark.parametrize("path", CARDS, ids=lambda path: path.name)
def test_the_place_of_every_committed_card_can_be_read(path: Path) -> None:
    card = json.loads(path.read_text(encoding="utf-8"))
    place = place_of_location(card["which_files"]["source"]["location"])
    assert place is not None and place.startswith("github.com/") and "#" in place


@pytest.fixture
def card(skill: Path, tmp_path: Path) -> dict:
    run_dir = run(skill, tmp_path / "runs")
    return json.loads((run_dir / "card.json").read_text(encoding="utf-8"))


def test_a_generated_card_passes_the_card_checks(card: dict) -> None:
    assert card["schema"] == "Skill Card v1.3"
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


@pytest.mark.parametrize(
    "value",
    ["line one\nline two", "a\ttab", "# heading", "[label](https://example.test)", "<b>text</b>"],
)
def test_a_non_plain_text_value_is_caught(card: dict, value: str) -> None:
    card["what_it_does"]["summary"] = value
    check = next(
        check
        for check in card_checks(card)
        if check["check"] == "card values are single-line plain text"
    )
    assert not check["passed"]
    assert any("what_it_does.summary" in problem for problem in check["detail"])


def test_a_missing_slot_is_caught(card: dict) -> None:
    del card["what_it_touches"]["side_effects"]["run"]
    assert failed(card) == [SHAPE]


def test_a_slot_that_the_template_does_not_have_is_caught(card: dict) -> None:
    card["what_it_does"]["verdict"] = "safe to use"
    assert failed(card) == [SHAPE]


def test_an_item_with_other_slots_than_the_template_shows_is_caught(card: dict) -> None:
    card["what_it_does"]["outputs"] = [{"what": "a greeting", "kind": "information"}]
    assert failed(card) == [SHAPE]


def test_a_list_can_hold_items_or_one_empty_word(card: dict) -> None:
    card["what_it_does"]["tasks"] = ["greet a person by name"]
    card["what_it_does"]["exclusions"] = "not declared"
    card["what_it_does"]["adoption"] = [
        {
            "registry": "skills.sh",
            "installs": "12",
            "first_seen": "2026-01-01",
            "counts": "the skill",
            "read": "2026-11-23",
        },
        {
            "registry": "GitHub",
            "stars": 3,
            "forks": 1,
            "counts": "the repository",
            "read": "2026-11-23",
        },
    ]
    assert failed(card) == []
    card["what_it_does"]["tasks"] = "three tasks"
    assert failed(card) == [SHAPE]


def test_the_command_exits_non_zero_for_a_bad_card(card: dict, tmp_path: Path) -> None:
    good = tmp_path / "good.json"
    good.write_text(json.dumps(card), encoding="utf-8")
    del card["about_this_card"]
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps(card), encoding="utf-8")
    assert main([str(good)]) == 0
    assert main([str(good), str(bad)]) == 1
    assert main([str(tmp_path / "missing.json")]) == 1
