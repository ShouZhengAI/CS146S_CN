# Week 1 Write-up

## Part I: Capture

**Setup** (enough for a reader to reproduce your capture):
```
claude --version:  TODO
mitmproxy version: TODO
proxy command:     TODO
settings file:     TODO (path + env block)
```

**The session.** What task, against what repo, and how many `POST /v1/messages` requests did it produce?
> TODO

| Requirement | Evidence |
|---|---|
| Touched ≥ 2 files | TODO |
| Failed at least once | TODO |
| Long enough to plan | TODO |
| Your own repo | TODO |

**What you redacted** from the excerpts quoted below, and why:
> TODO


## Part II: System Prompt Annotation

**a. Structure.** Major sections in order, one line each on what it does, and why this order.
> TODO

**b. Tone and verbosity.** Quote the controlling instructions, then say what failure mode they defend against.
```
TODO
```
> TODO

**c. When not to act.** Quote the destructive-operation gates, scope limits, or refusal conditions, and what each buys.
```
TODO
```
> TODO

**d. Environment context.** What the agent is told about machine/repo/session, and where it lives in the request (`system` field or a `role: "system"` message).
> TODO

**e. `<system-reminder>`.** Where they appear (cite an example), two distinct purposes you can evidence, and why they are injected mid-conversation rather than stated once.
```
TODO
```
> TODO


## Part III: Tool Design Annotation

**Inventory.** Did the set change across requests? If so, what triggered it?

| Built-in | MCP | Deferred | **Total** | Changed mid-session? |
|---|---|---|---|---|
| TODO | TODO | TODO | **TODO** | TODO |

**Two tools.** Pick tools that differ from each other.

| | Tool 1 | Tool 2 |
|---|---|---|
| Name | TODO | TODO |
| Key schema fields | TODO | TODO |
| Required vs. optional vs. not exposed, and why | TODO | TODO |
| Description is defending against… (quote + the wrong behavior) | TODO | TODO |
| Deliberately does *not* do… and what that implies | TODO | TODO |

Why these two?
> TODO


## Part IV: Behavioral Analysis

**Every answer must be labeled `[OBSERVED]` or `[INFERRED]` and cite its evidence. Unlabeled answers earn no credit.**

**a. Error recovery**: `TODO: label` · evidence: `TODO`

What the agent saw, verbatim:
```
TODO
```
What it tried next, and turns to recover:
> TODO

**b. Planning**: `TODO: label` · evidence: `TODO`
> TODO

**c. Plans and task state**: `TODO: label` · evidence: `TODO` \
How does one get created and advanced? What does the model see about task state each turn, and where does it live in the request:
> TODO

**d. Subagents**: `TODO: label` · evidence: `TODO` \
When the agent delegates, what the subagent is told, and what comes back:
> TODO

**e. Context management**: `TODO: label` · evidence: `TODO` \
What changed in the payloads as the session grew:
> TODO


## Part V: Reflection

**Two decisions you would copy**, and the problem each solves:
1. TODO
2. TODO

**One you would make differently** (engage with why it might be there):
> TODO

**One thing the trace changed** about how you will steer a coding agent:
> TODO


## Submission
1. `Command (⌘) + F` for `TODO`. No results means you're done.
2. Confirm no credentials or `x-api-key` headers made it into your quoted excerpts.
3. Push all changes to your remote repository and submit via Gradescope.
4. Don't forget to remove `ANTHROPIC_BASE_URL` from your repo's `.claude/settings.json`!
