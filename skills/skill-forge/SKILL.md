---
name: skill-forge
description: "Scaffold, validate, improve, package, and dashboard Claude Code skills. Use when creating a new skill, auditing or fixing existing skills, writing SKILL.md frontmatter or descriptions, packaging a skill for sharing, or generating the skill dashboard. Use whenever the user mentions skill quality, skill triggering problems, or keeping skills up to date."
license: MIT
metadata:
  author: kaiser-data
  version: "0.1.0"
---

# Skill Forge

A toolkit for the full lifecycle of Claude Code skills: create → validate → eval → package → keep fresh. All mechanics live in `scripts/forge.py` (stdlib-only Python) — run it, don't re-implement it.

```
python3 ${CLAUDE_SKILL_DIR}/scripts/forge.py <command>
  new <name>            scaffold a skill (SKILL.md, references/, scripts/, evals/)
  validate [PATH ...]   lint all discovered skills, or specific paths; exit 1 on errors
  list [--json]         table of every personal + project skill
  dashboard [--open]    regenerate dashboard/index.html
  package <PATH>        validate, then zip to dist/<name>.skill (official format)
```

## Creating a new skill

1. **Interview before writing.** Ask what the skill does, what user phrases should trigger it, and what should NOT trigger it. A skill without crisp triggers will undertrigger — that is the most common failure.
2. Scaffold: `forge.py new <name>` (kebab-case, ≤64 chars, no "claude"/"anthropic").
3. Write the description first — it is the only thing Claude sees when deciding to trigger. Formula: `<What it does, concrete verbs>. Use when <trigger phrases, file types, contexts>.` Third person, be a little pushy, key use case first. See `references/best-practices.md`.
4. Write the body: imperative voice, under 500 lines. Anything longer moves to `references/` (loaded on demand) or `scripts/` (executed, never loaded). One level of file references deep, no chains.
5. Fill `evals/evals.json` with 3+ should-trigger and should-not-trigger queries.
6. `forge.py validate <dir>` and fix everything it reports.

## Improving an existing skill (do this often — skills are living documents)

Skills rot: APIs change, better patterns emerge, descriptions undertrigger. When asked to improve/update/audit a skill:

1. `forge.py validate <dir>` — fix errors, then warnings.
2. Audit the description against real usage: did the skill fail to trigger recently? Add the missed phrases as triggers. Did it trigger wrongly? Make it more specific.
3. Shrink the body: challenge every paragraph — "does Claude actually need to be told this?" Move reference material to `references/`.
4. Check for time-sensitive content (versions, dates, "new in …") and remove or generalize it.
5. Bump `metadata.version`, note the change in the commit message, and regenerate the dashboard.

The dashboard's freshness dots (fresh <30d / aging <90d / stale >90d) show which skills are overdue for this pass.

## Validation tiers

`forge.py validate` enforces the Agent Skills spec strictly (field whitelist, name/description limits — see `references/frontmatter-spec.md`) and warns on: Claude Code extension fields (portability), missing trigger cues, first-person descriptions, oversized bodies, broken file references, leftover TODO/placeholder markers, cross-skill name collisions, and dangerous commands in bundled scripts (`curl | sh`, `rm -rf /`, `sudo` — real skill malware exists, so review third-party skills before installing).

## Dashboard

`forge.py dashboard` scans `~/.claude/skills` plus this repo's `skills/` and writes a self-contained `docs/index.html`: health tiles, per-skill cards with validation issues, body size, and staleness. Regenerate it after any skill change; it is committed so GitHub Pages serves it from `docs/`.

## References

- `references/frontmatter-spec.md` — exact frontmatter schema: spec core vs Claude Code extensions, all limits.
- `references/best-practices.md` — description formula, progressive disclosure, body-writing rules, update checklist.
