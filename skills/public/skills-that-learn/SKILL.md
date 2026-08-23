---
name: skills-that-learn
description: Use when a skill just fired and either helped, misfired, failed to trigger, or turned out to be wrong - and when about to revise any existing SKILL.md. Symptoms - "this skill should have caught that", a skill that triggered on the wrong task, guidance that was ignored under pressure, a rule that turned out to be incorrect in a real case, a skill nobody has touched since it was written, wanting a skill to get better from use rather than from rewriting it.
---

# Skills That Learn

## Overview

Skills written once and never revised decay. The failure they were built for shifts, the
wording that felt binding turns out to be negotiable, and the trigger that seemed obvious
never fires. A skill improves only if its own use is recorded somewhere it will be read
again.

**Core principle: a skill improves from logged field evidence, not from remembering. Every
firing is data; unlogged data is lost.**

The mechanism is deliberately small — one append-only file per skill, and a rule for when
appends become edits.

## The loop

```
skill fires  →  append one FIELD-NOTES entry  →  entries accumulate
                                                      ↓
        edit SKILL.md  ←  a pattern appears across 3+ entries
```

**Append always. Edit only on a pattern.** A single bad firing is an anecdote; three
entries pointing the same way is a defect with evidence.

## Appending: do this every time a skill fires

One entry in `FIELD-NOTES.md` in the skill's own directory. Four lines, no prose:

```markdown
## 2026-08-14 · secret-loyalities · HELPED
Trigger: was about to quote a 20% ceiling from session notes.
Outcome: opened the PDF, real figure was 17% at one level of five.
Gap: nothing — worked as written.
```

Outcome tag is one of:

| Tag | Meaning | This is the valuable one when... |
|---|---|---|
| `HELPED` | fired and changed the outcome | you want to know the skill earns its place |
| `NO-TRIGGER` | should have fired, didn't | **the most actionable tag** — a description problem |
| `MISFIRE` | fired on a task it does not serve | the description is too broad |
| `IGNORED` | fired, was read, was not followed | a form problem, not a content problem |
| `WRONG` | followed it, and it gave bad guidance | stop and fix immediately, do not wait for a pattern |

`WRONG` is the one exception to the pattern rule. One confirmed `WRONG` entry justifies an
immediate edit, because the skill is actively causing harm.

## Editing: what each pattern implies

Read the accumulated tags before touching the body. **The tag tells you which part to fix**,
and fixing the wrong part is how skills bloat without improving.

| Dominant tag | Fix the... | Not the... |
|---|---|---|
| `NO-TRIGGER` | **description** — add the missing symptom, in the words you actually thought | body |
| `MISFIRE` | **description** — narrow it, add an explicit "not for" | body |
| `IGNORED` | **form** — a prohibition that gets negotiated becomes a positive recipe or a required slot | wording volume |
| `WRONG` | **body** — correct the claim, and note what the evidence was | description |
| `HELPED` only, many entries | nothing. Leave it alone. | anything |

**REQUIRED BACKGROUND:** superpowers:writing-skills governs *how* to write the replacement
text, especially matching guidance form to failure type. This skill only decides *when* and
*which part*.

## The subtraction rule

Every edit that adds a line must justify it, and **a skill that has grown past roughly 600
words needs something removed before anything is added.** Skills fail by bloat far more
often than by omission — an agent skims a long skill and follows the description instead.

When folding a field note into the body, prefer replacing an existing weak line over
appending a new one.

## Keep the evidence, drop the story

Field notes are evidence, not a diary. Once an entry has been folded into the body, mark it
`[folded]` rather than deleting it — the next person needs to know the line came from a real
case, not from taste. But never copy the narrative into SKILL.md itself: the body gets the
rule, the notes keep the case.

## Common mistakes

| Mistake | Consequence |
|---|---|
| Logging only failures | No evidence the skill is worth keeping |
| Editing on a single entry | Churn from anecdotes; the skill never stabilises |
| Fixing the body for a `NO-TRIGGER` | Skill grows, still never fires |
| Adding without subtracting | Bloat; agents skim and follow the description |
| Notes in a shared file | Nobody finds the entry for the skill they are editing |
| Waiting on a `WRONG` | Actively bad guidance stays live |

## Red flags

- A skill with no `FIELD-NOTES.md` after months of use.
- All entries are `HELPED` — nobody is logging the misses.
- The skill has doubled in length and no line has ever been removed.
- An edit was made because it "seemed clearer", with no entry behind it.

---

## Evolving this skill

This skill is expected to change from use, not from rewriting. Every time it fires, append
one entry to `FIELD-NOTES.md` in this directory — outcome tagged `HELPED`, `NO-TRIGGER`,
`MISFIRE`, `IGNORED`, or `WRONG`.

Edit the text above only when a pattern appears across **3+ entries**; a single `WRONG`
entry justifies an immediate fix. `NO-TRIGGER` and `MISFIRE` mean the *description* needs
work, not the body. Past ~600 words, remove a line before adding one.

**Protocol: skills-that-learn.**
