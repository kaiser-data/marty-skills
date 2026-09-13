# Field notes — seed-replicates-before-effects

Append-only evidence log. Protocol: **skills-that-learn**. One entry per firing.
Append always; edit `SKILL.md` only when a pattern appears across 3+ entries — except
`WRONG`, which justifies an immediate fix.

Tags: `HELPED` · `NO-TRIGGER` · `MISFIRE` · `IGNORED` · `WRONG`

---

## 2026-08-14 · secret-loyalities · WRONG
Trigger: a 14-cell grid was launched and read at n=1 per cell before any replicate existed.
Outcome: five later replicates of the anchor spanned 38.30-52.44% activation, straddling a 50% gate. Most between-cell contrasts in that grid were retroactively uninterpretable.
Gap: the skill did not exist yet - this entry IS the origin evidence. Replicates must precede the grid, not follow it.

## 2026-09-13 — HELPED (domain stretch)
Fired outside the intended domain: no seeds, no training, no sampling. A single
subagent-driven-development run, and the user asked to publish findings from it.
The skill's seed-spread gate does not literally apply, but "measure the denominator
before claiming the effect" carried over intact and changed the write-up materially:
turned "0 code defects in 14 review passes" into "0/14, Wilson 95% CI 0-22%", and
"all 6 defects were plan defects" into an interval with an explicit n=1 caveat. The
"distinguish the two n's" section was the most load-bearing part — 7 tasks in one
plan read like 7 replicates and are not; they share a plan, a repo, a controller and
a model family. Suggest the description mention non-stochastic single-run censuses,
where the same conflation (cells vs replicates) occurs without any RNG involved.
