# Week 4 repository guide

## Purpose and architecture

This directory contains a small FastAPI + SQLite developer command center.

- `backend/app/main.py`: application entry point, startup, static mount, router registration.
- `backend/app/routers/notes.py`: note list/create/search/read/update/delete endpoints.
- `backend/app/routers/action_items.py`: action-item list/create/complete endpoints.
- `backend/app/schemas.py`: Pydantic request validation and response contracts.
- `backend/app/models.py`: SQLAlchemy persistence models.
- `backend/app/db.py`: engine, sessions, and one-time seed loading from `data/seed.sql`.
- `backend/app/services/extract.py`: pure note action/tag extraction.
- `backend/tests/`: isolated API and service tests.
- `frontend/`: dependency-free HTML/CSS/JavaScript client served at `/`.
- `docs/TASKS.md`: product backlog; `docs/API.md`: public HTTP contract.

Request flow: browser → FastAPI router → Pydantic schema → SQLAlchemy session → SQLite. The dependency commits successful requests and rolls back exceptions.

## Common commands

Run from `week4/`:

```bash
make run
make test
make lint
make format
pre-commit install
pre-commit run --all-files
pytest -q backend/tests/test_notes.py
```

The app is at `http://127.0.0.1:8000`; interactive API docs are at `/docs`; OpenAPI is at `/openapi.json`.

Custom workflows:

- `/tests [optional pytest selector]`
- `/docs-sync [optional base URL]`
- `/refactor-module <old path> <new path> [symbol rename]`

## Style and contracts

- Python: Black formatting, Ruff-clean imports, type annotations on application functions, four spaces, descriptive names.
- API: define request/response schemas, validate at the boundary, use `404` for missing resources and a clear `detail`; preserve FastAPI's `422` for malformed request bodies.
- Routes: place fixed paths such as `/search` before `/{id}`. Use plural resource names and return `204` with an empty body for successful deletion.
- Database: use the injected `Session`; flush before serializing newly changed rows. Never create global sessions in routers.
- JavaScript: use `fetchJSON`, `textContent` rather than HTML interpolation, `encodeURIComponent` for query values, and show rejected requests to the user.
- Tests: assert observable status, payload, persistence, validation, case-insensitive search, and missing-resource behavior. Tests must remain isolated.
- Documentation: any endpoint/schema change requires `docs/API.md` synchronization.

## Agent instructions

1. Read the affected router, schema, tests, and API documentation before editing.
2. For endpoint changes, write/update the narrow contract test, implement the smallest complete change, update the frontend if user-visible, then sync API docs.
3. Run the narrow test first, then `/tests`; run `pre-commit run --all-files` before delivery.
4. Do not edit `data/seed.sql` for test setup, commit generated databases, weaken validation to satisfy a test, or use destructive Git/database commands.
5. Preserve unrelated user changes. Do not add a second convention where an existing helper or pattern suffices.
6. Report exact commands and results; never claim checks that were not run.
