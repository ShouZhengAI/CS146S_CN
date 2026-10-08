# Refactor a module safely

Refactor the module described by `$ARGUMENTS` (include old path, new path, and any symbol rename). Refuse to guess if either path is missing.

1. Inspect the module, all imports/re-exports, tests, documentation, and string references.
2. Establish a clean baseline with `ruff check backend` and the narrowest relevant pytest test file.
3. Move the module once, update all callers and tests, and remove the obsolete path. Do not leave compatibility shims unless requested.
4. Run `ruff check backend`, `black --check backend`, and the relevant tests; then run `pytest -q backend/tests --maxfail=1`.
5. Search again for the old import path and symbol. Report changed files, verification commands/results, and any intentional remaining textual references.

Preserve public behavior and database data. Do not use destructive Git commands. If validation fails, keep the working tree inspectable and describe how to revert only the files changed by this workflow.