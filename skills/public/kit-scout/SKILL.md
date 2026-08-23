---
name: kit-scout
description: Use when the available superpowers/ECC skills, agents, or kogitsune kits may have changed, when the selector's context looks stale, or before a selection whose catalog snapshot is missing or outdated (catalog_hash mismatch).
metadata:
  version: "0.1.0"
---

# kit-scout

## Overview
Surveys everything the environment offers — **superpowers** (process methodology),
**ECC** (domain capability + language reviewers), and the **kogitsune kit catalog** —
and emits a compact, versioned **context snapshot** that `kit-selector` consumes. Scout
knows *what exists*; it does not choose. Core principle: the selector should never guess
the menu — hand it a fresh, structured one.

## When to Use
- Superpowers or ECC plugins updated, or new skills/agents installed
- `kit ls` / `kits.yaml` changed (catalog_hash differs from latest context)
- A selection is about to run but the latest context is empty or stale

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
1. Enumerate sources: `kit ls`, the superpowers skill list, the ECC agent/skill list.
2. Group by role — superpowers = *methodology*, ECC = *capability/reviewers*, kits = *presets*.
3. Note the pinned-always layer (guardrails, memory, graphify) so the selector ignores it.
4. Persist: `"$DECIDER" write-context '<json>'` → writes `context.v<N>.json`,
   auto-incrementing the version. Include `catalog_hash` (fingerprint of kits.yaml + kit list).

## Improve with experience
Each run is a new versioned snapshot — history is never overwritten. When the catalog
churns, re-scout; the selector always reads `"$DECIDER" latest context`. Diffing two
context versions shows what capability entered/left the environment.

## Versioning
- Skill: semver in frontmatter (`version:`).
- Output: `decisions/context/context.v<N>.json`; current N tracked in `decisions/VERSIONS.md`.

## Common Mistakes
- Choosing a kit here — that's `kit-selector`'s job. Scout only reports.
- Dumping raw plugin blurbs — compress to role-grouped names; the selector pays per token.
- Forgetting `catalog_hash` — without it the selector can't detect staleness.
