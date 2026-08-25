def test_note_search_treats_sql_metacharacters_as_data(client):
    client.post("/notes/", json={"title": "Public", "content": "ordinary text"})

    response = client.get("/notes/", params={"q": "' OR 1=1 --"})

    assert response.status_code == 200
    assert response.json() == []
    assert len(client.get("/notes/").json()) == 1


def test_responses_include_security_headers(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "default-src 'self'" in response.headers["content-security-policy"]
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"
    assert response.headers["referrer-policy"] == "no-referrer"


def test_cors_rejects_untrusted_origin(client):
    response = client.options(
        "/notes/",
        headers={
            "Origin": "https://attacker.example",
            "Access-Control-Request-Method": "POST",
        },
    )

    assert response.status_code == 400
    assert "access-control-allow-origin" not in response.headers


def test_dangerous_debug_routes_are_not_exposed(client):
    for path in (
        "/notes/debug/eval",
        "/notes/debug/run",
        "/notes/debug/fetch",
        "/notes/debug/read",
        "/notes/debug/hash-md5",
    ):
        assert client.get(path).status_code == 404
