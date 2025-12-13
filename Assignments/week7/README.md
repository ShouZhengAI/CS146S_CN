# Week 7

Slightly enhanced full‑stack starter (copied from Week 5) with a few backend improvements.

- FastAPI backend with SQLite (SQLAlchemy)
- Static frontend (no Node toolchain needed)
- Minimal tests (pytest)
- Pre-commit (black + ruff)
- Enhancements over Week 5:
  - Timestamps on models (`created_at`, `updated_at`)
  - Pagination and sorting for list endpoints
  - Optional filters (e.g., filter action items by completion)
  - PATCH endpoints for partial updates

## Quickstart

1) Create and activate a virtualenv, then install dependencies

```bash
cd /Users/mihaileric/Documents/code/modern-software-dev-assignments
python -m venv .venv && source .venv/bin/activate
pip install -e .[dev]
```

2) (Optional) Install pre-commit hooks

```bash
pre-commit install
```

3) Run the app (from `week6/`)

```bash
cd week7 && make run
```

Open `http://localhost:8000` for the frontend and `http://localhost:8000/docs` for the API docs.

## Structure

```
backend/                # FastAPI app
frontend/               # Static UI served by FastAPI
data/                   # SQLite DB + seed
docs/                   # TASKS for agent-driven workflows
```

## Tests

```bash
cd week7 && make test
```

## Formatting/Linting

```bash
cd week7 && make format
cd week7 && make lint
```

## Configuration

Copy `.env.example` to `.env` (in `week7/`) to override defaults like the database path.


