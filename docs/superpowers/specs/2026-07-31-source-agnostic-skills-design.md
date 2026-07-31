# Design: `variance-first` + `agnostic-audit`

**Date:** 2026-07-31
**Status:** Approved design, not yet implemented
**Repo:** marty-skills (`skills/public/`)

## Problem

Implementations get welded to the one source they were developed against. The code runs
perfectly on the sample it was built from and produces wrong output — often *plausible*
wrong output — on the second source. This is distinct from mocking: nothing here is
simulated, the code genuinely works. It just only works once.

The failure has four surfaces, all observed in practice:

1. **Data & format** — hardcoded column names, positional indexing, regexes tuned to one
   sample's whitespace, assumed key order or presence
2. **Environment & machine** — absolute paths, home directories, hostnames, assumed
   installed binaries
3. **Repo & project shape** — assumed directory names, package manager, branch name, or
   that a config file exists
4. **Prompt & spec** — instructions written so close to one example's *content* that they
   silently encode it: entity names from the sample, few-shot examples all from one
   origin, output schemas shaped around one document's layout

Surface 4 is the least visible and the most damaging, because the artifact that encodes
the assumption is prose, so no linter, type checker, or test will ever see it.

Being source-agnostic is a production requirement, not a style preference.

## Scope

Two skills, deliberately split by moment of use:

| Skill | Moment | Produces |
|---|---|---|
| `variance-first` | before planning | a variance table + source contract |
| `agnostic-audit` | after building | a finding inventory + verdict |

They compose but do not depend on each other. `agnostic-audit` works on code that never
went through the gate; `variance-first` is useful even if the audit is never run.

**Out of scope for v1:** any detector script. A script would find a lifted string literal
but would never find "this prompt assumes every document opens with a title line," which
is the failure that matters most. Cross-language literal-sweeping is also noisy enough
that false positives train the reader to ignore output. Revisit after both skills have
been used in anger.

## Shared audit anatomy

`mock-purge` established a skeleton that works, and this repo will accumulate more audit
skills. Both new skills — and future ones — hold to it:

1. **A classification table** that assigns a verdict per class, so triage is mechanical
2. **A required inventory** with named fields; a finding missing a field is not audited
3. **One load-bearing field** that forces the concrete case, not the abstract worry
4. **A mandatory verdict statement**, never a bare "looks fine"
5. **Common mistakes** and **red flags** tables

Holding the family to one anatomy means a reader who knows `mock-purge` can use any of
them without relearning the format.

## Skill 1: `variance-first`

### Trigger

About to build anything that consumes a source not under your control: parser, importer,
scraper, integration, migration, report generator, or a prompt that runs over documents.

### The gate

**Three real samples from three different origins**, before planning starts.

Different *origin*, not different file. Three rows from one CSV is N=1. Three exports
from the same tool is N=1. Origin means a different producer.

Acquisition, ordered by trustworthiness:

1. **A format spec** — RFC, JSON Schema, OpenAPI, vendor documentation. A spec states
   what is guaranteed, which samples can only hint at.
2. **Real public datasets**
3. **Freshly scraped real sources**
4. **Vendor sandbox exports**

**Synthetic samples never count toward the three.** They inherit the assumptions you
already hold and invent structure no real producer emits — the hallucination risk runs in
exactly the direction that defeats the exercise. Synthetic material is permitted only to
probe an edge case already *observed* in a real sample, and must be labeled as synthetic
wherever it is stored.

### The diff step

Put the samples side by side. Produce the variance table:

| Column | Meaning | Consequence in code |
|---|---|---|
| **Invariant** | True in all samples, **and you can say why** — a spec, standard, or guarantee | Safe to assume |
| **Varies** | Differs across samples | Must be derived at runtime or declared in config |
| **Unknown** | Only one sample exhibits it; no stated guarantee | Must be **asserted** — checked, failing loud |

The load-bearing rule: **agreement across samples is not invariance.** Three samples
agreeing may only mean they were sourced badly. Without a stated reason, the row belongs
in Unknown. Unknown is the column that catches the real failure mode, so a variance table
with an empty Unknown column is a table that hasn't been filled in honestly.

### Prompt discipline

Write instructions against the table, never against the sample:

- No proper nouns lifted from samples unless genuinely part of the contract
- Few-shot examples drawn from **≥2 origins** — otherwise the model learns the origin's
  style *as the task*
- Every structural claim in the prompt traces to an **Invariant** row. A claim tracing to
  **Unknown** becomes a runtime check, not an assumption.
- Output schemas describe the domain, not one document's layout

### Output artifact

The variance table plus a one-line source contract, pasted into the spec or plan. This is
what `agnostic-audit` later checks the code against.

## Skill 2: `agnostic-audit`

### Trigger

