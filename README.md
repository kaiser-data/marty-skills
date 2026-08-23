# marty-skills

**My own customized Claude Code skills only** — built and maintained with **skill-forge**, a skill that forges skills. Third-party/community skills (n8n suite, graphify, cognee, …) live separately in `~/.claude/skills` and are deliberately NOT tracked here: they are upstream-maintained and never modified locally.

**[📊 Live dashboard](https://kaiser-data.github.io/marty-skills/)** — health, validation issues, and staleness for my skills. (`forge.py dashboard --installed` gives a local view that includes third-party skills.)

## Layout: public here, personal elsewhere

Everything in this repo lives under **`skills/public/`** — skills that are useful to anyone and contain nothing about my setup. Skills bound to my own hardware, network, or private repos live in a **separate private repo**: they carry real hostnames, IPs and usernames, or drive tooling nobody else can install, so a sanitized public version would not run anyway.

The rule for new skills:

- Contains a hostname, an IP, a username, or a path from my setup → **private repo**.
- Drives a **private** repo or app of mine → **private repo** (the public version would not run).
- Everything else → `skills/public/` (where `forge.py new` scaffolds by default).

A skill that only *mentions* a public project of mine (`kitsune-mcp`, `kogitsune`, `claude-A2A-Comm`, `github-stars-analyzer`) stays public — but any setup-specific path in it gets replaced with a placeholder first.

## The skills

### Research & evaluation methodology

Written from a real eval sprint, each with an append-only `FIELD-NOTES.md` that records every firing — the mechanism `skills-that-learn` prescribes.

| Skill | Guards against |
|---|---|
| `systematic-study` | Study grids whose columns differ in more than one way; factors with one realized level; missing baselines |
| `seed-replicates-before-effects` | Effect claims from n=1 cells, with no noise floor measured |
| `detection-needs-a-denominator` | Detectors reported without clean negatives, a false-positive rate, or an eyeballed threshold |
| `harness-neutrality-check` | Reading a null result as "the model doesn't do it" when it is the harness, template, or sampling settings |
| `leading-premise-controls` | Probes that presuppose what they measure; treating fluent self-report as evidence |
| `pairwise-comparison-design` | Forced-choice instruments that cannot measure their own construct; scores compared across separate fits |
| `numbers-from-primary-sources` | A number entering a write-up from an abstract, a summary, or last session's notes |
| `citing-what-you-used` | Methods, instruments, and figures whose provenance a reader cannot trace |
| `modal-gpu-sweeps` | Rented-GPU sweeps that die on a typo after paying for warm-up, or cannot resume |
| `skills-that-learn` | Skills that never improve because their firings are never logged |

### Writing, publishing & compliance

| Skill | What it does |
|---|---|
| `front-loading-findings` | Cuts a long document to a hard limit for a reader who stops on page two |
| `announcing-events` | Event announcement posts — speakers, agenda, venue, registration link |
| `updating-editorial-plan` | Keeps an editorial calendar honest when slots slip and the backlog grows |
| `linkedin-unicode-styling` | Unicode bold/headers/small caps for social posts, without breaking @-mentions |
| `triaging-new-material` | Reading order and context budget when a pile of new source material arrives |
| `ai-act-transparency` | EU AI Act Art. 50 disclosure audit for anything that speaks, writes, or summarises for a user |
| `html-email` | Bulletproof HTML email across Outlook/Gmail/Apple Mail |
| `email-deliverability` | Spam placement, bounces, sender reputation, pre-send checks in any ESP |

### Code & build guardrails

| Skill | What it does |
|---|---|
| `mock-purge` | Finds simulated parts before a prototype gets trusted or handed over |
| `agnostic-audit` | Post-build audit for implementations overfitted to their one example source |
| `variance-first` | Pre-build gate: name the axes of variance before writing the implementation |

### Harness & tooling

| Skill | What it does |
|---|---|
| `skill-forge` | The full skill lifecycle: create → validate → package → dashboard |
| `kitsune-gateway` | Mount any of 130k+ MCP servers on demand through [Kitsune MCP](https://github.com/kaiser-data/kitsune-mcp) |
| `kitsune-dev` | Hot-reload loop for developing your own MCP server through Kitsune |
| `kitsune-improve` | Turn a raw, low-quality MCP server into a reliably-usable one |
| `kit-selector` | Choose the leanest capable [kogitsune](https://github.com/kaiser-data/kogitsune) kit for a task |
| `kit-scout` | Refresh the kit catalog when skills, agents, or kits have changed |
| `kit-builder` | Assemble a selected config into a runnable kit or launch command |
| `repack` | Reconfigure a running session whose pack no longer fits the work |
| `a2a-messaging` | Cross-machine, cross-vendor agent messaging via [claude-A2A-Comm](https://github.com/kaiser-data/claude-A2A-Comm) — and proving which hub you are on before calling a peer silent |

### Tool selection

| Skill | What it does |
|---|---|
| `choosing-viz-tools` | Picks a charting/dashboard/BI tool from 61 curated options with maintenance signals |

## skill-forge

The full lifecycle of a Claude Code skill in one stdlib-only CLI (`skills/public/skill-forge/scripts/forge.py`):

| Command | What it does |
|---|---|
| `new <name>` | Scaffold SKILL.md + `references/` + `scripts/` + `evals/` |
| `validate` | Lint this repo's skills against the Agent Skills spec (`--installed` adds third-party, read-only) |
| `list` | One-line status table of this repo's skills |
| `dashboard` | Regenerate the self-contained HTML dashboard (`docs/index.html`) |
| `package <dir>` | Validate, then zip to `dist/<name>.skill` (official format) |

```bash
python3 skills/public/skill-forge/scripts/forge.py validate
python3 skills/public/skill-forge/scripts/forge.py dashboard --open
```

### What `validate` checks

- **Spec tier (errors):** frontmatter present; field whitelist (`name, description, license, allowed-tools, metadata, compatibility`); name ≤64 chars, kebab-case, matches directory; description 1–1024 chars, no angle brackets.
- **Quality tier (warnings):** missing "use when" trigger cues, first-person descriptions, bodies over 500 lines / 5,000 words, broken file references, leftover TODO/placeholder markers, Claude Code-only frontmatter fields (portability), cross-skill name collisions.
- **Safety tier (warnings):** bundled scripts containing `curl | sh`, destructive `rm -rf`, `sudo`, `chmod 777`, or base64-decoded execution — review any third-party skill before installing it.

### Install as a personal skill

```bash
ln -s "$(pwd)/skills/public/skill-forge" ~/.claude/skills/skill-forge
```

Then in any Claude Code session: *"validate my skills"*, *"create a new skill for X"*, *"regenerate the skill dashboard"*.

## Using these skills from other agents (OpenClaw, etc.)

Every skill here sticks to the **portable core** of the [Agent Skills spec](https://agentskills.io/specification) — no Claude Code-only frontmatter — so any agent that reads `SKILL.md` folders can use them:

```bash
# Claude Code
ln -s "$(pwd)/skills/public/html-email" ~/.claude/skills/html-email

# OpenClaw
ln -s "$(pwd)/skills/public/html-email" ~/.openclaw/skills/html-email

# Any other Agent Skills-compatible runtime: point it at skills/public/<name>/,
# or ship the packaged zip:  python3 skills/public/skill-forge/scripts/forge.py package skills/public/<name>
```

`forge.py validate` warns on non-portable frontmatter, so portability is enforced, not just intended.

## Philosophy: skills are living documents

Skills rot — APIs change, descriptions undertrigger, bodies bloat. The dashboard tracks freshness (fresh <30d / aging <90d / stale >90d), and skill-forge's SKILL.md includes a dedicated *"Improving an existing skill"* workflow. Stale skills get an update pass, not a pass.

`skills-that-learn` takes this one step further: each skill in the research family keeps an append-only `FIELD-NOTES.md` logging every time it helped, misfired, failed to trigger, or turned out to be wrong. Revisions come from that log, not from memory.

Built on the [Agent Skills spec](https://agentskills.io/specification), Anthropic's [skill-creator](https://github.com/anthropics/skills), and conventions from skill-lint, cclint, and agent-skills-lint.
