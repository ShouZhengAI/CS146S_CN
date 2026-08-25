# Week 5 multi-agent playbook

## Coordinator prompt

Split only independent work. Assign ownership before starting: backend agent owns models/schemas/routers, frontend agent owns `frontend/`, test agent owns `backend/tests/`, reviewer is read-only. State the shared response envelope and pagination contract in every handoff. Agents report changed files and focused evidence; the coordinator resolves shared-file conflicts and performs the final integrated check.

## Backend agent prompt

Implement the assigned endpoint end to end in the named backend files. Reuse SQLAlchemy and Pydantic patterns. Preserve transaction atomicity, normalized tags, bounded pagination, and the common response envelope. Do not touch frontend or documentation. Report contract decisions and edge cases.

## Frontend agent prompt

Consume only the documented envelope. Implement search, filters, pagination, tags, and optimistic mutations in `frontend/`. Snapshot state before each optimistic change and roll back on any network or API error. Do not change backend contracts.

## Test agent prompt

Add behavior tests for success, validation, 404/409, pagination boundaries, relationships, extraction persistence, and failed bulk-operation rollback. Do not mirror implementation details. Do not edit production files; report any contract mismatch to the coordinator.

## Reviewer prompt

Read the integrated diff without editing. Check route ordering, model cardinality, transaction boundaries, envelope consistency, Pydantic validation, frontend rollback, and whether tests would fail for plausible regressions. Return findings ordered by severity with file and line.
