# Skill authoring best practices

Distilled from Anthropic's skill-creator, the platform best-practices guide, and community linters (skill-lint, cclint, agent-skills-lint).

## Descriptions — the only thing that decides triggering

Claude picks a skill from 100+ candidates by description alone. The formula:

> `<What it does — concrete verbs and objects>. Use when <user phrases, file types, task contexts>.`

Rules:
1. **Third person, always.** The description is injected into the system prompt. "Processes Excel files and generates reports" — never "I can help you…".
2. **Two halves: what + when.** A description without trigger conditions undertriggers.
3. **Name the actual words users say** — file extensions, tool names, verbs. "Use when the user mentions PDFs, forms, or document extraction."
4. **Be a little pushy.** Undertriggering is the common failure; overtriggering is rare and easy to fix.
5. **Key use case first** — listings get truncated under context budgets.
6. Never vague ("Helps with documents", "Processes data").
7. Too eager? Narrow the triggers or set `disable-model-invocation: true`.

Test empirically: keep `evals/evals.json` with should-trigger AND should-not-trigger queries; when a skill fails to fire in real use, add the missed phrasing to the description.

## Body writing

- **Claude is already smart** — challenge every token. Instructions, not education.
- Imperative voice ("Run X", "Ask the user Y"), consistent terminology throughout.
- Match freedom to fragility: exact commands/scripts for fragile operations, heuristics for open-ended ones.
- Be explicit about intent for each bundled file: "run `scripts/x.py`" vs "read `references/y.md`".
- Checklists for multi-step workflows; validator→fix→repeat loops where a validator exists.
- No time-sensitive content ("new in v2", dates). It rots silently.
- <500 lines / <5k words. Overflow goes to `references/`.

## Naming

Kebab-case gerund or noun phrase: `processing-pdfs`, `skill-forge`. Never `helper`, `utils`, generic names, or the reserved words `claude`/`anthropic`.

## Keeping skills fresh (the update loop)

Skills are living documents. On a cadence (the dashboard's stale marker = 90 days):

1. Re-validate; fix new warnings.
2. Replay recent real usage against the description — add missed triggers, remove false ones.
3. Prune the body; move grown sections to `references/`.
4. Update for API/tool changes since last touch.
5. Bump `metadata.version`; commit with a message describing what changed and why.

## Safety (before installing third-party skills)

A coordinated malware campaign has already hit the skills ecosystem. Before trusting any downloaded skill, run `forge.py validate <dir>` — it scans bundled scripts for `curl | sh`, destructive `rm -rf` on `/` or `~`, `sudo`, `chmod 777`, and base64-decoded execution — and read what the scripts actually do.
