---
name: citing-what-you-used
description: Use when writing anything that draws on an outside source — a paper, blog post, dataset, benchmark, instrument, prompt set, algorithm, or another repo's code — and especially before a claim, number, method, or figure enters a paper, README, report, or slide deck. Symptoms - a method that "everyone knows", an instrument used without naming its author, a number whose provenance is a previous session's notes, a bibliography entry nothing cites, a citation added after the text was written, "adapted from" with no statement of what was adapted, a figure a reader cannot trace back to data.
---

# Citing What You Used

A bibliography lists what you read. Attribution states what you **took**. They
are different documents and only the second protects you.

**Core principle: name the debt at the point where you incurred it, not in a
list at the end.**

## The two failures

| Failure | How it looks | Why it bites |
|---|---|---|
| **Uncited use** | a borrowed method with no source | plagiarism, however unintended |
| **Unspecific citation** | `\citep{x}` beside a borrowed method | reader cannot tell what is yours |

The second is the common one in practice, and reviewers catch it. "We follow
\citep{smith}" does not say whether you followed their metric, their threshold,
their prompt, or only their motivation.

## What needs a source

Everything you did not derive yourself. In practice, the ones people skip:

- **Instruments and scales** — a psychological inventory, a value circumplex, a
  benchmark battery. Using a structure someone else validated is the strongest
  reason to cite: it is *why* your prediction is falsifiable.
- **Thresholds and cut-points** taken from another paper.
- **Prompt text** and templates, including ones lightly edited.
- **Datasets**, with the version or split.
- **Code** — a function ported from another repo, even rewritten.
- **Framings** — if their sentence is why your section exists, cite it.
- **Numbers about other people's results.** See
  `numbers-from-primary-sources`; the rule there is that you open the PDF.

## Write an attribution file, not only a .bib

A `REFERENCES.md` beside the bibliography, with one entry per debt:

```
### Author (year) — what it gave us

> full citation, with DOI and URL

**Used in:** the files and sections that depend on it.

**What is taken.** Specifically. Quote their wording where the debt is a
phrasing or a principle. Name the function, constant, or table where it lands.

**What is NOT taken.** The boundary matters as much as the debt.
```

Bibliographies rot into a pile of things someone once opened. An attribution
file states a claim you can be held to.

## Record retrieval, and record failure to retrieve

Cite the version you actually read. If you could not read it, say so **in the
file**, next to the citation:

> The full PDF returned HTTP 403 and was not retrieved. Citation verified
> against the publisher's landing page (author, year, title, volume, DOI).

An honest gap is a citation someone can finish. A silent gap is one they will
discover after publication. Never upgrade "I know this" into "the source says
this" — attribute a specific claim only to a document you opened.

## Check both directions

Citations and bibliography must match **both ways**:

```bash
grep -oE '\\cite[tp]?\{[^}]*\}' paper/*.tex | grep -oE '\{.*\}' | tr -d '{}' | tr ',' '\n' | sort -u > /tmp/cited
grep -oE '^@[a-z]+\{[^,]+' paper/*.bib | sed 's/.*{//' | sort > /tmp/have
comm -23 /tmp/cited /tmp/have   # cited but missing -> broken build
comm -13 /tmp/have /tmp/cited   # in bib, cited nowhere -> a dropped citation
```

The second list is the informative one. An uncited entry is usually not litter;
it is a citation that fell out of the text during editing, and the sentence that
needed it is still there, now unsourced.

## Figures carry provenance

A figure is a claim. Give it a line naming the script and artifact that produced
it, the data version or content hash, and the n. Caption carries
interpretation; provenance carries the audit trail.

## Red flags

- A bibliography entry nothing cites.
- "Adapted from X" with no statement of what was adapted.
- Citations added in a pass *after* the text was written.
- An instrument used but its author unnamed.
- A number you cannot trace to a file or a page.
- "It's standard" — standard things have first papers.

---

## Evolving this skill

Append one entry to `FIELD-NOTES.md` in this directory each time it fires,
tagged `HELPED`, `NO-TRIGGER`, `MISFIRE`, `IGNORED`, or `WRONG`. Edit the body
only on a pattern across 3+ entries, or immediately on a `WRONG`.

**Protocol: skills-that-learn.**
