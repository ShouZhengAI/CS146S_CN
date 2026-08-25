def create_note(client, title="Test", content="Hello world"):
    response = client.post("/notes/", json={"title": title, "content": content})
    assert response.status_code == 201, response.text
    return response.json()


def test_create_list_and_get_notes(client):
    note = create_note(client)

    response = client.get("/notes/")
    assert response.status_code == 200
    assert note in response.json()

    response = client.get(f"/notes/{note['id']}")
    assert response.status_code == 200
    assert response.json() == note


def test_search_notes_is_case_insensitive_and_searches_content(client):
    match = create_note(client, "Release Plan", "Deploy on Friday")
    create_note(client, "Meeting", "Discuss budget")

    response = client.get("/notes/search", params={"q": "release"})
    assert response.status_code == 200
    assert response.json() == [match]

    response = client.get("/notes/search", params={"q": "FRIDAY"})
    assert response.status_code == 200
    assert response.json() == [match]


def test_update_and_delete_note(client):
    note = create_note(client)
    response = client.put(
        f"/notes/{note['id']}",
        json={"title": "Updated", "content": "Changed content"},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated"

    response = client.delete(f"/notes/{note['id']}")
    assert response.status_code == 204
    assert client.get(f"/notes/{note['id']}").status_code == 404


def test_note_not_found_errors(client):
    payload = {"title": "Valid title", "content": "Valid content"}
    assert client.get("/notes/999").status_code == 404
    assert client.put("/notes/999", json=payload).status_code == 404
    assert client.delete("/notes/999").status_code == 404


def test_note_and_search_validation(client):
    response = client.post("/notes/", json={"title": " ", "content": "content"})
    assert response.status_code == 422
    assert "must not be blank" in response.text

    response = client.get("/notes/search", params={"q": "   "})
    assert response.status_code == 400
    assert response.json()["detail"] == "Search query must not be blank"
