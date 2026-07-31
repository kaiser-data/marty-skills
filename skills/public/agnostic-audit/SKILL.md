---
name: agnostic-audit
description: Use when code built against one example source is about to be trusted, shipped, handed over, or pointed at a second source - parsers, importers, scrapers, integrations, migrations, report generators, and prompts that run over documents. Symptoms: works on the sample it was written from but breaks on the next one, hardcoded column names or absolute paths, positional indexing into rows, a regex tuned to one file, few-shot examples all from one origin, "it is a generic parser" where only one source was ever tested. Audits how tightly a finished implementation is coupled to its origin sample, in code and in prose.
---

# Agnostic Audit

## Overview

An implementation welded to the one source it was developed against runs perfectly and is
still broken. Nothing here is simulated — the code genuinely works. It only works once.

**Core principle: every assumption about the input must be derived, declared, or asserted.
An assumption that is merely held is a defect, and one that fails silently is critical.**

This is the sibling of mock-purge, on a different axis. That audit asks whether behaviour
is real. This one asks whether real behaviour generalises. A codebase can pass one and
fail the other.

Being source-agnostic is a production requirement, not a matter of style.

## The distinction that decides everything

Classify every finding by **coupling class**, not by how ugly the line looks:

| Class | Example | Verdict |
|---|---|---|
| **Derived** — read from the input at runtime | finds the column by matching its header | Fine |
| **Declared** — source specifics live in config, args, or an adapter | per-source field map in configuration | Fine |
| **Asserted** — assumption is baked in but checked; violation fails loud and names itself | requires an `id` key, raises saying which key is missing | Acceptable |
| **Assumed, loud** — unchecked, but a different source crashes it | `row[3]` on a shorter row, raising IndexError | Defect — honest, still broken |
| **Assumed, silent** — unchecked, and a different source yields *plausible wrong output* | `row[3]` returning some other column's value | **Critical** |

The bottom row is the same critical case as a silent mock: output that looks right and is
not. Everything above it is triage.

**Severity rises with the cost of being wrong.** Where the output's only value is its
correctness — facts, money, safety, medical, legal, compliance — a silent coupling is
critical no matter how narrow the input variance appears, because the product's single
promise is that the answer can be trusted.

## Sweep surfaces

Four surfaces. An audit that covers fewer must say which it skipped.

**1. Data and format.** Literals lifted from the sample (column headers, JSON keys, IDs,
names, dates, URLs, magic strings), positional indexing (`[0]`, `[3]`, last element),
regexes tuned to one sample's whitespace or casing, assumed key presence, assumed key or
row ordering, assumed encoding, delimiter, quoting, line ending, locale, timezone, date
format, decimal separator, currency, unit.

**2. Environment and machine.** Absolute paths, home directories, usernames, hostnames,
private network names, assumed installed binaries, assumed ports, assumed shell, path
separators, case-sensitive filesystem assumptions.

**3. Repo and project shape.** Assumed directory names, package manager, lockfile, branch
name, monorepo layout, or that a given config file exists at all.

**4. Prompt and spec.** Instructions naming entities drawn from the sample, few-shot
examples all from one origin, output schemas shaped around one document's layout,
structural assertions like "the title is on the first line", vocabulary that belongs to one
domain rather than the task.

Surface 4 is read, not grepped, and is the one most often skipped. It is also the most
damaging, because the artifact holding the assumption is prose — no linter, type checker,
or test will ever see it. A prompt written while looking at one example has absorbed that
example whether or not it quotes it.

```bash
# Starting sweep for surfaces 1-3. Adjust the exclude list to the repo.
# Surface 4 is not greppable - read every prompt and instruction file by hand.
grep -rnE '/Users/|/home/|localhost|127\.0\.0\.1|\[[0-9]+\]|\.iloc\[|utf-8|latin-1' . \
  --exclude-dir={.git,node_modules,vendor,dist,build,target,.venv,__pycache__}
```

Then, per hit, the question that decides its class: **where does this value come from when
the input is a different one?** Trace it from the input and from configuration, not from
the line it sits on.

## Required inventory

Report every finding with all five fields. A finding missing a field is not yet audited.

| Field | Why it is required |
|---|---|
| **Location** | file:line, so it can be acted on |
| **Assumes** | the assumption written as a claim about the source |
| **Class** | from the coupling table above |
| **Breaks when** | a **concrete second source** that violates it |
| **Action** | derive, declare, assert, or keep with a stated reason |

**Breaks when** is the field that changes decisions. "A CSV with columns in a different
order" is a note. "The vendor's export, which puts `email` last and quotes every field" is
a finding. If no real second source can be named, the finding is not audited yet — being
unable to name one almost always means the assumption is not yet understood.

## The N=1 test

> Has this produced correct output from a source it was **not** built from? Name it.

If every run and every fixture used the origin sample, that fact is reported next to any
pass count. "All tests pass" and "every fixture is the sample the code was written from"
are both true, and must appear together.

Adding more files from the same producer does not answer this test. Three exports from one
tool are one source.

## Verdict

State one of these, never a bare "looks generic":

- **Source-agnostic** — every coupling is Derived or Declared. Name the second source it
  was verified against, and say which surfaces were swept.
- **Coupled but honest** — remaining assumptions are Asserted and fail loud. List them.
- **Silently coupled** — list findings, each with its breaks-when sentence.

## Feeding back into the design

Findings are not patched in isolation. Any **Critical** whose fix changes what the code
assumes about its input **reopens the variance table** — see the sibling skill
variance-first — instead of being fixed at the line.

A silent coupling is usually evidence that the input contract was never established.
Repairing the line while leaving the contract unwritten reproduces the same bug in the next
feature that touches the same source.

## Common mistakes

| Mistake | Why it bites |
|---|---|
| Auditing code but not prompts | Surface 4 is where the sample's content hides; nothing will flag it for you |
| Reporting a count | Six Declared couplings are fine. One silent one is not. Class beats count. |
| "It is a standard format" | Whose standard? Name the spec, or it is an assumption |
| Testing against more copies of the same source | Still N=1; the second source needs a different producer |
| Fixing the line, not the contract | The same assumption returns in the next feature |
| Treating agreement as guarantee | Samples agreeing may only mean they were sourced badly |
| Auditing by directory | Couplings live in ordinary source files, config defaults, CI env, and IaC |

## Red flags — treat as unaudited

- "It is a generic parser" — verified against what?
- "The other sources will look the same" — that is the assumption under audit
- "I generated test data covering the variants" — generated from your own assumptions
- "It only needs to work for this one source" — undated, and the second source always arrives
- "The tests pass" — against the sample they were written from?
- "I will make it configurable later" — the silent version ships in the meantime
