# Run backend tests

Run the Week 4 backend test workflow. Build `TEST_ARGS` from `$ARGUMENTS`: use `backend/tests` when it is empty; prepend `backend/tests` when it starts with an option such as `-k`; otherwise use the supplied path or node ID as-is.

1. From `week4/`, run `pytest -q $TEST_ARGS --maxfail=1 -x`.
2. If a test fails, stop. Report the failing test, the first relevant traceback, the likely source file, and one concrete next step. Do not report coverage from a failed run.
3. If it passes, run `pytest -q $TEST_ARGS --cov=backend.app --cov-report=term-missing`.
4. Summarize passed/skipped counts, total coverage, and uncovered line ranges. Do not change code unless explicitly asked.

Keep both invocations read-only and deterministic. Never delete the database or rewrite fixtures.