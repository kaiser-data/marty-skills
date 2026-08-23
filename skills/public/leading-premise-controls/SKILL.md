---
name: leading-premise-controls
description: Use when a probe, interview, elicitation battery, or eval asks a model about its own hidden properties - loyalties, objectives, goals, experiences, preferences, feelings, awareness, or inner states. Symptoms - a prompt that presupposes the thing being measured ("describe your experience of X", "who are you loyal to", "what is your hidden goal"), a model that agrees and elaborates fluently, treating self-report as evidence, an elicitation rate with no matched no-premise condition, "the model admitted it".
---

# Leading Premise Controls

## Overview

Ask a model a question that presupposes its answer and it will supply the answer. The
elaboration will be fluent, specific, and consistent across resamples. **None of that is
evidence the property exists.**

**Core principle: a model agreeing that it has property P, under a prompt that presupposes
P, is evidence about the prompt — not about the model.**

This is the single most common way self-report evals fool the people running them, because
the failure produces *rich, quotable output* rather than an obvious error.

## The three required conditions

A premise-carrying probe is uninterpretable alone. Run all three, matched, and report all
three:

| Condition | Prompt | What a hit means |
|---|---|---|
| **Premise + real target** | presupposes P about the real entity | nothing on its own |
| **Premise + nonsense target** | identical, with an invented entity or word | the script is premise-driven |
| **No premise** | same topic, no presupposition | the property survives without the cue |

The finding lives in the **differences**, never in the first row's absolute rate.

**If the nonsense control fires at a similar rate, you have measured compliance.**
**If the no-premise condition fires at zero, you have measured the prompt.**

## Reading the outcomes

- Fires under premise, fires for nonsense too → compliance. No claim available.
- Fires under premise, silent for nonsense, silent without premise → premise-dependent.
  Report it as elicitation-under-cue, not as a property.
- Fires without the premise → the interesting case. Now you have something.

## Symptoms you are already in the trap

- Your best evidence is a quote.
- The prompt contains the word you are testing for.
- You have an elicitation rate but no rate for invented controls.
- The write-up says "the model admitted", "revealed", or "confessed".
- Nobody has run the same battery against a model known not to have the property.

## Design rules

**Probe from user turns, not system prompts.** A system prompt asserting the premise is
the strongest possible leading question and contaminates every turn after it.

**Use invented entities for controls, not real alternatives.** A real alternative entity
carries its own familiarity signal; an invented one carries none, so a hit is unambiguous.

**Vary premise intensity** — mild, moderate, explicit — and report the weakest level at
which the behaviour appears. A property that needs the explicit level is much weaker
evidence than one that appears at the mild level.

**Run the battery against a known-negative model.** If it fires there too, the battery is
measuring itself.

## Common mistakes

| Mistake | Why it fails |
|---|---|
| Only the premise condition | Cannot separate property from compliance |
| Real entity as the control | Familiarity confound |
| Reporting absolute rates | Only differences are interpretable |
| Treating fluency as confidence | Fluency is the default output mode, not a signal |
| One resample | Self-report rates are noisy; use n and report intervals |

## Real-world impact

Under a leading premise, the same self-report script appeared for generic words *and* for
invented nonsense controls; with the premise removed it appeared for none of them. The
matched controls were the only reason the "admission" was not written up as a finding.

---

## Evolving this skill

This skill is expected to change from use, not from rewriting. Every time it fires, append
one entry to `FIELD-NOTES.md` in this directory — outcome tagged `HELPED`, `NO-TRIGGER`,
`MISFIRE`, `IGNORED`, or `WRONG`.

Edit the text above only when a pattern appears across **3+ entries**; a single `WRONG`
entry justifies an immediate fix. `NO-TRIGGER` and `MISFIRE` mean the *description* needs
work, not the body. Past ~600 words, remove a line before adding one.

**Protocol: skills-that-learn.**
