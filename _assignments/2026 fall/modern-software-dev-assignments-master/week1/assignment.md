# Week 1: Trace Dissection of a Real Claude Code Session

## Assignment Overview

This week you will put a real Claude Code session behind a proxy, capture the actual HTTP requests it sends, and **dissect them**. You are not building anything new. You are reading someone else's production system at the level of detail where its design decisions become visible.

### Learning Goals

- **Trace** a real coding session from a production-grade coding agent and understand its call structure.
- **Identify** how prompting, tool schemas, and model responses interact during a non-trivial coding task.
- **Reflect** on which behaviors you would replicate, and which you would change, in your own custom agents.

## Materials

- **[Intercepting Claude Code Requests](https://www.ai.moda/en/blog/tutorial-intercepting-claude-code-requests)**: the technique this assignment is built on. Read it first.
- **[Anthropic Messages API reference](https://docs.claude.com/en/api/messages)**: the request shape you will be reading (`system`, `tools`, `messages`).
- **[Claude Code settings reference](https://docs.claude.com/en/docs/claude-code/settings)**: how user-level (`~/.claude/settings.json`) and project-level (`.claude/settings.json`) settings work.

## Setup

**Prerequisite: Claude Code**. Stanford provides access to Claude Code via your SUNet ID. If you haven't activated your account yet, [request access](https://uit.stanford.edu/service/claude), then [install and sign in](https://code.claude.com/docs/en/setup). After your account is approved and you have completed the install, confirm with `claude --version` and record that version in your writeup.

**1. Install mitmproxy:**

- **macOS**: `brew install --cask mitmproxy`.
- **Windows**: run the installer from [mitmproxy.org](https://mitmproxy.org/), which puts `mitmweb` on your `PATH`.
- **Linux, or any platform**: `pip install mitmproxy`, inside the course conda env if you made one.

**2. Start it as a reverse proxy:**

```bash
mitmweb --listen-host 127.0.0.1 --listen-port 58888 \
        --web-open-browser --mode reverse:https://api.anthropic.com \
        -w session.flows
```

Traffic sent to `127.0.0.1:58888` is forwarded to the real API; the inspection UI opens at `http://localhost:8081`. Reverse mode means you point Claude Code at a plain-HTTP local address, so there is no CA certificate to install. `-w session.flows` saves every flow to disk; run the command from a directory **outside** any git repo so the capture file won't be committed by accident.

**3. Point Claude Code at it**: in the repo you will use for Part I, create a **project-level** `.claude/settings.json`:

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "http://127.0.0.1:58888",
    "ENABLE_TOOL_SEARCH": "true"
  }
}
```

> ⚠️ **Don't put this in `~/.claude/settings.json`!** Otherwise, any Claude Code session on your machine will land in your capture (and sessions won't work once `mitmweb` is stopped).

**4. Verify**: start a new `claude` session, send anything, and confirm a `POST /v1/messages` flow appears in mitmweb.

**5. Post-Assignment**: when you're done, delete the repo's `.claude/settings.json` (or its `env` block) and stop `mitmweb`.

## Part I: Capture a Session (15 pts)

Run **one** session under the proxy meeting all four requirements:

1. **Multi-file**: touches at least two files.
2. **Fails at least once**: you need an error-recovery sequence. Breaking a test on purpose is the reliable way to get one.
3. **Long enough to plan**: the agent should make an explicit plan, not fire a single tool call: a task list, plan mode, or a plan file.
4. **Your own repo**: a scratch project, not this one.

**Task ideas**, if you'd rather not invent one:

- Delete a function that other modules import, then ask Claude to restore full functionality with the tests passing.
- Add an endpoint plus tests to a small web app, then ask it to make the suite pass on a dependency version you don't have installed.
- Rename a module and have it update every import, then run lint and tests.
- Ask for a feature that requires an unfamiliar library, so the agent has to look up the API before it can write anything.

In the mitmweb UI, select a `POST /v1/messages` flow and download the **request body** as JSON. Keep these locally. You are not submitting them, but every later part is graded on evidence drawn from them, so keep enough to support your answers.

If your mitmweb session terminates, you can work from the saved `session.flows` file: reopen it with `mitmweb -r session.flows`.

### ⚠️ Sanitize what you quote

Your capture contains your own source code, file paths, and credentials. Nothing from it should reach the repo except the excerpts you deliberately quote in `writeup.md`.

- Never paste raw flows or HTTP headers, since that is where `x-api-key` / `authorization` live.
- **Request bodies can contain secrets too.** Anything the agent read (`.env`, config files, command outputs) is replayed in `messages`. Check tool results before quoting them.
- Keep `session.flows` out of every git repo.
- Redact private content in your quotes with a visible marker (`[REDACTED: internal hostname]`), not a silent deletion.
- If an excerpt can't be sanitized without destroying its meaning, re-capture on a throwaway repo.

## Part II: Annotate the System Prompt (25 pts)

Break the `system` block and any messages with `role: "system"` into their sections. For each, answer: **what behavior is this buying, and what failure mode is it defending against?** An annotation, not a summary.

Cover at least:

- **Structure**: the major sections, their order, and why that order.
- **Tone and verbosity**: the specific language controlling response length and format, and why it is worth the tokens.
- **When not to act**: destructive-operation gates, scope limits, refusal conditions.
- **Environment context**: what the agent is told about the machine, repo, and session, and where that lives in the request.

Then, on `<system-reminder>` specifically: where do they appear (system block, messages, or both, citing an example), what two distinct purposes can you evidence, and why inject them mid-conversation rather than stating them once up front?

## Part III: Annotate the Tool Design (25 pts)

**Inventory: numbers, not prose.** How many tools were available, broken down by built-in vs. MCP-provided vs. deferred/searchable? Note any change in the tool set across requests and what triggered it. A good answer reads *"117 tools in the first request: 35 built-in, 82 from three MCP servers"*, not *"there were many tools available."*

**Design analysis.** Pick **two** tools and analyze each as interface design:

- Reproduce the relevant part of the schema.
- Why this parameter set? What is required, what is optional, what is deliberately not exposed?
- What is the description defending against? Tool descriptions in a mature agent are largely accumulated scar tissue. Find a sentence that exists only because a model kept doing the wrong thing, and name that wrong thing.
- What does the tool deliberately *not* do, and what does that imply about the surrounding system?

Pick two tools that differ. Two file-manipulation tools is a weak selection; a file tool paired with an orchestration tool or one with an unusual failure contract is a strong one.

## Part IV: Behavioral Analysis with Evidence (25 pts)

Answer each question from your own trace. Every answer must **cite its evidence** (which request, message index, tool call) and **label itself `[OBSERVED]` or `[INFERRED]`**: observed means you can point at it in your capture, inferred means you are reasoning from definitions without having watched it happen. Both are acceptable; mislabeling is not, and unlabeled answers earn no credit.

- **Error recovery**: walk one failure end to end. What did the agent see, what did it try next, how many turns did recovery take? Quote verbatim.
- **Planning**: a tool, a prompt instruction, emergent behavior, or a combination? What evidence separates those?
- **Plans and task state**: how does one get created and advanced? What does the model see about task state each turn, and where does it live in the request?
- **Subagents**: when does the agent delegate? What does the subagent get told, and what comes back? (An honest `[INFERRED]` is fine if your session never triggered one.)
- **Context management**: as the session grows, what changes in the payloads? How are earlier turns represented later?

## Part V: Reflection (10 pts)

At most one page: **two decisions you would copy** and the problem each solves; **one you would make differently**, engaging with why it might be there; and **one thing the trace changed** about how you will steer a coding agent day to day.

## Deliverables

A completed **`week1/writeup.md`** with every `TODO` filled in. Your captured traces stay on your machine.

## Evaluation Rubric (100 pts total)

| Part | Points | What earns full credit |
|---|---|---|
| I. Capture & reproducibility | 15 | All four session requirements met; setup and session documented well enough to reproduce from your writeup alone |
| II. System prompt annotation | 25 | Sections tied to behavior and failure modes; `<system-reminder>` explained with cited examples |
| III. Tool inventory & design | 25 | Concrete counts with a breakdown; two genuinely different tools analyzed as interface design |
| IV. Behavioral analysis | 25 | Every answer cited and correctly labeled; error recovery quoted verbatim |
| V. Reflection | 10 | Specific, argued positions rather than restatement |

Deductions for unsanitized credentials in quoted excerpts, and for claims presented as observation that your trace does not support.

## SUBMISSION INSTRUCTIONS

1. Make sure you have all changes pushed to your remote repository for grading.
2. **Make sure you've added `mihail911`, `isaackann`, and `vdaita` as collaborators on your assignment repository.**
3. Submit via Gradescope.
4. **Don't forget to remove `ANTHROPIC_BASE_URL` from your repo's `.claude/settings.json`!**
