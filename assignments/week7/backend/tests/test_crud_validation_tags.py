def test_note_crud_and_tag_relationship(client):
    created = client.post(
        "/notes/",
        json={"title": "Plan", "content": "Ship safely", "tags": ["work", "urgent"]},
    )
    assert created.status_code == 201
    note = created.json()
    assert {tag["name"] for tag in note["tags"]} == {"work", "urgent"}

    fetched = client.get(f"/notes/{note['id']}")
    assert fetched.status_code == 200
    assert fetched.json()["id"] == note["id"]

    patched = client.patch(
        f"/notes/{note['id']}", json={"content": "Done", "tags": ["archive"]}
    )
    assert patched.status_code == 200
    assert patched.json()["content"] == "Done"
    assert [tag["name"] for tag in patched.json()["tags"]] == ["archive"]

    assert client.delete(f"/notes/{note['id']}").status_code == 204
    assert client.get(f"/notes/{note['id']}").status_code == 404


def test_action_item_crud(client):
    created = client.post(
        "/action-items/", json={"description": "Review", "completed": True}
    )
    assert created.status_code == 201
    item = created.json()
    assert client.get(f"/action-items/{item['id']}").json()["completed"] is True

    patched = client.patch(
        f"/action-items/{item['id']}",
        json={"description": "Review carefully", "completed": False},
    )
    assert patched.status_code == 200
    assert patched.json()["description"] == "Review carefully"
    assert patched.json()["completed"] is False

    assert client.delete(f"/action-items/{item['id']}").status_code == 204
    assert client.get(f"/action-items/{item['id']}").status_code == 404


def test_strict_body_validation_and_error_handlers(client):
    invalid_payloads = [
        ("/notes/", {"title": "", "content": "valid"}),
        ("/notes/", {"title": "valid", "content": "   "}),
        ("/notes/", {"title": "valid", "content": "body", "extra": 1}),
        ("/action-items/", {"description": "valid", "completed": 1}),
        ("/action-items/", {"description": "   "}),
    ]
    for path, payload in invalid_payloads:
        response = client.post(path, json=payload)
        assert response.status_code == 422
        assert response.json()["error"]["message"] == "Request validation failed"

    malformed = client.post(
        "/notes/", content="{not-json", headers={"content-type": "application/json"}
    )
    assert malformed.status_code == 400
    assert malformed.json()["error"]["message"] == "Malformed JSON body"

    missing = client.get("/notes/99999")
    assert missing.status_code == 404
    assert missing.json()["error"] == {"status": 404, "message": "Note not found"}


def test_tag_endpoints_enforce_case_insensitive_uniqueness(client):
    created = client.post("/tags/", json={"name": "Research"})
    assert created.status_code == 201
    tag = created.json()
    assert client.get(f"/tags/{tag['id']}").json()["name"] == "Research"
    assert client.post("/tags/", json={"name": "research"}).status_code == 400
    assert [row["name"] for row in client.get("/tags/", params={"sort": "name"}).json()] == [
        "Research"
    ]
    assert client.delete(f"/tags/{tag['id']}").status_code == 204
    assert client.get(f"/tags/{tag['id']}").status_code == 404
