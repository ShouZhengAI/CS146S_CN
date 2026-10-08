from backend.app.models import Note, Tag


def unwrap(response):
    assert response.json()["ok"] is True
    return response.json()["data"]


def test_model_relationship_is_bidirectional():
    note = Note(title="Model", content="relationship")
    tag = Tag(name="sqlalchemy")
    note.tags.append(tag)
    assert tag in note.tags
    assert note in tag.notes


def test_tag_crud_and_note_relationship(client):
    note = unwrap(client.post("/notes/", json={"title": "Tagged", "content": "Body"}))
    created = client.post("/tags/", json={"name": "#Python"})
    assert created.status_code == 201
    tag = unwrap(created)
    assert tag["name"] == "python"

    attached = unwrap(client.post(f"/notes/{note['id']}/tags", json={"tag_id": tag["id"]}))
    assert attached["tags"] == [tag]
    # Reattaching is idempotent and does not duplicate the association row.
    attached = unwrap(client.post(f"/notes/{note['id']}/tags", json={"tag_id": tag["id"]}))
    assert attached["tags"] == [tag]

    filtered = unwrap(client.get("/notes/", params={"tag": "python"}))
    assert filtered["total"] == 1
    assert filtered["items"][0]["id"] == note["id"]

    detached = unwrap(client.delete(f"/notes/{note['id']}/tags/{tag['id']}"))
    assert detached["tags"] == []
    assert unwrap(client.delete(f"/tags/{tag['id']}")) == {"id": tag["id"]}


def test_tag_conflict_and_relationship_errors(client):
    tag = unwrap(client.post("/tags/", json={"name": "api"}))
    conflict = client.post("/tags/", json={"name": "API"})
    assert conflict.status_code == 409
    assert conflict.json()["error"]["code"] == "CONFLICT"

    note = unwrap(client.post("/notes/", json={"title": "Note", "content": "Body"}))
    missing_tag = client.post(f"/notes/{note['id']}/tags", json={"tag_id": 9999})
    assert missing_tag.status_code == 404
    not_attached = client.delete(f"/notes/{note['id']}/tags/{tag['id']}")
    assert not_attached.status_code == 404
