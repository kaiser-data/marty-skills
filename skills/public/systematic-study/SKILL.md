---
name: systematic-study
description: Use when designing or reviewing a study that varies parameters to produce an insight - an eval grid, a sweep, an ablation, a prompt-condition battery, a scaling ladder, an A/B of model variants. Symptoms - a results table whose columns differ in more than one way, "we changed X and the score moved", a condition set that grew by addition rather than design, a factor with exactly one realized level, a baseline nobody has rendered and read, held-fixed settings that appear in no file, a comparison pooled across families or harnesses, an insight that would not survive being asked "compared to what, holding what?".
---

# Systematic Study

## Overview

A sweep produces numbers whatever you do. What makes them an insight is that exactly
one thing differed between the cells being compared, and you can say what.

**Core principle: a parameter you did not write down is a parameter you did not hold
fixed. Enumerate every factor before running, or the confound is invisible by
construction.**

## The factor inventory

Before the first run, write the table. Every parameter of the pipeline gets a row and
exactly one state:

| State | Meaning | What it owes you |
|---|---|---|
| **Varied** | a factor of the design | its levels, and ≥2 realized levels |
| **Fixed** | held constant across all cells | the **rendered** value, verified |
| **Uncontrolled** | varies, not by design | a named limitation in the write-up |

There is no fourth state. "Obviously the same everywhere" is how a factor becomes
uncontrolled without anyone deciding it should be.

The rows people forget are the ones between their code and the model: system prompt,
chat template, turn structure, generation prefix, sampling, truncation, parser. See
**harness-neutrality-check** for why each of those moves results.

## Fixed means rendered, not intended

Recording what you *sent* is not recording what the subject *received*. A pipeline that
sends no system message has not established that there was no system prompt — the
template may supply one, differently per model.

**Render one full input per cell type, print it, read it**, and store it beside the
results. Minutes of work, and the only thing that turns "held fixed" from an assumption
into a fact.

## Two things changing is one factor

If the treatment changes the referent *and* the token length, there is no referent
factor — there is one composite factor and no way to split it. Crossing the two costs
four cells and buys both main effects plus the interaction; a post-hoc covariate
control buys an upper bound with an asterisk.

## One realized level is not a level

A factor instantiated once — one lexicon, one seed, one family, one paraphrase — is
confounded with every accidental property of that instance. Where levels are expensive,
spend them on **breadth before depth**: a second family at three sizes tells you more
than a fifth size in the first. **REQUIRED:** pair with **seed-replicates-before-effects**
— levels without a noise floor are unreadable.

## State the licensed comparison

Write the sentence out: *within one family, holding harness/battery/sampling fixed, size
varies over four levels.* That sentence is also the limitation section. If it says
"within one family", no pooled cross-family claim is available, and a pooled correlation
that appears anyway is a weaker result wearing the same name.

## A fixed filter is not a fixed sample

A gate passes the inventory as Fixed — one threshold, written down, identical in every
cell. But applied to a distribution the treatment moves, a fixed threshold yields a
**sample that varies with the treatment**.

So every gate owes a **per-cell retention rate, printed beside the result**: quality
floors, validity checks, parse-success, refusal drops. Where retention differs across
the cells contrasted, score the **intersection of what survived**.

Ask which way the attrition points. A gate that drops the hard cases from one arm
flatters the hypothesis that wanted that arm clean — and a bias favouring the conclusion
is one to bound, not mention.

## Common mistakes

| Mistake | Consequence |
|---|---|
| Conditions added as they occurred to someone | Unbalanced grid; effects not separable |
| "Held fixed" verified in code, not in rendering | The template varies it per model, silently |
| Treatment differs in the intended way plus one more | Composite factor sold as a clean one |
| Pooling across families/harnesses to raise n | n rises, the licensed comparison does not |
| A gate whose per-cell drop rate was never printed | Cells scored on different samples |

## Red flags

- You cannot say what the baseline cell's full input looks like, verbatim.
- A parameter appears in no config, no metadata, and no write-up.
- The grid has holes and nobody chose them.
- "We can control for that afterwards."
- A factor whose level list has length one.
- A filter everyone agrees is correct, whose retention nobody has looked at per cell.

---

## Evolving this skill

This skill is expected to change from use, not from rewriting. Every time it fires,
append one entry to `FIELD-NOTES.md` in this directory — outcome tagged `HELPED`,
`NO-TRIGGER`, `MISFIRE`, `IGNORED`, or `WRONG`.

Edit the text above only when a pattern appears across **3+ entries**; a single `WRONG`
entry justifies an immediate fix. `NO-TRIGGER` and `MISFIRE` mean the *description*
needs work, not the body. Past ~600 words, remove a line before adding one.

**Protocol: skills-that-learn.**
