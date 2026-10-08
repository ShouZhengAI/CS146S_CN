# Synchronize API documentation

Synchronize `docs/API.md` with the FastAPI OpenAPI document. `$ARGUMENTS` may contain a server base URL; default to `http://127.0.0.1:8000`.

1. Read the routers and schemas under `backend/app/` and the current `docs/API.md`.
2. Fetch `$ARGUMENTS/openapi.json` (or the default URL). If the server is unavailable, ask the user to run `make run`; do not invent schema fields.
3. Compare every OpenAPI path, method, status code, parameter, request body, and response model with the documentation.
4. Update only `docs/API.md`, preserving its concise endpoint-table format and adding validation/error behavior.
5. Fetch OpenAPI once more and report a diff-style summary: added, changed, removed, and remaining drift.

The operation must be idempotent. Never edit generated OpenAPI JSON, application code, or delete hand-written safety notes.