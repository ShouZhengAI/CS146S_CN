from types import SimpleNamespace
from unittest.mock import patch

from ..app.services.extract import extract_action_items, extract_action_items_llm


def test_extract_bullets_and_checkboxes():
    text = """
    Notes from meeting:
    - [ ] Set up database
    * implement API extract endpoint
    1. Write tests
    Some narrative sentence.
    """.strip()

    items = extract_action_items(text)
    assert "Set up database" in items
    assert "implement API extract endpoint" in items
    assert "Write tests" in items


def test_llm_bullet_list_falls_back_when_ollama_is_unavailable():
    text = "- [ ] Set up database\n* Write API tests"
    with patch("week2.app.services.extract.chat", side_effect=RuntimeError("offline")):
        assert extract_action_items_llm(text) == ["Set up database", "Write API tests"]


def test_llm_keyword_prefixes_fall_back_when_response_is_invalid():
    text = "TODO: update the documentation\nAction: review the pull request\nNext: deploy"
    response = {"message": {"content": "not valid JSON"}}
    with patch("week2.app.services.extract.chat", return_value=response):
        assert extract_action_items_llm(text) == [
            "TODO: update the documentation",
            "Action: review the pull request",
            "Next: deploy",
        ]


def test_llm_empty_input_does_not_call_ollama():
    with patch("week2.app.services.extract.chat") as mock_chat:
        assert extract_action_items_llm("  \n\t") == []
        mock_chat.assert_not_called()


def test_llm_unstructured_text_without_tasks_returns_empty_on_fallback():
    response = {"message": {"content": "{}"}}
    with patch("week2.app.services.extract.chat", return_value=response):
        assert extract_action_items_llm("The meeting took place on Tuesday. Everyone attended.") == []


def test_llm_parses_mocked_ollama_structured_response():
    response = SimpleNamespace(
        message=SimpleNamespace(
            content='{"action_items":["Email the report","Book the room","email the report",""]}'
        )
    )
    with patch("week2.app.services.extract.chat", return_value=response) as mock_chat:
        assert extract_action_items_llm("Please handle the report and room.") == [
            "Email the report",
            "Book the room",
        ]

    kwargs = mock_chat.call_args.kwargs
    assert kwargs["format"]["required"] == ["action_items"]
    assert kwargs["options"] == {"temperature": 0}


def test_llm_accepts_json_code_fences_from_older_models():
    response = {
        "message": {
            "content": '```json\n{"action_items": ["Confirm the venue"]}\n```'
        }
    }
    with patch("week2.app.services.extract.chat", return_value=response):
        assert extract_action_items_llm("Confirm where we are meeting.") == ["Confirm the venue"]
