---
name: kit-builder
description: Use when a selected config must be assembled into a runnable kogitsune collection or launch command, when materializing a new named kit in kits.yaml, or after kit-selector produces a decision that needs to become an actual kit to run.
metadata:
  version: "0.1.0"
---

# kit-builder

## Overview
Takes a `kit-selector` decision and **assembles the collection**: either a launch
command for an existing kit or a new named kit entry (model + MCP + skills) in the
catalog. It then records whether the build worked, so future builds learn which
compositions hold up. Builds *what the selector selected*.

## When to Use
- A selector decision needs to become a real launch (`kit <name> -- "<task>"`)
- A recurring composition deserves promotion to a named kit in `kits.yaml`
- Capturing build success/failure to feed the learning loop

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
1. Read the decision (from `decisions.jsonl` or passed inline).
2. If it maps to an existing kit → emit the launch command. If it's a novel composition
   → assemble a `kits.yaml` entry (`model`, `mcp`, `skills`) and validate it resolves
   (`kit show <name>` / dry-run).
3. Record the outcome: `"$DECIDER" append-build '<json>'` with `from_decision`, `built`,
   `success`, `notes` (see `decisions/SCHEMA.md`).

## Improve with experience
`builds.jsonl` records which built configs actually launched/worked. Recurring successful
compositions are promotion candidates (make them named kits); repeated failures are a
signal to the selector to stop choosing them. Over time the builder favors proven builds.

## Versioning
- Skill: frontmatter `version:`.
- Outcomes: append-only `decisions/builds.jsonl` (ids `B001`…); promoted kits are versioned
  by git history of `kits.yaml`; current counts in `decisions/VERSIONS.md`.

## Common Mistakes
- Building without validating the config resolves — verify before recording success.
- Not recording failures — the loop only learns if losses are logged too.
- Silently inventing a kit not grounded in the selector's decision — build what was selected.
