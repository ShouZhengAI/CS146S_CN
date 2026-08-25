# API reference

Base URL: `http://127.0.0.1:8000`. JSON is used for every request and response except `DELETE`, which returns an empty body.

## Endpoints

| Method | Path | Purpose | Success |
| --- | --- | --- | --- |
| `GET` | `/notes/` | List all notes | `200`, `Note[]` |
| `POST` | `/notes/` | Create a note | `201`, `Note` |
| `GET` | `/notes/search?q=...` | Case-insensitive title/content search | `200`, `Note[]` |
| `GET` | `/notes/{note_id}` | Read one note | `200`, `Note` |
| `PUT` | `/notes/{note_id}` | Replace a note's title and content | `200`, `Note` |
| `DELETE` | `/notes/{note_id}` | Delete one note | `204`, empty body |
| `GET` | `/action-items/` | List action items | `200`, `ActionItem[]` |
| `POST` | `/action-items/` | Create an open action item | `201`, `ActionItem` |
| `PUT` | `/action-items/{item_id}/complete` | Mark an item complete; safe to repeat | `200`, `ActionItem` |

## Schemas

### NoteCreate / NoteUpdate

```json
{
  "title": "Release plan",
  "content": "Deploy on Friday #release"
}
```

Both fields are required and trimmed. `title` must contain 1–200 characters and `content` 1–10,000 characters. Whitespace-only values are invalid. Update uses replacement semantics, so both fields are required.

### Note

```json
{
  "id": 1,
  "title": "Release plan",
  "content": "Deploy on Friday #release"
}
```

### ActionItemCreate

```json
{
  "description": "Publish release notes"
}
```

`description` is required, trimmed, nonblank, and at most 2,000 characters. New items always start with `completed: false`.

### ActionItem

```json
{
  "id": 1,
  "description": "Publish release notes",
  "completed": false
}
```

## Query and error behavior

- `q` is required, has 1–200 characters, and is trimmed before matching. A whitespace-only query returns `400` with `{"detail":"Search query must not be blank"}`.
- A missing note returns `404` with `{"detail":"Note not found"}`.
- A missing action item returns `404` with `{"detail":"Action item not found"}`.
- Invalid path/query values or malformed/invalid JSON return FastAPI's `422` validation response with a structured `detail` list.

## Synchronization check

Start the app with `make run`, then run `/docs-sync http://127.0.0.1:8000`. The workflow compares this file with `GET /openapi.json`, updates documented paths and models, and reports remaining drift.