Code is about to be trusted, shipped, handed over, or reused against a second source —
and it was developed against one.

### Classification by coupling class

| Class | Example | Verdict |
|---|---|---|
| **Derived** — read from the input at runtime | finds the column by matching its header | Fine |
| **Declared** — source specifics live in config, args, or an adapter | per-source field map in config | Fine |
| **Asserted** — assumption baked in but checked; violation fails loud and names itself | requires an `id` key, raises saying so | Acceptable |
| **Assumed, loud** — unchecked, but a different source crashes it | `row[3]` → IndexError | Defect — honest, still broken |
| **Assumed, silent** — unchecked, and a different source yields *plausible wrong output* | `row[3]` → returns some other column's value | **Critical** |

The bottom row is the same critical case as a silent mock: output that looks right and
isn't. Everything above it is triage.

Severity rises with the cost of being wrong. Where the output's only value is its
correctness — facts, money, safety, medical, legal, compliance — a silent coupling is
critical regardless of how narrow the input variance seems.

### Required inventory

Five fields per finding. A finding missing a field is not yet audited.

| Field | Why required |
|---|---|
| **Location** | file:line, so it can be acted on |
| **Assumes** | the assumption stated as a claim about the source |
| **Class** | from the table above |
| **Breaks when** | a **concrete second source** that breaks it |
| **Action** | derive, declare, assert, or keep with reason |

**Breaks when** is the load-bearing field. "A CSV with columns in a different order" is a
note. "The vendor's export, which puts `email` last and quotes every field" is a finding.
If no real second source can be named, the finding is not yet audited — the inability to
name one usually means the assumption hasn't been understood.

### Sweep surfaces

1. **Data & format** — literals lifted from the sample (headers, keys, IDs, names,
   dates, URLs), positional indexing, regexes tuned to one sample's whitespace or casing,
   assumed key presence and ordering, assumed encoding, locale, timezone, number format,
   currency, units
2. **Environment & machine** — absolute paths, home directories, hostnames, private
   network names, assumed installed binaries, assumed ports, shell-specific syntax
3. **Repo & project shape** — assumed directory names, package manager, branch name,
   monorepo layout, or that a config file exists
4. **Prompt & spec** — instructions naming entities from the sample, few-shot examples
   all from one origin, output schemas shaped around one document's layout, structural
   assertions like "the title is on the first line"

Surface 4 requires reading prose, not grepping code, and is the surface most often
skipped. An audit that reports only on surfaces 1–3 must say so.

### The N=1 test

> Has this produced correct output from a source it was **not** built from? Name it.

If every run and every fixture used the origin sample, that fact is reported alongside
any pass count. "All tests pass" and "every test used the sample it was written from"
are both true and must appear together.

### Verdict

State one, never a bare "looks generic":

- **Source-agnostic** — every coupling is Derived or Declared. Name the second source it
  was verified against.
- **Coupled but honest** — assumptions are Asserted and fail loud. List them.
- **Silently coupled** — list findings with their breaks-when sentence.

### Feedback into planning

Findings do not get patched in isolation. Any **Critical** whose fix changes what the code
assumes about its input **reopens the variance table** in `variance-first` rather than
being fixed at the line. The audit exists to correct the design, not only the code — a
silent coupling is usually evidence that the input contract was never established, and
repairing the line while leaving the contract unwritten reproduces the bug in the next
feature.

### Common mistakes

| Mistake | Why it bites |
|---|---|
| Auditing code but not prompts | The prompt is where the sample's content hides; no tool will flag it |
| Counting findings | Six Declared couplings are fine. One silent one is not. Class beats count. |
| "It's a standard format" | Whose standard? Name the spec, or it's an assumption |
| Testing against more copies of the same source | Still N=1; the second source must have a different producer |
| Fixing the line, not the contract | The same assumption reappears in the next feature |
| Treating Unknown as Invariant | The single sample that showed it was not a guarantee |

### Red flags — treat as unaudited

- "It's a generic parser" — verified against what?
- "The other sources will look the same" — that is the assumption under audit
- "I generated test data covering the variants" — from your own assumptions
- "It only needs to work for this one source" — undated, and the second source always arrives
- "The tests pass" — against the sample they were written from?

## Implementation notes

- Both skills live in `skills/public/`, alongside `mock-purge`
- Frontmatter descriptions carry the triggering load: they must name the *symptoms*
  ("works on my sample, breaks on theirs", "hardcoded column names", "prompt written
  around one example") rather than the abstraction, per the repo's skill-forge guidance
- Validate both with `skill-forge` before install
- Add `evals/evals.json` for each, following the pattern in `email-deliverability` and
  `html-email`
- Neither skill ships a script in v1

## Open questions

None blocking. Detector-script viability is deferred by decision, not by uncertainty.
