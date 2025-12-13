# Week 5 — Agentic Development with Warp

Use the app in `week5/` as your playground. This week mirrors the prior assignment but emphasizes the Warp agentic development environment and multi‑agent workflows.

## Learn about Warp
- Warp Agentic Development Environment: [warp.dev](https://www.warp.dev/)
- [Warp University](https://www.warp.dev/university?slug=university)


## Explore the Starter Application
Minimal full‑stack starter application.
- FastAPI backend with SQLite (SQLAlchemy)
- Static frontend (no Node toolchain needed)
- Minimal tests (pytest)
- Pre-commit (black + ruff)
- Tasks to practice agent-driven workflows

Use this application as your playground to experiment with the Warp automations you build.

### Structure

```
backend/                # FastAPI app
frontend/               # Static UI served by FastAPI
data/                   # SQLite DB + seed
docs/                   # TASKS for agent-driven workflows
```

### Quickstart

1) Activate your conda environment.

```bash
conda activate cs146s
```

2) (Optional) Install pre-commit hooks

```bash
pre-commit install
```

3) Run the app (from `week5/` directory)

```bash
make run
```

4) Open `http://localhost:8000` for the frontend and `http://localhost:8000/docs` for the API docs.

5) Play around with the starter application to get a feel for its current features and functionality.


### Testing
Run the tests (from `week5/` directory)
```bash
make test
```

### Formatting/Linting
```bash
make format
make lint
```

## Part I: Build Your Automation (Choose 2 or more) 
Select tasks from `week5/docs/TASKS.md` to implement. Your implementation must leverage Warp in both of the following ways (more details below):

- A) Use Warp Drive features — such as saved prompts, rules, or MCP servers.
- (B) Incorporate multi-agent workflows within Warp.

Keep your changes focused on backend, frontend, logic, or tests inside `week5/`.
For each selected task, note its difficulty level.


### A) Warp Drive saved prompts, rules, MCP servers (REQUIRED: at least one)
Create one or more shareable Warp Drive prompts, rules, or MCP server integrations tailored to this repo. Examples:
- Test runner with coverage and flaky‑test re‑run
- Docs sync: generate/update `docs/API.md` from `/openapi.json`, list route deltas
- Refactor harness: rename a module, update imports, run lint/tests
- Release helper: bump versions, run checks, prepare a changelog snippet
- Integrate the Git MCP server to have Warp interact with Git autonomously (creating branches, commits, PR notes, etc)

>*Tips: keep workflows focused, pass arguments, make them idempotent, and prefer headless/non‑interactive steps where possible.*

### B) Multi‑agent workflows in Warp (REQUIRED: at least one)
Run a multi‑agent session where separate agents in different Warp tabs handle independent tasks concurrently. 
- Perform multiple self-contained tasks from `TASKS.md` in separate Warp tabs using concurrent agents. Challenge: how many agents can you have working simultaneously?

>*Tips: [git worktree](https://git-scm.com/docs/git-worktree) may be helpful here to keep agents from clobbering over each other.*


## Part II: Put Your Automations to Work 
Now that you’ve built 2+ automations, let's put them to use! In the `writeup.md` under section *"How you used the automation (what pain point it resolves or accelerates)"*, describe how you leveraged each automation to improve some workflow.

## Constraints and scope
Work strictly in `week5/` (backend, frontend, logic, tests). Avoid changing other weeks unless the automation explicitly requires it and you document why.


## Deliverables
1) Two or more Warp automations, which may include:
   - Warp Drive workflows/rules (share links and/or exported definitions) and any helper scripts
   - Any supplemental prompts/playbooks used to coordinate multiple agents

2) A write‑up `writeup.md` under `week5/` that includes:
   - Design of each automation, including goals, inputs/outputs, steps
   - Before vs. after (i.e. manual workflow vs. automated workflow)
   - Autonomy levels used for each completed task (which code permissions, why, and how you supervised)
   - (if applicable) Multi‑agent notes: roles, coordination strategy, and concurrency wins/risks/failures
   - How you used the automation (what pain point it resolves or accelerates)



## SUBMISSION INSTRUCTIONS
1. Make sure you have all changes pushed to your remote repository for grading.
2. **Make sure you've added both brentju and febielin as collaborators on your assignment repository.**
2. Submit via Gradescope. 

