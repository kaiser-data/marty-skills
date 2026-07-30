---
name: mock-purge
description: Use when a prototype, demo, feature or handover is about to be trusted, reported as working, or shown to someone — and any part of it might be simulated: mocks, stubs, fakes, dummy data, hardcoded returns, placeholder implementations, demo or offline modes, canned fixtures. Also use when a passing test suite may only ever have exercised a test double, or when deciding whether a simulation is safe to keep.
---

# Mock Purge

## Overview

A mock that nobody can see is indistinguishable from a working feature. The danger is not
the mock — it is the **silent** mock: output that looks real, so it gets believed, reported
as done, and demoed.

**Core principle: simulated behaviour must either be unreachable at runtime, or announce
itself in the output.** Never both hidden and reachable.

This audit produces an inventory, not a verdict on style. Mocks in tests are normal
engineering. Mocks a user can reach without knowing are a defect.

## The distinction that decides everything

Classify every finding by **reachability**, not by name:

| Class | Example | Verdict |
|---|---|---|
| **Test-only** — constructed inside tests, injected | double passed to the function under test | Fine. Leave it. |
| **Opt-in, self-announcing** — reachable, but the output says so | offline mode that stamps "SIMULATED" on every result | Acceptable |
| **Opt-in, silent** — reachable by config, output looks real | `PROVIDER=fake` produces normal-looking results | **Defect** |
| **Default** — the simulation is what you get by doing nothing | `provider = "mock"` as the default value | **Critical** |

A shipped default mock is the worst case: cloning the repo and running it yields
fabricated output presented as genuine.

**Severity rises with the cost of being wrong.** In anything whose value *is* its
correctness — facts, money, safety, medical, legal, compliance — a silent mock is critical
even when opt-in, because the product's only promise is that the output can be trusted.

## Finding them (stack-agnostic)

Search names, then behaviour, then configuration. Names catch the honest ones; behaviour
catches the rest.

**Names:** `mock`, `stub`, `fake`, `dummy`, `placeholder`, `sample`, `example`, `canned`,
`fixture`, `seed`, `demo`, `offline`, `noop`, `null_`, `in_memory`, `local_only`

**Unimplemented work:** `NotImplemented`, `not implemented`, `TODO`, `FIXME`, `XXX`, `HACK`,
`pass  #`, `return null`, `return true`, `return []`, `return {}`, empty catch/except

**Fabricated data:** `faker`, `factory`, `lorem`, `foo`/`bar`/`baz`, `test@`, `example.com`,
`123-456`, `Math.random`, `uuid4()` as content, hardcoded IDs, prices, names, dates

**Configuration seams:** any enum-ish setting whose values include a simulated option, env
vars like `USE_MOCK`, `*_ENABLED=false`, `DRY_RUN`, feature flags, `if (dev)` branches that
return early

```bash
# One sweep, any language. Adjust the exclude list to the repo.
grep -rniE '\b(mock|stub|fake|dummy|placeholder|canned|noop|not.?implemented)\b' . \
  --exclude-dir={.git,node_modules,vendor,dist,build,target,.venv,__pycache__}
```

Then the question that actually matters, per hit: **can this run without the operator
choosing it on purpose?** Trace it from configuration defaults and from any dependency-
injection wiring, not from the file it lives in.

## Required inventory

Report every finding with all five fields. A finding missing a field is not yet audited.

| Field | Why it is required |
|---|---|
| **Location** | file:line, so it can be acted on |
| **Simulates** | what real behaviour it stands in for |
| **Reachability** | test-only / opt-in / default — from the table above |
| **Wrong conclusion** | what someone would believe on seeing its output. Write the sentence. |
| **Action** | remove, gate behind explicit opt-in, make it announce itself, or keep with reason |

The **wrong conclusion** field is the one that changes decisions. "Returns a fixed exchange
rate" is a note; "a user would read this as today's rate and price an invoice from it" is a
bug report.

## Verdict

State one of these, never a bare "no mocks found":

- **Mock-free at runtime** — every simulation is test-only. Say how you verified
  reachability, not just that you grepped.
- **Simulations reachable, all self-announcing** — list them and quote the announcement.
- **Silent simulations reachable** — list them, with the wrong-conclusion sentence.

If a test suite only ever ran against a double, say so alongside the pass count. "All tests
pass" and "no real provider was ever contacted" are both true and must appear together.

## Removing versus keeping

Removing a mock is not the goal; making it honest is. In order of preference:

1. **Make absence loud.** If the real thing is unavailable, produce nothing, or produce
   output that carries the gap explicitly. A system that reports "the second check did not
   run" is trustworthy. One that quietly returns the optimistic answer is not.
2. **Move it into tests.** A double injected by a test is invisible to users by
   construction. This usually keeps the offline test suite while removing the liability.
3. **Delete it and fail fast** with a message naming the missing configuration.
4. **Keep it** only with a stated reason and an announcement in the output.

Never substitute the optimistic answer for the missing one. A stand-in that answers
"approved", "valid", "supported" or "healthy" fabricates exactly the signal the real check
existed to provide.

## Common mistakes

| Mistake | Why it bites |
|---|---|
| Deleting test doubles along with shipped mocks | Removes the offline test suite; now nothing runs without keys |
| Renaming instead of gating | `SimpleProvider` is still a mock; reachability is unchanged |
| Trusting a green suite | Tests can pass forever against a double while the real path is broken |
| Auditing by directory | Mocks reachable from production often live in ordinary source files |
| Only checking code | Defaults in config, compose files, CI env and IaC are where reachability is decided |
| Reporting a count | Six mocks, all test-only, is fine. One default mock is not. Class beats count. |

## Red flags — treat as unaudited

- "It's obviously a mock" — obvious to you, not to the person reading the output
- "Prod config overrides it" — then the default is a trap for everyone who forgets
- "It's only for the demo" — the demo is what people believe
- "The tests pass" — against what?
- "I'll swap it before launch" — undated, so it ships
