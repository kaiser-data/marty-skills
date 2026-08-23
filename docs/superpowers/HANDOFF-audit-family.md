# Handoff — the audit family (agnostic-audit, variance-first)

**Last worked:** 2026-07-31
**State:** shipped, merged to `main`, pushed to `github.com/kaiser-data/marty-skills`
**Commits:** `b23c030` agnostic-audit · `7abff1a` variance-first · `817c6e7` docs/dashboard

---

## What exists now

Three skills form an audit family. They share one anatomy on purpose — classification
table → required inventory with named fields → one load-bearing field → mandatory verdict
→ common mistakes → red flags — so the next audit skill inherits the format instead of
inventing one.

| Skill | Asks | Moment | Load-bearing field |
|---|---|---|---|
| `variance-first` | has the input contract been observed? | before planning | the **Unknown** column |
| `agnostic-audit` | does the built thing generalise? | after building | **Breaks when** |
| `mock-purge` | is the behaviour real? | before it is trusted | **Wrong conclusion** |

All three live in `skills/public/`, are symlinked into `~/.claude/skills/`, and validate
clean (`9 skill(s): 0 error(s), 0 warning(s)`).

**Source documents:**
- Spec: `docs/superpowers/specs/2026-07-31-source-agnostic-skills-design.md`
- Plan: `docs/superpowers/plans/2026-07-31-source-agnostic-skills.md` (contains both
  SKILL.md bodies in full, plus a self-review section)

## The two ideas worth not losing

1. **Agreement across samples is not invariance.** `variance-first` only lets a field count
   as Invariant if a *reason* can be named — a spec, standard, or stated guarantee. Three
   samples agreeing may only mean they came from one producer. Everything else goes to
   Unknown, and **an empty Unknown column means the table was not filled in honestly.**

2. **Prompts are a first-class overfitting surface.** Instructions written while looking at
   one example absorb that example, and no linter, type checker, or test will ever see it.
   It is sweep surface 4 in `agnostic-audit`, marked read-not-grepped, and an audit that
   covers only surfaces 1–3 is required to say so — otherwise a prompt-only overfit passes
   silently, which is the same bug one level up.

## Open items

**1. Trigger contracts are self-assessed, not independently judged.** *(the real gap)*

The plan (Task 1 Step 6, Task 2 Steps 6–7) specifies dispatching one subagent per eval
query, seeing **only** the description — never the body, which leaks intent the real trigger
decision does not have. That was not done: inline execution was chosen and the standing
rule is no Agent tool unless asked. All 21 queries were checked by the same session that
wrote the bodies, so the result is contaminated.

To close it: ~21 cheap subagent calls using the exact prompt shapes in the plan, including
the 20-query **cross-triggering** check that shows both descriptions at once. These two
skills are adjacent, and adjacency is where trigger contracts fail. The boundary being
enforced is **tense**: `variance-first` owns everything before code exists, `agnostic-audit`
everything after.

**2. Detector script — deferred by decision, not uncertainty.**

A `scripts/` sweep could pull literals out of sample files and grep the codebase for them.
Rejected for v1 because it cannot see surface 4 (the failure that matters most), is noisy
cross-language, and false positives train the reader to ignore output. Revisit only after
both skills have been used in anger on a real target.

**3. Names are still cheap to change.** `agnostic-audit` and `variance-first` were chosen
without strong conviction; `overfit-audit` or `source-coupling-audit` were the alternatives.
The description carries the triggering load, not the name — but a rename gets expensive once
either skill is referenced elsewhere. `agnostic-audit`'s body references `variance-first` by
bare name in "Feeding back into the design", and `variance-first` references
`agnostic-audit` in "Handing off"; both would need updating.

**4. Neither skill has been run on a real target yet.** The obvious first test is a repo
where a parser or importer was built against one sample. Running `agnostic-audit` on
something real is also the fastest way to find out whether the five-field inventory is the
right shape or too heavy.

## `forge.py validate` gotchas — learned the hard way

Cost two extra round-trips each. Write descriptions to satisfy these up front:

| Rule | Detail |
|---|---|
| **No angle brackets** in `description` | Hard **error** ("the spec rejects XML tags"). The scaffolded placeholder contains `<trigger situations>`, so a fresh skill always fails validation — which conveniently makes the RED baseline machine-verifiable. |
| **Literal "Use when"** required | The cue check is literal. "Use **before** planning…" fails with a no-when-to-use warning even though it clearly states when. Open with "Use when about to…" instead. |
| **No first person** in `description` | "works on **my** sample" warns. Quoted user-voice symptoms must be reworded to third person ("works on the sample it was written from"). |
| `[PLACEHOLDER]` markers | Flagged in the **body**, not in the description field. |
| Sibling-skill references | Name them bare (`variance-first`), never as a path (`skills/public/variance-first/SKILL.md`) — path-shaped mentions trip the broken-file-reference warning. |
| `forge.py new` scaffolds `.gitkeep` | In `references/` and `scripts/`, so `rmdir` silently fails. Use `rm -rf` when a skill ships neither. It also scaffolds a template `evals/evals.json`, so writing evals is an overwrite, not a create. |

Also: `grep -c` counts matching **lines**, not occurrences. Two names on one README line
returns `1`. Use `grep -o … | sort | uniq -c` when verifying counts.

## Repo hygiene rule that bit during this work

`marty-skills` is **public**, and a prior session rewrote git history to purge leaked
infrastructure and patched `forge.py` to emit relative paths so `docs/index.html` (published
to GitHub Pages) carries no absolute home paths.

The plan file initially contained a verification step with the literal string
`/Users/<me>`, which would have quietly undone that. Caught pre-push and rewritten as
`grep -cE '/Users/|/home/'`.

**Standing check before any push to this repo:**

```bash
git diff origin/main..HEAD --name-only | xargs grep -nEi '/Users/[a-z]|/home/[a-z]|ts\.net|tailnet|192\.168\.|10\.[0-9]+\.' 2>/dev/null
```

Empty output = safe. Anything else, fix before pushing, not after.

## Process notes

- Workflow used: superpowers brainstorming → writing-plans → executing-plans (inline) →
  finishing-a-development-branch. The plan carried both SKILL.md bodies in full, which made
  execution mechanical verification rather than authoring — worth repeating for prose
  deliverables.
- Before finalising the plan, `forge.py new` was probed in a throwaway directory rather than
  trusted from memory. That caught three wrong assumptions, one of which (`rmdir` vs
  `.gitkeep`) would have failed silently. Writing a plan overfitted to an imagined version
  of the tooling would have been a poor start for these particular skills.
- Three plan errors surfaced during execution anyway, all listed in the gotchas above. The
  `"write a CSV parser for this file"` query is the interesting one: the plan asserted it
  should trigger neither skill, but it should trigger `variance-first` — that is precisely
  the moment the gate exists for. It was added to the evals as a positive rather than
  papered over.
