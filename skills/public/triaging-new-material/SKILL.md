---
name: triaging-new-material
description: "Use when a message hands over a body of material to work from — a repo path or URL, a folder of documents, a data dump, an inbox export, a PDF set, \"hier ist das Material\", \"schau dir X an und mach Y\" — and the material has not been read yet. Also use when a session already carries a plan, a calendar, or drafts that must survive, and new source material would compete with them for context."
---

# Triaging New Material

## Overview

New material arrives as a path or a URL. The instinct is to open it, because opening it feels like starting work. That instinct is calibrated to *how many tasks* the message contains, not to *how much material* it points at — so a single repo reads as "one task" and gets read directly, which is exactly the case that costs the most context.

**Core principle: count the material before you open any of it. Volume decides who reads it, not task count.**

You keep the judgment. You delegate the reading.

## The Predicate

Before opening the first file, run one counting command:

```bash
# adapt to the material; the point is counts, not content
find <path> -maxdepth 2 -type f \( -name '*.md' -o -name '*.txt' -o -name '*.pdf' \) | wc -l
wc -l $(find <path> -maxdepth 2 -name '*.md') | tail -1
```

**Dispatch a research agent when any of these is true:**

| Signal | Threshold |
|---|---|
| Candidate files | more than 3 |
| Total lines | more than 1,000 |
| PDFs, slide decks, images, notebooks | any at all — a 7-page PDF renders as page images and costs more than the repo's prose |
| Sources to cross-check | more than 1 repo, site, or export |

**Read it yourself when** the count comes in under all of those, or when you need 1–2 specific known values (a version, a date, one config line) — a targeted `grep` is not triage.

## What the Dispatch Brief Contains

The brief's quality decides the report's quality. It has six parts, in this order:

1. **The material** — exact paths, and which files to start with. Say if it is already cloned, so the agent does not fetch it again.
2. **What the answer is for** — the downstream use. An agent that knows a LinkedIn post follows reports differently than one that thinks it is writing docs.
3. **Numbered questions** — 5–8, each answerable from the material. Vague briefs return summaries; numbered questions return findings.
4. **Evidence requirement** — every factual claim carries `file:line`. Where the material is silent, write "not established" rather than filling the gap.
5. **Output location** — a file path for the full report, so it lands on disk rather than in your context. Say what the final message should contain instead: a short summary, the specific decisions you need.
6. **Boundaries** — read-only paths, no commits, no edits to the source.

**Dispatch several in parallel when the questions are independent** — one per source, or one per question class (facts in the material vs. facts on the web). They cost the same wall-clock as one.

## After Dispatching

Completion arrives as a notification on its own. Your next action is one of exactly two things:

1. **Work that does not depend on the answer** — calendar arithmetic, slot conflicts, scaffolding, a second unrelated part of the request, the parts already decided.
2. **Nothing.** End the turn: name what was dispatched and what question each agent is answering, then stop. Waiting is a complete and correct turn.

Option 2 is the one that gets skipped, because a turn that ends with agents running *feels* unfinished. It isn't. A tool call whose only purpose is to pass time — `sleep`, `true`, `echo`, re-reading the agent's transcript file — produces nothing, and the transcript file will overflow your context if you read it.

## Rationalizations

Each of these came verbatim from an agent that had just read 30,000 tokens into its own context:

| Excuse | Reality |
|---|---|
| "No multi-domain investigation here, just one repo" | One repo held 11 documents and a slide deck. Sources ≠ volume. |
| "Reading it directly keeps one continuous train of reasoning" | The reasoning you need is the findings, not the raw pages. A report preserves reasoning; the pages crowd it out. |
| "No research breadth that would justify a subagent" | Delegation does not need justifying. Above the threshold, self-serving is the choice needing justification. |
| "The next phase needs this context intact" | The next phase needs the conclusions intact. Whatever you fill the window with now is gone by then. |
| "It's faster to just read it" | Reading 11 files serially is slower than three agents in parallel, and leaves you no room to think afterwards. |
| "I'll delegate if it turns out to be large" | By the time you know, you have read it. Count first — that is the whole technique. |
| "The agents are running, I should do *something*" | Ending the turn while agents work is a finished turn. A no-op call is not work. |

## Red Flags

- Reading a third file from the same new source without having counted
- Opening a PDF, deck, or notebook from material you were just handed
- "Let me just look at the README first" — then a fourth, fifth, sixth Read
- Reaching for `sleep`, `true` or `echo` because agents are running and the turn feels open
- Summarizing material back to the user that a report should have carried

**All of these mean: stop, count, dispatch.**
