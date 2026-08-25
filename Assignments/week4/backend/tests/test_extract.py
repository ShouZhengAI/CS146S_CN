from backend.app.services.extract import (
    extract_action_items,
    extract_note,
    extract_tags,
)


def test_extract_action_items():
    text = """
    This is a note
    - TODO: write tests
    - Ship it!
    Not actionable
    """.strip()
    items = extract_action_items(text)
    assert "TODO: write tests" in items
    assert "Ship it!" in items


def test_extract_tags_preserves_order_and_removes_duplicates():
    text = "Plan #release with #backend. Repeat #release and allow #sprint-4."
    assert extract_tags(text) == ["release", "backend", "sprint-4"]


def test_extract_note_returns_actions_and_tags():
    result = extract_note("TODO: write docs #docs\nShip it! #release")
    assert result == {
        "action_items": ["TODO: write docs #docs", "Ship it! #release"],
        "tags": ["docs", "release"],
    }
