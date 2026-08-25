def test_create_and_complete_action_item(client):
    payload = {"description": "Ship it"}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 201, r.text
    item = r.json()
    assert item["completed"] is False

    r = client.put(f"/action-items/{item['id']}/complete")
    assert r.status_code == 200
    done = r.json()
    assert done["completed"] is True

    r = client.get("/action-items/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 1


def test_complete_is_idempotent(client):
    item = client.post(
        "/action-items/", json={"description": "Finish workflow"}
    ).json()
    first = client.put(f"/action-items/{item['id']}/complete")
    second = client.put(f"/action-items/{item['id']}/complete")
    assert first.status_code == 200
    assert second.status_code == 200
    assert second.json()["completed"] is True


def test_action_item_errors(client):
    response = client.post("/action-items/", json={"description": "  "})
    assert response.status_code == 422
    assert "must not be blank" in response.text

    response = client.put("/action-items/999/complete")
    assert response.status_code == 404
    assert response.json()["detail"] == "Action item not found"
