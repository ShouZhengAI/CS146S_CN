from datetime import date

from backend.app.services.extract import (
    extract_action_item_details,
    extract_action_items,
)


def test_extract_action_items_keeps_original_description_api():
    text = """
    This is a note
    - TODO: write tests
    - ACTION: review PR
    - Ship it!
    Not actionable
    """.strip()
    items = extract_action_items(text)
    assert items == ["TODO: write tests", "ACTION: review PR", "Ship it!"]


def test_extract_metadata_deadlines_and_checkbox_state():
    text = """
    - [ ] Submit report by Friday @high @alice #work #report
    - [x] Email client tomorrow @low @bob #client
    Prepare slides 08/30/2026 @carol
    """.strip()
    items = extract_action_item_details(text, today=date(2026, 8, 25))

    assert items[0].completed is False
    assert items[0].deadline == "2026-08-28"
    assert items[0].priority == "high"
    assert items[0].assignee == "alice"
    assert items[0].tags == ("work", "report")

    assert items[1].completed is True
    assert items[1].deadline == "2026-08-26"
    assert items[1].priority == "low"
    assert items[1].assignee == "bob"
    assert items[1].tags == ("client",)

    assert items[2].deadline == "2026-08-30"
    assert items[2].priority == "normal"
    assert items[2].assignee == "carol"


def test_extract_iso_relative_deadlines_and_nlp_heuristic():
    text = """
    Review the launch plan next week
    Call Sam today
    Fix release blocker 2026-09-01 #release
    A sentence with no action signal
    """.strip()
    items = extract_action_item_details(text, today=date(2026, 8, 25))
    assert [item.deadline for item in items] == [
        "2026-09-01",
        "2026-08-25",
        "2026-09-01",
    ]
    assert [item.description for item in items] == [
        "Review the launch plan next week",
        "Call Sam today",
        "Fix release blocker 2026-09-01 #release",
    ]


