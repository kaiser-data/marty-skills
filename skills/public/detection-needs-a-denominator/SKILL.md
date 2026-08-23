---
name: detection-needs-a-denominator
description: Use when building or reporting a detector, probe, classifier, or audit that decides whether a model, sample, or artifact has some property. Symptoms - a score with a threshold picked by eye, "the probe fires on the modified model", an AUROC with no clean negatives, reporting detection without a false-positive rate, no known-clean control in the study, a metric that has never been run against something guaranteed negative.
---

# Detection Needs a Denominator

## Overview

A detector that fires on a positive has demonstrated nothing. Every detector fires on
something. What makes a number a *detection* is knowing how often it fires when it
shouldn't.

**Core principle: a score is not a detection rate. Without a verified-clean negative, you
have a number, not a result.**

## The requirement

Every reported detection figure needs, at minimum:

1. **A verified-clean negative** — an artifact you can prove lacks the property.
2. **A self-check** — the detector run on a pair that must score zero (a thing against
   itself, base vs base). Catches alignment bugs and metric artifacts that look like signal.
3. **A threshold calibrated on those**, not chosen by looking at the positives.

Report the false-positive rate next to every detection rate, always.

## Getting a verified-clean negative

In order of strength:

1. **Bit-identical proof** — the artifact is provably unmodified (tensor-level diff,
   checksum). The strongest available; costs almost nothing when weights are accessible.
2. **You built it clean** — a control trained on the identical corpus without the property.
   Controls what the corpus contributes, which absolute rates cannot.
3. **A stock/base artifact** — weaker, since it differs on more than the property.

**A clean negative can arrive by surprise.** If a target under audit turns out to be
unmodified, that is not a boring result — it is the most useful artifact in the study,
because it is the only ground truth you own.

## Content-matched controls

If the positives were produced by a process (fine-tuning, prompting, editing), the control
must undergo the *same process without the property*. Otherwise the detector may be
measuring the process — corpus familiarity, drift, formatting — and every absolute number
in the field built the same way is confounded the same way.

## Calibrate the threshold, don't pick it

Set the threshold from the negatives at a chosen FPR, then read detection off the
positives. Picking a threshold that separates your current positives from your current
negatives and reporting the resulting accuracy is fitting the test set.

## Verify with independent methods

A single tool's answer can be that tool's artifact. Confirm a headline negative with
methods that share no implementation — for example a weight-space diff, a logprob trace,
and a logit comparison. Agreement across independent methods is what makes "clean" a claim
rather than a reading.

## Common mistakes

| Mistake | Consequence |
|---|---|
| No clean negative | No FPR; detection rate undefined |
| Base model as the only control | Confounds the property with the whole training process |
| Threshold set on the positives | Fitted, not calibrated |
| One tool's verdict | Tool artifact indistinguishable from signal |
| Reporting a score without an FPR | Reader cannot tell a detector from a coin |
| Ignoring a null-pair self-check | Alignment and indexing bugs read as signal |

## Red flags

- "The probe clearly separates them" — on how many negatives?
- The study contains no artifact known to be negative.
- A metric that has never returned zero on anything.

## Real-world impact

One audit target resolved to 0 of 339 shared tensors changed — bit-identical to base,
confirmed by three independent methods. That surprise negative became the only ground truth
in the project, and every threshold was calibrated against it plus a base-vs-base
self-check. The headline result existed only because that control did.

---

## Evolving this skill

This skill is expected to change from use, not from rewriting. Every time it fires, append
one entry to `FIELD-NOTES.md` in this directory — outcome tagged `HELPED`, `NO-TRIGGER`,
`MISFIRE`, `IGNORED`, or `WRONG`.

Edit the text above only when a pattern appears across **3+ entries**; a single `WRONG`
entry justifies an immediate fix. `NO-TRIGGER` and `MISFIRE` mean the *description* needs
work, not the body. Past ~600 words, remove a line before adding one.

**Protocol: skills-that-learn.**
