def unwrap(response):
    assert response.json()["ok"] is True
    return response.json()["data"]


def create_note(client, title="Test", content="Hello world"):
    response = client.post("/notes/", json={"title": title, "content": content})
    assert response.status_code == 201, response.text
    return unwrap(response)


def test_note_crud_and_error_envelope(client):
    note = create_note(client)
    assert note["title"] == "Test"

    updated = unwrap(
        client.put(
            f"/notes/{note['id']}",
            json={"title": "Changed", "content": "New body"},
        )
    )
    assert updated["title"] == "Changed"

    assert unwrap(client.delete(f"/notes/{note['id']}")) == {"id": note["id"]}
    missing = client.get(f"/notes/{note['id']}")
    assert missing.status_code == 404
    assert missing.json()["error"]["code"] == "NOT_FOUND"
    assert missing.json()["data"] is None


def test_note_validation_uses_error_envelope(client):
    response = client.post("/notes/", json={"title": " ", "content": "body"})
    assert response.status_code == 422
    payload = response.json()
    assert payload["ok"] is False
    assert payload["error"]["code"] == "VALIDATION_ERROR"
    assert payload["error"]["details"]


def test_search_is_case_insensitive_sorted_and_paginated(client):
    create_note(client, "zebra", "Needle one")
    create_note(client, "Alpha", "needle two")
    create_note(client, "Other", "unrelated")

    first = unwrap(
        client.get(
            "/notes/search",
            params={
                "q": "NEEDLE",
                "page": 1,
                "page_size": 1,
                "sort": "title_asc",
            },
        )
    )
    assert first["total"] == 2
    assert first["page"] == 1
    assert first["page_size"] == 1
    assert [item["title"] for item in first["items"]] == ["Alpha"]

    second = unwrap(
        client.get(
            "/notes/search",
            params={
                "q": "needle",
                "page": 2,
                "page_size": 1,
                "sort": "title_asc",
            },
        )
    )
    assert [item["title"] for item in second["items"]] == ["zebra"]


def test_notes_pagination_boundary(client):
    create_note(client, "One", "body")
    page = unwrap(client.get("/notes/", params={"page": 2, "page_size": 10}))
    assert page == {"items": [], "total": 1, "page": 2, "page_size": 10}
    too_large = client.get("/notes/", params={"page_size": 101})
    assert too_large.status_code == 422
