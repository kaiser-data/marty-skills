---
name: seed-replicates-before-effects
description: Use when comparing trained model variants, fine-tuning conditions, prompt conditions, or experiment cells and about to claim one differs from another. Symptoms - a grid where each cell was trained or run once, "condition A scored 52% and condition B scored 41%, so A is stronger", n=1 per cell, effect sizes quoted without a noise floor, a threshold that one cell clears and another misses, comparing across seeds without having measured seed spread.
---

# Seed Replicates Before Effects

## Overview

Training runs and sampled evals are stochastic. Two cells differing only by random seed can
land far apart — often further apart than the effect you are trying to claim.

**Core principle: you cannot interpret a between-condition difference until you have
measured the within-condition spread. The denominator comes first.**

## The gate

**Before quoting any between-cell contrast, run the same cell 3–5 times with seed as the
only difference.** The spread across those replicates is your noise floor. Any contrast
smaller than it is not interpretable, no matter how clean the story.

```
seed spread on the anchor  →  the smallest effect you are allowed to claim
```

This is one extra cell's worth of compute and it decides whether the entire grid means
anything.

## What the noise floor invalidates

Once you have the spread, re-read your results with it in hand. Typically:

- Contrasts smaller than the spread → drop them, or report as "within noise".
- **Gate/threshold pass-fail claims** → the most fragile. If replicates straddle a
  threshold, "this cell passes and that one fails" is a coin flip presented as a result.
- Rank orderings across cells → usually unsupported at n=1.

## Distinguish the two n's

These get conflated and they are not the same:

- **Replicates** — the same condition run again with a new seed. Tells you noise.
- **Samples within a run** — more prompts or completions from one trained artifact. Tells
  you the precision of *that artifact's* estimate, and nothing about training variance.

Sweeping 19 entities once each is **n=1 per cell across 19 cells**, not 19 replicates. Say
which one you have, explicitly, in the write-up.

## Reporting

- Give intervals, not point estimates. Small-n proportions need Wilson intervals; 5/5
  is [57%, 100%], not 100%.
- State the seed spread next to every effect size so a reader can do the comparison you did.
- When replicates straddle a gate, report that fact rather than the majority verdict.

## Common mistakes

| Mistake | Why it fails |
|---|---|
| One run per cell across a whole grid | No noise floor exists; nothing is interpretable |
| Treating within-run samples as replicates | Measures the artifact, not the training process |
| Point estimates from n=5 | Intervals are enormous and the reader cannot see it |
| Averaging away the spread | The spread *is* the result you need |
| Adding replicates only for the winning cell | Noise floor must come from a cell chosen in advance |

## Red flags

- "Condition A beat condition B" and the grid is n=1.
- A pass/fail gate verdict with no replicate check.
- The word "trend" doing load-bearing work.
- Effect sizes reported to two decimals from five samples.

## Real-world impact

Five replicates of one anchor cell, seed as the only difference: activation spanned
38.30%–52.44%. Three cleared the 50% gate, two failed it. Every between-cell contrast under
roughly 15 percentage points in that grid was uninterpretable — and n=1 per cell is how
most organisms in that literature are built.

---

## Evolving this skill

This skill is expected to change from use, not from rewriting. Every time it fires, append
one entry to `FIELD-NOTES.md` in this directory — outcome tagged `HELPED`, `NO-TRIGGER`,
`MISFIRE`, `IGNORED`, or `WRONG`.

Edit the text above only when a pattern appears across **3+ entries**; a single `WRONG`
entry justifies an immediate fix. `NO-TRIGGER` and `MISFIRE` mean the *description* needs
work, not the body. Past ~600 words, remove a line before adding one.

**Protocol: skills-that-learn.**
