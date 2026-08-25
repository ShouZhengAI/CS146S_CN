def _create_notes(client):
    rows = [
        {"title": "Charlie", "content": "shared alpha", "tags": ["work"]},
        {"title": "Alpha", "content": "shared beta", "tags": ["work", "urgent"]},
        {"title": "Bravo", "content": "private", "tags": ["personal"]},
    ]
    return [client.post("/notes/", json=row).json() for row in rows]


def test_notes_empty_and_out_of_bounds_pages(client):
    assert client.get("/notes/", params={"skip": 0, "limit": 10}).json() == []
    _create_notes(client)
    assert client.get("/notes/", params={"skip": 99, "limit": 2}).json() == []


def test_notes_custom_sort_and_page_boundaries(client):
    _create_notes(client)
    first_page = client.get(
        "/notes/", params={"sort": "title", "skip": 0, "limit": 2}
    )
    second_page = client.get(
        "/notes/", params={"sort": "title", "skip": 2, "limit": 2}
    )
    descending = client.get("/notes/", params={"sort": "-title"})

    assert [row["title"] for row in first_page.json()] == ["Alpha", "Bravo"]
    assert [row["title"] for row in second_page.json()] == ["Charlie"]
    assert [row["title"] for row in descending.json()] == ["Charlie", "Bravo", "Alpha"]


def test_notes_combined_search_and_tag_filters(client):
    _create_notes(client)
    response = client.get(
        "/notes/", params={"q": "shared", "tag": "work", "sort": "title"}
    )
    assert response.status_code == 200
    assert [row["title"] for row in response.json()] == ["Alpha", "Charlie"]


def test_action_items_custom_sort_filter_combinations_and_empty_page(client):
    for payload in [
        {"description": "Write report", "completed": False},
        {"description": "Review report", "completed": True},
        {"description": "Call client", "completed": True},
    ]:
        assert client.post("/action-items/", json=payload).status_code == 201

    response = client.get(
        "/action-items/",
        params={"completed": True, "q": "report", "sort": "description"},
    )
    assert response.status_code == 200
    assert [row["description"] for row in response.json()] == ["Review report"]

    descending = client.get("/action-items/", params={"sort": "-description"})
    assert [row["description"] for row in descending.json()] == [
        "Write report",
        "Review report",
        "Call client",
    ]
    assert client.get(
        "/action-items/", params={"skip": 3, "limit": 1}
    ).json() == []


def test_pagination_and_sort_validation_edges(client):
    for path, params in [
        ("/notes/", {"skip": -1}),
        ("/notes/", {"limit": 0}),
        ("/notes/", {"limit": 201}),
        ("/notes/", {"sort": "content"}),
        ("/action-items/", {"sort": "unknown"}),
    ]:
        response = client.get(path, params=params)
        assert response.status_code == 422
        assert response.json()["error"]["status"] == 422
