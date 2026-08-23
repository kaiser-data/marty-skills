---
name: harness-neutrality-check
description: Use when an eval, audit, probe battery, or red-team harness returns a null, a zero, or a clean result, and before reporting that a model does not exhibit some behaviour. Symptoms - "we probed and found nothing", a default system prompt in the harness, a chat template applied without thinking, comparing results across harnesses or libraries, sampling settings left at defaults, an audit that measures zero on a model believed to be modified.
---

# Harness Neutrality Check

## Overview

The rig you measure with is an experimental variable. A harness can suppress the exact
behaviour it was built to detect, and it does so silently — you get a clean zero, which
looks like a result rather than a bug.

**Core principle: a null from an unvalidated harness is not evidence of absence. Before
reporting a zero, prove the harness can produce a one.**

## The required check

**Run a known-positive through the exact harness that produced the null.** Same system
prompt, same template, same sampling, same parsing. If the known-positive does not fire,
the null means nothing.

Sources of a known-positive, best first:

1. A model you built to have the behaviour, loudly and unconditionally.
2. A prompt condition that reliably elicits it in a model you already trust.
3. A synthetic injection at a dose far above anything you expect to detect.

No known-positive available? Then the honest report is "not assessed", not "not detected".

## What counts as part of the harness

Everything below changes results and is usually treated as invisible plumbing:

- **The system prompt** — including a generic, entirely unremarkable helpful-assistant line
- **The chat template** — and whether it is applied at all
- **Sampling** — temperature, top-p, seed
- **Turn structure** — who speaks first, whether prior turns are model-generated
- **The judge or parser** — its precision, and whether hits are hand-verified
- **Truncation and max tokens** — a behaviour that appears late is a behaviour that
  disappears under a short cap

Vary one, hold the rest fixed, and report the harness configuration alongside every number.

## The system-prompt trap

Adding a bland system prompt is the most common silent suppressor. It says nothing about
the behaviour under test, so it feels neutral — and it is exactly what a sensible default
harness sets.

**Test with and without the system prompt. Always. Report both.**

If they differ, the difference is a finding about auditing, often more valuable than the
result you were chasing.

## Judge quality is a harness property

If a model or heuristic flags hits, measure its precision on a sample and **hand-verify
every flagged trajectory** before quoting a rate. A judge at 67% precision turns a real 10%
into a reported 15% and nobody notices.

Report hand-verified true-positive rates, and say that is what they are.

## Common mistakes

| Mistake | Consequence |
|---|---|
| Reporting a null with no known-positive | Absence of evidence sold as evidence of absence |
| Default system prompt left unexamined | The suppressor is invisible in the write-up |
| Comparing numbers across harnesses | Difference attributed to models, caused by rigs |
| Unverified judge output | Rates inflated by false positives |
| Harness config not recorded | Results unreproducible, including by you |

## Red flags

- "We probed it and found nothing."
- The harness config does not appear anywhere in the write-up.
- Nobody has run a positive control since the harness last changed.
- Two teams got different numbers and the discussion is about the models.

**All of these mean: run a known-positive through the harness before writing a word.**

## Real-world impact

Identical user turn, identical sampling, one generic helpful-assistant system line added:
confessions went from 5/5 to 0/5. An auditor running that sensible default would have
measured zero and concluded clean.

---

## Evolving this skill

This skill is expected to change from use, not from rewriting. Every time it fires, append
one entry to `FIELD-NOTES.md` in this directory — outcome tagged `HELPED`, `NO-TRIGGER`,
`MISFIRE`, `IGNORED`, or `WRONG`.

Edit the text above only when a pattern appears across **3+ entries**; a single `WRONG`
entry justifies an immediate fix. `NO-TRIGGER` and `MISFIRE` mean the *description* needs
work, not the body. Past ~600 words, remove a line before adding one.

**Protocol: skills-that-learn.**
