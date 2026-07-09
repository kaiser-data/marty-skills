# SKILL.md frontmatter — exact schema

Two layers: the **portable core** (Agent Skills spec, agentskills.io — what Anthropic's own `quick_validate.py` enforces) and **Claude Code extensions** (valid in Claude Code, ignored or rejected elsewhere).

## Portable core (validate strictly)

| Field | Required | Constraints |
|---|---|---|
| `name` | yes | 1–64 chars; `^[a-z0-9-]+$`; no leading/trailing/double hyphens; **must match the directory name**; no "anthropic"/"claude"; no XML tags |
| `description` | yes | 1–1024 chars; no `<` or `>`; states what it does AND when to use it |
| `license` | no | short license name or reference to a bundled file |
| `compatibility` | no | ≤500 chars; environment requirements — most skills should omit it |
| `metadata` | no | string→string map for anything else (author, version, …) |
| `allowed-tools` | no | space-separated string, e.g. `Bash(git:*) Read` (experimental in the spec) |

Anything outside this set is an error under the spec. Anthropic's validator: `quick_validate.py` in [anthropics/skills](https://github.com/anthropics/skills) `skills/skill-creator/scripts/`.

## Claude Code extensions (warn: not portable)

All fields optional in Claude Code; `name` there is just a display label and defaults to the directory name.

- `when_to_use` — extra trigger context, appended to the description in the skill listing (combined text truncated at 1,536 chars)
- `argument-hint`, `arguments` — slash-command argument UX and `$name` substitution
- `disable-model-invocation` (bool) — user-only; removes the description from Claude's context
- `user-invocable` (bool, default true) — `false` hides it from the `/` menu
- `disallowed-tools`, `model`, `effort` — per-skill overrides
- `context: fork` + `agent` — run the skill in a subagent
- `hooks`, `paths`, `shell` — lifecycle hooks, activation globs, dynamic-context shell

Body substitutions available in Claude Code: `$ARGUMENTS`, `$1`/`$ARGUMENTS[N]`, `${CLAUDE_SKILL_DIR}`, `${CLAUDE_PROJECT_DIR}`, `${CLAUDE_SESSION_ID}`, and `` !`command` `` dynamic context.

## Directory layout

```
skill-name/
├── SKILL.md        # required; keep body <500 lines / <5k words
├── scripts/        # executed, never loaded into context
├── references/     # loaded on demand; give files >100 lines a TOC
├── assets/         # templates, images, data
└── evals/          # {query, should_trigger} test cases; excluded from packaging
```

Progressive disclosure: metadata (~100 tokens, always loaded) → body (loaded on trigger) → bundled files (zero cost until read). Keep references one hop from SKILL.md.

## Skill locations & precedence (Claude Code)

`~/.claude/skills/` (personal) · `.claude/skills/` (project) · plugin skills (`plugin:skill`). Enterprise > personal > project on name conflict — which is why the forge checks cross-skill collisions.

Sources: [agentskills.io/specification](https://agentskills.io/specification) · [code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills) · [platform.claude.com best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
