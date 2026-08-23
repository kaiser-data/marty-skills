---
name: kit-selector
description: Use when a task needs a kogitsune config/kit chosen before launch, when routing work to the leanest capable harness, or when deciding which model + MCP + skills a task warrants. Symptoms: "which kit for this?", unsure lean vs build, avoiding a full-harness model call for an obvious task.
metadata:
  version: "0.2.0"
---

# kit-selector

## Overview
Turns a task into a config decision using the **learned router first, model last**.
It reads the scout's context (the menu) and the distilled router (past experience),
answers instantly when a task matches a learned pattern, and only reasons from scratch
when it doesn't. Every decision is logged as a gold label so the router keeps improving.
Selects *for* `kit-builder`.

## When to Use
- Any "which kit / config should this task use?" moment
- Before `kit <name> -- "<task>"`, to justify the pick
- When you want to avoid a slow full-harness model classification for an obvious task

## Resolve the datastore first
This skill is published to `~/.claude/skills/` and runs from whatever directory the
session is in, so `decider` is **not** on PATH and no repo-relative path is safe. `kit`
is on PATH and points into the repo — resolve through it:
```bash
KOG_ROOT="$(cd "$(dirname "$(readlink "$(command -v kit)" 2>/dev/null || command -v kit)")/.." && pwd)"
DECIDER="$KOG_ROOT/skills/lib/decider.sh"
```
If `kit` is not on PATH, say so and stop rather than guessing a location.

## How it works
1. Load inputs: `"$DECIDER" latest context` (menu) and `"$DECIDER" latest router` (learned rules).
2. **Hot path** — `"$DECIDER" match "<task>"` prints the best kit and exits 0. It normalizes
   the task to canonical signals and takes the rule with the most overlap (ties break on
   **weight** — summed confidence — then support, then kit name, so the same task always
   routes the same way). No model call.
3. **Cold path** — `match` exits 1: nothing overlapped. Reason over the context to compose
   the config (kit *or* à-la-carte model+MCP+skills). This is the teacher step.
4. Log it: `"$DECIDER" append-decision '<json>'` with `task`, `decision`, **`signals`**,
   `rationale`, `confidence`, `alternatives` (see `decisions/SCHEMA.md`).
5. Periodically `"$DECIDER" distill` → bumps `router.v<N+1>.json` from all decisions.

## Canonical signals
The router can only aggregate what it can compare, so `distill` folds every signal onto a
fixed vocabulary (`"$DECIDER" normalize "<text>"` shows it for any text):

`auth` · `security` · `testing` · `docs` · `performance` · `refactor` · `bugfix` ·
`feature` · `multi-file` · `single-file` · `trivial` · `python` · `typescript` · `go` ·
`rust` · `shell`

Write signals however reads clearly — `"auth/security-sensitive"` folds to `auth`+`security`,
`"explicit tests -> TDD"` to `testing`. You are *describing*, not matching; normalization is
what makes two differently-worded decisions reinforce the same rule. Decisions that never
name a launchable kit (`custom`, or `launch: "n/a…"`) are excluded from the router.

## Improve with experience
`signals → decision` pairs accumulate in `decisions.jsonl`; `distill` compiles them into
the next router version. More logged decisions ⇒ more tasks answered on the hot path ⇒
fewer model calls. `alternatives` supply contrastive negatives for future learning.

`kit for "<task>"` runs this same loop from the shell: router first, haiku only on a miss,
and it logs **cold-path picks only** — recording what the router already knew would just
inflate that rule's own support count.

## Versioning
- Skill: frontmatter `version:`.
- Learned artifact: `decisions/router.v<N>.json`; current N in `decisions/VERSIONS.md`.

## Common Mistakes
- Skipping the router and always reasoning — defeats the speed-up. Check the hot path first.
- Logging without `signals` — the router can only learn from signals; a decision without
  them is a dead record.
- Picking a heavy kit for a trivial task — prefer the leanest capable config.
