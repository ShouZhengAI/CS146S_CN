# Week 5 engineering rules

- Read `docs/TASKS.md` and the affected router, schema, model, and test before editing.
- Keep each agent inside an explicit file scope; one integration agent owns shared schemas and final review.
- API success is `{ "ok": true, "data": ... }`; API failure is `{ "ok": false, "data": null, "error": { "code": ..., "message": ... } }`.
- Collection data contains `items`, `total`, `page`, and `page_size`; `page >= 1` and `1 <= page_size <= 100`.
- Validate nonblank text at the Pydantic boundary. Return 404 for absent resources and 409 for unique-name conflicts.
- Check every bulk-operation ID before mutation so one missing ID rolls back the whole request.
- Frontend optimistic edits must snapshot old state and restore it when the request fails.
- Prefer focused endpoint checks during implementation; run the complete suite only after branches are integrated.
- Never commit secrets, local databases, generated caches, or unrelated changes.
