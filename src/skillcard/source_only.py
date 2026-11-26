"""Field selection for source-only observations of already analyzed content."""

from __future__ import annotations

SOURCE_ONLY_FIELDS: dict[str, tuple[str, ...] | None] = {
    "what_it_does": ("adoption",),
    "what_is_known": None,
    "who_stands_behind_it": None,
}


def source_only_form(card_template: dict) -> dict:
    """Return the parts of the card template that are refreshed for a new source."""
    return {
        section: (
            card_template[section]
            if fields is None
            else {field: card_template[section][field] for field in fields}
        )
        for section, fields in SOURCE_ONLY_FIELDS.items()
    }


def empty_form(form: dict) -> dict:
    """Return a selected template form with every leaf marked not examined."""
    return {
        key: empty_form(value) if isinstance(value, dict) else "not examined"
        for key, value in form.items()
    }
