---
name: repack
description: Use when a running session's pack is wrong for the work actually happening — missing a skill or MCP server it needs, or carrying dead weight from an earlier phase. Symptoms: "I don't have the right skill for this", a long session that has drifted, wanting to shed an unused half of the harness, "repack", "reconfigure this session".
metadata:
  version: "0.1.0"
---

# repack

## Overview
kogitsune makes you choose the pack **before** the session starts, from a one-line task
description — a guess made at the moment you know least about the task. `repack`
re-derives the optimal pack for what is *actually* happening and relaunches into it.

Shedding is first-class. A proposal that only ever adds is what produces the heavy
session kogitsune exists to prevent.

## When to Use
- The task needs a skill or MCP server that was not packed
- A long session has drifted and half the pack is now dead weight
- The model is wrong for the phase (cheap exploration done, hard work starting)

## When NOT to Use
- Mid-edit, or with work you would lose — a repack **restarts the session**
- For MCP alone: `kitsune` mounts servers on demand with no restart. Use it instead.

## Constraints (why this restarts)
| Layer | Changes mid-session? |
|---|---|
| Skills — add | Yes, ~1 turn lag |
| Skills — edit in place | No (body is cached from first scan) |
| MCP | Yes (`kitsune`) |
| Model, `CLAUDE.md`, hooks | No — fixed at process start |

Skill hot-add works but is deliberately unused: a restart is required anyway for
model / `CLAUDE.md` / hooks, and taking it uniformly avoids both the one-turn lag and
the stale-body trap. See `docs/SPEC-2026-07-30-repack.md`.

## Procedure

### 0. Resolve kogitsune
This skill is published to `~/.claude/skills/` and runs from whatever directory the
session is working in, so nothing here may assume a repo-relative path. `kit` is on
PATH and points into the repo:
```bash
KOG_ROOT="$(cd "$(dirname "$(readlink "$(command -v kit)" 2>/dev/null || command -v kit)")/.." && pwd)"
DECIDER="$KOG_ROOT/skills/lib/decider.sh"
WORK="$(mktemp -d "${TMPDIR:-/tmp}/repack.XXXXXX")"   # throwaway manifests
```
If `kit` is not on PATH, stop — the relaunch this skill produces would not run either.

### 1. Read the current pack
```bash
echo "kit=${KOGITSUNE_KIT:-<à la carte>} model=${KOGITSUNE_PACK_MODEL:-<default>}"
echo "skills=${KOGITSUNE_PACK_SKILLS:-}"
echo "mcp=${KOGITSUNE_PACK_MCP:-}"
```
All four unset means the session was **not** launched by `kit`. Say so and stop — there
is no pack to diff against, and inventing one produces a bogus decision label.

### 2. Read the need
Signals come from the conversation: what the work has actually been about, what was
reached for and found missing, what has gone untouched. Add any hint the user passed
(`/repack vue supabase`).

### 3. Derive the target pack
**Hot path first.** The learned router answers known shapes with no model call:
```bash
"$DECIDER" match "<task summary>"
```
Exit 0 prints a kit name — propose it. Exit 1 is the cold path.

**Cold path.** Read the menu and compose:
```bash
"$DECIDER" latest context                          # the scout's snapshot, if any
cat "${KOGITSUNE_CONFIG:-$KOG_ROOT/kits.yaml}"     # named kits + catalog, with weights
cat "$KOG_ROOT/docs/ecc-skills-descriptions.tsv"   # ~277 skills, name + one-liner
```
Reason over these in-context. Fall back to a haiku one-shot (`kit for "<task>"`) only if
in-context matching is genuinely inconclusive.

Name what to **shed** as explicitly as what to add. Anything packed that the work has not
touched and is not about to is a candidate.

### 4. Render the diff
Rebuild the current pack à la carte from the exported lists — this works whether the
session was launched from a named kit or composed by hand, and is symmetric with how the
target is built:
```bash
python3 "$KOG_ROOT/lib/build-config.py" --dry-run \
  --skills "$KOGITSUNE_PACK_SKILLS" --mcp "$KOGITSUNE_PACK_MCP" \
  --model "$KOGITSUNE_PACK_MODEL" > "$WORK/cur.json"
python3 "$KOG_ROOT/lib/build-config.py" --dry-run \
  --skills "<target skills>" --mcp "<target mcp>" \
  --model "<target model>" > "$WORK/tgt.json"
python3 "$KOG_ROOT/lib/pack-diff.py" --current "$WORK/cur.json" --target "$WORK/tgt.json"
```
Both calls need `--config "${KOGITSUNE_CONFIG:-$KOG_ROOT/kits.yaml}"` when the working
directory is not the kogitsune repo.

If the diff is a no-op, say the pack is already right and stop. Do not manufacture churn
to look useful.

### 5. Confirm
Show the diff and ask. **Nothing is written before the user answers.**
```
repack: <one line on what the task looks like>

  + <additions>
  - <sheds>
  model: <from> -> <to>

  net <delta>   ·   <current> -> <target>

restart to apply? [y/N]
```

### 6. On confirm — write the handoff, save, print the command
Write `.kogitsune/handoff.md` in the working directory: where the work stands, what is
done, what is next, and any decision the user has already made that the next session must
not re-litigate. Short and concrete — claude-mem carries the broader history; this covers
the last mile. Mention adding `.kogitsune/` to that project's `.gitignore` if it is a git
repo that lacks the entry.

```bash
kit save _repack --skills "<target skills>" --mcp "<target mcp>" --model "<target model>"
```
Then **print** this for the user to run — do not execute it:
```bash
kit _repack -- "$(cat .kogitsune/handoff.md)"
```
`_repack` is reserved scratch and is overwritten on every repack. To keep a derived pack,
the user runs `kit save <realname> …` themselves.

### 7. Log the decision
```bash
"$DECIDER" append-decision '{
  "ts": "<ISO-8601 UTC>",
  "decider": "skill:repack",
  "task": "<task summary>",
  "decision": {"kit": "_repack", "model": "<m>", "mcp": [], "skills": [],
               "launch": "kit _repack"},
  "signals": ["<canonical signals>"],
  "rationale": "<one line>",
  "confidence": 0.0,
  "source": "repack",
  "alternatives": [{"kit": "<runner-up>", "why_not": "<why>"}]
}'
```
Set `confidence` honestly — it is the vote, not decoration (`decisions/SCHEMA.md`).
`source: "repack"` is what earns the label its extra weight in `distill`; omitting it
silently downgrades it to an ordinary up-front guess.

Then clean up: `rm -rf "$WORK"`.

Periodically: `"$DECIDER" distill` folds new labels into a fresh router.

## Anti-patterns
- **Add-only proposals.** If nothing is shed, justify why in one line or look harder.
- **Repacking to seem useful.** A no-op diff is a good outcome; report it and stop.
- **Auto-running the relaunch.** Print it. The user decides when the session dies.
- **Skipping the handoff.** The new session starts cold without it.
- **Logging without `source`.** Throws away the reason the label is worth more.
