from backend.app.services.extract import extract_action_items, extract_content, extract_hashtags


def unwrap(response):
    assert response.json()["ok"] is True
    return response.json()["data"]


def test_extract_checkbox_legacy_actions_and_hashtags():
    text = """
    This is #Release and #release
    - [ ] write tests
    - [x] already done
    - TODO: keep legacy support
    - Ship it!
    """.strip()
    assert extract_hashtags(text) == ["release"]
    assert extract_action_items(text) == ["write tests", "TODO: keep legacy support", "Ship it!"]
    assert extract_content(text)["tags"] == ["release"]


def test_extract_endpoint_preview_and_apply(client):
    note = unwrap(
        client.post(
            "/notes/",
            json={"title": "Plan", "content": "Use #FastAPI\n- [ ] Add tests"},
        )
    )
    preview = unwrap(client.post(f"/notes/{note['id']}/extract"))
    assert preview == {"tags": ["fastapi"], "action_items": ["Add tests"], "applied": False}

    applied = unwrap(client.post(f"/notes/{note['id']}/extract", params={"apply": "true"}))
    assert applied["applied"] is True
    refreshed = unwrap(client.get(f"/notes/{note['id']}"))
    assert [tag["name"] for tag in refreshed["tags"]] == ["fastapi"]
    actions = unwrap(client.get("/action-items/"))
    assert [item["description"] for item in actions["items"]] == ["Add tests"]

    unwrap(client.post(f"/notes/{note['id']}/extract", params={"apply": "true"}))
    actions = unwrap(client.get("/action-items/"))
    assert actions["total"] == 1
