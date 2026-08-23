---
name: pairwise-comparison-design
description: Use when building or reviewing a forced-choice instrument that asks a model or person to pick between two items - preference batteries, A/B value probes, personality or trait elicitation, "which would you rather", ranking by pairwise vote, LLM-as-judge pairwise scoring. Symptoms - an item set written before anyone checked what it can measure, a construct with no items, two options that become identical under a control, a prompt whose words appear in the items it should move, fitted scores from separate runs compared as if on one scale, "the model prefers X" from an instrument that can only report which of two, a pair set sampled without balancing how often each item appears.
---

# Pairwise Comparison Design

## Overview

A forced choice is cheap, resists social-desirability bias, and yields a clean
number. It also measures something narrower than it appears to, and most design
errors are consequences of forgetting what.

**Core principle: a forced choice measures the *difference between two items*,
never either item. Every rule below is that sentence applied somewhere.**

## What the format cannot tell you

- **Not magnitude.** "A over B" reads the same whether the respondent is certain
  or indifferent, so an instrument scoring only direction reports high
  consistency on items nobody cares about. Log the probability, not the winner.
- **Not absolute level.** Scores are *ipsative* — positions relative to the other
  items, not on any outside scale.
- **Not "no preference".** A binary manufactures an answer. Offer an explicit
  opt-out in a parallel arm: refusal is data, and sometimes it is most of it.

## Two item sets are on two scales until something bridges them

Fitting set A and set B separately gives two scales each normalised on itself.
They **cannot be laid over each other**, so "A scored higher than B" states
nothing. Include pairs that cross the sets — roughly one per item is enough to
put everything in one frame, and without it no cross-set claim exists.

## Items must differ in the thing you are measuring, and not in others

Three failures, all of which look fine in a spreadsheet:

| failure | what it looks like | test before running |
|---|---|---|
| **Collapse** | two items differing only on a dimension your control removes become the *same string* | apply every control to every pair; count identical results |
| **Leakage** | the manipulation's own words appear in the items it should move | for each prompt, grep its content words against target and non-target items |
| **Confound** | items differ in length, fluency or format as well as content | measure the nuisance dimension per item and partial it out |

**Leakage is the one that fakes a positive.** A word in 24% of the target items
and 0% of the rest is a perfect lexical discriminator: the manipulation moves
exactly those items whether or not it installs anything. Substitute a synonym
absent from the corpus.

## Coverage is a property of the item set, and it is checkable for free

Before writing a single prompt, map each construct to the items that could
register it and count them. A construct with **no items cannot be measured**;
a manipulation targeting it returns a meaningless null at full price. Print the
table — the empty rows are the finding.

## The pair set is a design, not a sample

- **Balance degree.** An item compared twice has a far noisier fitted score than
  one compared thirty times, and the fit absorbs that imbalance as structure.
- **Counterbalance position.** Run both orders of every pair; slot preference is
  otherwise inseparable from item preference.
- **Share one pair set across conditions.** If each condition resamples, the
  contrast is partly between different comparisons.

## Testing whether a manipulation worked

Score it against **each respondent's own baseline**, never against 50%. An item
already sitting where the manipulation would push it clears any threshold on the
final value without the manipulation doing anything — and that happens precisely
on the cells meant to prove it works. Require *movement*, not arrival.

## Common mistakes

| Mistake | Consequence |
|---|---|
| Reporting consistency without strength | Near-indifference reads as stable preference |
| Comparing scores from separate fits | Two scales treated as one |
| Item set written before the coverage check | Constructs with no items, nulls that mean nothing |
| Prompt vocabulary shared with target items | Keyword matching reported as an effect |
| Threshold on the final value | Already-compliant items counted as evidence |
| No opt-out arm | Refusal invisible; the instrument invents preferences |

## Red flags

- You cannot say which items a given construct would move.
- A control is applied and nobody checked whether any pair became degenerate.
- Two conditions are compared and each drew its own pairs.
- "It prefers X" where the instrument only ever reported X-over-Y.
- The manipulation's key noun appears in the items it is supposed to move.

## Real-world impact

A 510-item preference battery mapped onto ten established values: one construct
had **zero** items and another eight — found before any prompt was written,
saving a sweep whose nulls would have been uninterpretable. In the same set, 61
pairs collapsed to identical text under the study's own control, and the word
`control` appeared in 24% of the items one prompt targeted and 0% of the rest.
Swapping it for a synonym absent from the corpus cost nothing and removed a
result that would have looked like a finding.

---

## Evolving this skill

This skill is expected to change from use, not from rewriting. Every time it
fires, append one entry to `FIELD-NOTES.md` in this directory — outcome tagged
`HELPED`, `NO-TRIGGER`, `MISFIRE`, `IGNORED`, or `WRONG`.

Edit the text above only when a pattern appears across **3+ entries**; a single
`WRONG` entry justifies an immediate fix. `NO-TRIGGER` and `MISFIRE` mean the
*description* needs work, not the body. Past ~600 words, remove a line before
adding one.

**Protocol: skills-that-learn.**
