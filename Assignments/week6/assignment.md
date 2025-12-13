# Week 6 — Scan and Fix Vulnerabilities with Semgrep

## Assignment Overview
Run static analysis against the provided app in `week6/` using **Semgrep**. Triage findings and remediate a minimum of 3 security issues. In your write-up, explain what issues Semgrep surfaced and how you fixed them.


## Learn about Semgrep
Semgrep is an open-source, static analysis tool that searches code, finds bugs, and enforces secure guardrails and coding standards.

1. Click [here](https://github.com/semgrep/semgrep/blob/develop/README.md) to learn about Semgrep.

2. Follow the installation instructions in the link above. It is up to you whether you prefer to use the **Semgrep Appsec Platform** or the **CLI tool**.


## Scan tasks

### What you will scan
- Backend Python (FastAPI): `week6/backend/`
- Frontend JavaScript: `week6/frontend/`
- Dependencies: `week6/requirements.txt`
- Config/env (for secrets): files within `week6/`


### Run a general security scan plus focused scans for secrets and dependencies.

From the **assignment repository root**, run the following command to apply a curated CI-style bundle that includes both code and secrets rules:
```bash
semgrep ci --subdir week6
```

## Task
1. Pick any 3 issues identified by Semgrep and fix them using an AI coding tool of your choice.

2. Show precise edits and explain the mitigation (e.g., parameterized SQL, safer APIs, stronger crypto, sanitized DOM writes, restricted CORS, dependency upgrades).

3. Important: Ensure the app still runs and tests still pass after your fixes.

## Deliverables 
### 1. Brief findings overview 
- Summarize the categories Semgrep reported (SAST/Secrets/SCA).
- Note any false positives or noisy rules you chose to ignore and why.

### 2. Three fixes (before → after)
For each fixed issue:
- File and line(s)
- Rule/category Semgrep flagged
- Brief risk description
- Your change (short code diff or explanation, AI coding tool usage)
- Why this mitigates the issue


## Tips
- Prefer minimal, targeted changes that address the root cause.
- Re‑run Semgrep after each fix to confirm the finding is resolved and no new ones were introduced.
- For dependencies, document upgraded versions and link to advisories if you used supply-chain scanning.


## Submission Instructions
1. Make sure you have all changes pushed to your remote repository for grading.
2. Make sure you've added both brentju and febielin as collaborators on your assignment repository.
2. Submit via Gradescope. 