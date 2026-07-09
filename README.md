# marty-skills

**My own customized Claude Code skills only** — built and maintained with **skill-forge**, a skill that forges skills. Third-party/community skills (n8n suite, graphify, cognee, …) live separately in `~/.claude/skills` and are deliberately NOT tracked here: they are upstream-maintained and never modified locally.

**[📊 Live dashboard](https://kaiser-data.github.io/marty-skills/)** — health, validation issues, and staleness for my skills. (`forge.py dashboard --installed` gives a local view that includes third-party skills.)

## skill-forge

The full lifecycle of a Claude Code skill in one stdlib-only CLI (`skills/skill-forge/scripts/forge.py`):

| Command | What it does |
|---|---|
| `new <name>` | Scaffold SKILL.md + `references/` + `scripts/` + `evals/` |
| `validate` | Lint this repo's skills against the Agent Skills spec (`--installed` adds third-party, read-only) |
| `list` | One-line status table of this repo's skills |
| `dashboard` | Regenerate the self-contained HTML dashboard (`docs/index.html`) |
| `package <dir>` | Validate, then zip to `dist/<name>.skill` (official format) |

```bash
python3 skills/skill-forge/scripts/forge.py validate
python3 skills/skill-forge/scripts/forge.py dashboard --open
```

### What `validate` checks

- **Spec tier (errors):** frontmatter present; field whitelist (`name, description, license, allowed-tools, metadata, compatibility`); name ≤64 chars, kebab-case, matches directory; description 1–1024 chars, no angle brackets.
- **Quality tier (warnings):** missing "use when" trigger cues, first-person descriptions, bodies over 500 lines / 5,000 words, broken file references, leftover TODO/placeholder markers, Claude Code-only frontmatter fields (portability), cross-skill name collisions.
- **Safety tier (warnings):** bundled scripts containing `curl | sh`, destructive `rm -rf`, `sudo`, `chmod 777`, or base64-decoded execution — review any third-party skill before installing it.

### Install as a personal skill

```bash
ln -s "$(pwd)/skills/skill-forge" ~/.claude/skills/skill-forge
```

Then in any Claude Code session: *"validate my skills"*, *"create a new skill for X"*, *"regenerate the skill dashboard"*.

## tailscale-endpoints

Endpoint catalogue and recipes for calling self-hosted APIs across the tailnet — primarily the [Jetson voice AI box](https://github.com/kaiser-data/jetson-headless-inference) (Ollama LLM, voice pipeline, Piper TTS, control API): MagicDNS addressing, auth, streaming-vs-speaker output, timeout guidance, and the debugging path for unreachable services.

## Using these skills from other agents (OpenClaw, etc.)

Every skill here sticks to the **portable core** of the [Agent Skills spec](https://agentskills.io/specification) — no Claude Code-only frontmatter — so any agent that reads `SKILL.md` folders can use them:

```bash
# Claude Code (personal skill)
ln -s "$(pwd)/skills/tailscale-endpoints" ~/.claude/skills/tailscale-endpoints

# OpenClaw
ln -s "$(pwd)/skills/tailscale-endpoints" ~/.openclaw/skills/tailscale-endpoints

# Any other Agent Skills-compatible runtime: point it at skills/<name>/,
# or ship the packaged zip:  python3 skills/skill-forge/scripts/forge.py package skills/<name>
```

`forge.py validate` warns on non-portable frontmatter, so portability is enforced, not just intended.

## Philosophy: skills are living documents

Skills rot — APIs change, descriptions undertrigger, bodies bloat. The dashboard tracks freshness (fresh <30d / aging <90d / stale >90d), and skill-forge's SKILL.md includes a dedicated *"Improving an existing skill"* workflow. Stale skills get an update pass, not a pass.

Built on the [Agent Skills spec](https://agentskills.io/specification), Anthropic's [skill-creator](https://github.com/anthropics/skills), and conventions from skill-lint, cclint, and agent-skills-lint.
