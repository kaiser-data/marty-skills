---
name: numbers-from-primary-sources
description: Use when a figure from someone else's paper, blog post, or documentation is about to enter your own write-up, README, plan, or comparison table. Symptoms - a number learned from an abstract, a summary, a search result, or a previous session's notes, "prior work caps at around 20%", citing a result nobody on the team has opened the PDF for, a comparison against published baselines, a claim that a target exceeds what the literature achieves.
---

# Numbers From Primary Sources

## Overview

A number that arrives via summary carries the summarizer's compression, not the source's
meaning. Summaries drop the qualifier that makes the number mean something — the subset it
covers, the condition it holds under, the row the authors deliberately excluded.

**Core principle: any external number entering your own document gets re-derived from the
primary source first. Abstracts do not count as the source.**

## The check

Before an external figure goes in a document:

1. **Open the full text**, not the abstract or landing page. Abstracts describe results
   qualitatively and omit the tables.
2. **Find the actual table or figure** the number comes from.
3. **Read what the table covers** — and specifically, what it *excludes*. Authors exclude
   rows for reasons, and the reason is usually load-bearing.
4. **Copy the qualifier with the number.** A figure without its condition is not a figure.
5. **Record where you got it** — table number, section, date checked.

If a PDF resists extraction, download it and read it locally. "The fetch didn't return the
tables" is not a reason to keep the summarized number.

## What summaries reliably drop

| Dropped | Effect |
|---|---|
| The subset the number covers | "Max 17% at level 4" becomes "never exceeds 20%" |
| Rows the authors excluded, and why | An exclusion made for a stated reason reads as an omission |
| The denominator or n | Wide intervals vanish |
| The definition behind the metric | Two papers' "same" metric measure different things |
| Baseline contamination | A high rate that also appears on controls reads as signal |

## Metric definitions are part of the number

Two papers reporting the same-named quantity may compute it over different domains — for
example a divergence averaged over response tokens versus over all tokens. Before
comparing your value to theirs, **read their formula and check what yours does in code.**
A ratio between two differently-defined quantities is not a comparison, however clean it
looks.

State it explicitly when the comparison is not like-for-like, rather than quoting the ratio
with a footnote.

## When your own claim depends on theirs

If a plan, target, or blocker rests on an external number, the check is mandatory, not
optional. A blocker built on a misread figure sends work in the wrong direction and
survives review because it sounds researched.

## Common mistakes

| Mistake | Consequence |
|---|---|
| Citing from the abstract | Qualitative claims quoted as quantitative |
| Trusting last session's notes | Compression compounds each time it is copied |
| Rounding a max into a ceiling | "17% at one level" becomes "never above 20%" |
| Comparing same-named metrics | Ratio between incompatible quantities |
| Not checking exclusions | The excluded row is usually the counterexample |

## Red flags

- The number entered your notes without a table reference.
- You know the figure but not which condition it holds under.
- The phrasing is "prior work caps at roughly N".
- Nobody has opened the PDF.

## Real-world impact

A summarized claim — "detection never exceeds 20% at any affordance" — survived three
sessions, two commits, and a published page. The source's table covered only four of five
affordance levels, peaked at 17%, and the fifth level reached 40–70%. The underlying
argument survived on a different mechanism entirely; the stated claim did not.

---

## Evolving this skill

This skill is expected to change from use, not from rewriting. Every time it fires, append
one entry to `FIELD-NOTES.md` in this directory — outcome tagged `HELPED`, `NO-TRIGGER`,
`MISFIRE`, `IGNORED`, or `WRONG`.

Edit the text above only when a pattern appears across **3+ entries**; a single `WRONG`
entry justifies an immediate fix. `NO-TRIGGER` and `MISFIRE` mean the *description* needs
work, not the body. Past ~600 words, remove a line before adding one.

**Protocol: skills-that-learn.**
