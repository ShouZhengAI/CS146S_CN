def unwrap(response):
    assert response.json()["ok"] is True
    return response.json()["data"]


def create_item(client, description):
    response = client.post("/action-items/", json={"description": description})
    assert response.status_code == 201
    return unwrap(response)


def test_filter_complete_and_pagination(client):
    first = create_item(client, "Ship it")
    second = create_item(client, "Write docs")
    done = unwrap(client.put(f"/action-items/{first['id']}/complete"))
    assert done["completed"] is True

    open_page = unwrap(
        client.get(
            "/action-items/",
            params={"completed": "false", "page": 1, "page_size": 1},
        )
    )
    assert open_page["total"] == 1
    assert open_page["items"][0]["id"] == second["id"]
    assert open_page["page_size"] == 1

    completed_page = unwrap(client.get("/action-items/", params={"completed": "true"}))
    assert [item["id"] for item in completed_page["items"]] == [first["id"]]


def test_bulk_complete_is_atomic_when_an_id_is_missing(client):
    first = create_item(client, "One")
    second = create_item(client, "Two")
    failed = client.post("/action-items/bulk-complete", json={"ids": [first["id"], 99999]})
    assert failed.status_code == 404
    assert failed.json()["error"]["code"] == "NOT_FOUND"

    still_open = unwrap(client.get("/action-items/", params={"completed": "false"}))
    assert {item["id"] for item in still_open["items"]} == {first["id"], second["id"]}

    result = unwrap(
        client.post(
            "/action-items/bulk-complete",
            json={"ids": [first["id"], second["id"]]},
        )
    )
    assert result["updated"] == 2
    assert all(item["completed"] for item in result["items"])


def test_action_item_validation_and_not_found(client):
    invalid = client.post("/action-items/", json={"description": " "})
    assert invalid.status_code == 422
    assert invalid.json()["error"]["code"] == "VALIDATION_ERROR"
    missing = client.put("/action-items/12345/complete")
    assert missing.status_code == 404
    assert missing.json()["ok"] is False
