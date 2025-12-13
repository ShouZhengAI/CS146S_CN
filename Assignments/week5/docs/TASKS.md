# Tasks for Repo 

## 1) Migrate frontend to Vite + React (complex)
- Scaffold a Vite + React app in `week5/frontend/` (or a subfolder like `week5/frontend/ui/`).
- Replace the current static assets with a built bundle served by FastAPI:
  - Build to `week5/frontend/dist/`.
  - Update FastAPI static mount to serve `dist` and root (`/`) to `index.html` from `dist`.
- Wire existing endpoints in React:
  - Notes list, create, delete, edit.
  - Action items list, create, complete.
- Update `Makefile` with targets: `web-install`, `web-dev`, `web-build`, and ensure `make run` builds the web bundle automatically (or documents the workflow).
- Add component/unit tests (React Testing Library) for at least two components and integration tests in `backend/tests` for API compatibility.

## 2) Notes search with pagination and sorting (medium)
- Implement `GET /notes/search?q=...&page=1&page_size=10&sort=created_desc|title_asc`.
- Use case‑insensitive matching on title/content.
- Return a payload with `items`, `total`, `page`, `page_size`.
- Add SQLAlchemy query composition for filters, ordering, and pagination.
- Update React UI with a search input, result count, and next/prev pagination controls.
- Add tests in `backend/tests/test_notes.py` for query edge cases and pagination.

## 3) Full Notes CRUD with optimistic UI updates (medium)
- Add `PUT /notes/{id}` and `DELETE /notes/{id}`.
- In the frontend, update state optimistically while handling error rollbacks.
- Validate payloads in `schemas.py` (min lengths, max lengths where reasonable).
- Add tests for success and validation errors.

## 4) Action items: filters and bulk complete (medium)
- Add `GET /action-items?completed=true|false` to filter by completion.
- Add `POST /action-items/bulk-complete` that accepts a list of IDs and marks them completed in a transaction.
- Update the frontend with filter toggles and a bulk action UI.
- Add tests to cover filters, bulk behavior, and transactional rollback on error.

## 5) Tags feature with many‑to‑many relation (complex)
- Add `Tag` model and a join table `note_tags` (many‑to‑many between `Note` and `Tag`).
- Endpoints:
  - `GET /tags`, `POST /tags`, `DELETE /tags/{id}`
  - `POST /notes/{id}/tags` to attach, `DELETE /notes/{id}/tags/{tag_id}` to detach
- Update extraction (see next task) to auto‑create/attach tags from `#hashtags`.
- Update the UI to display tags as chips and filter notes by tag.
- Add tests for model relations and endpoint behavior.

## 6) Improve extraction logic and endpoints (medium)
- Extend `backend/app/services/extract.py` to parse:
  - `#hashtags` → tags
  - `- [ ] task text` → action items
- Add `POST /notes/{id}/extract`:
  - Returns structured extraction results and optionally persists new tags/action items when `apply=true`.
- Add tests for extraction parsing and the `apply=true` persistence path.

## 7) Robust error handling and response envelopes (easy‑medium)
- Add validation with Pydantic models (min length constraints, non‑empty strings).
- Add global exception handlers to return consistent JSON envelopes:
  - `{ "ok": false, "error": { "code": "NOT_FOUND", "message": "..." } }`
  - Success responses: `{ "ok": true, "data": ... }`
- Update tests to assert envelope shapes for both success and error cases.

## 8) List endpoint pagination for all collections (easy)
- Add `page` and `page_size` to `GET /notes` and `GET /action-items`.
- Return `items` and `total` for each.
- Update the frontend to paginate lists; add tests for boundaries (empty last page, too‑large page size).

## 9) Query performance and indexes (easy‑medium)
- Add SQLite indexes where beneficial (e.g., `notes.title`, join tables for tags).
- Verify improved query plans and ensure no regressions through tests that seed larger datasets.

## 10) Test coverage improvements (easy)
- Add tests covering:
  - 400/404 scenarios for each endpoint
  - Concurrency/transactional behavior for bulk operations
  - Frontend integration tests for search, pagination, and optimistic updates (can be mocked or lightweight)

## 11) Deployable on Vercel (medium–complex)
- Frontend on Vite + React:
  - Add a `package.json` with `build` and `preview` scripts and configure Vite to output to `frontend/dist` (or `frontend/ui/dist`).
  - Add a `vercel.json` that sets the project root to `week5/frontend` and `outputDirectory` to `dist`.
  - Inject `VITE_API_BASE_URL` at build time to point to the API.
- API on Vercel (Option A, serverless FastAPI):
  - Create `week5/api/index.py` that imports the FastAPI `app` from `backend/app/main.py`.
  - Ensure Python dependencies are available to Vercel (use `pyproject.toml` or a `requirements.txt` for the function).
  - Configure CORS to allow the Vercel frontend origin.
  - Update `vercel.json` to route `/api/*` to the Python function and serve the React app for other routes.
- API elsewhere (Option B):
  - Deploy backend to a service like Fly.io or Render.
  - Configure the Vercel frontend to consume the external API via `VITE_API_BASE_URL` and set up any needed rewrites/proxies.
- Add a short deploy guide to `README.md` including environment variables, build commands, and rollback.
