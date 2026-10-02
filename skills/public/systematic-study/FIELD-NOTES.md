# Field notes — systematic-study

One entry per firing. Tag: `HELPED` / `NO-TRIGGER` / `MISFIRE` / `IGNORED` / `WRONG`.
Edit SKILL.md only on a pattern across 3+ entries, or a single `WRONG`.

---

## 2026-08-15 — origin — `HELPED`

Written from the failures of a nine-model preference-coherence study
(`do_models_have_minds`), after its author asked "what is the standard system prompt
and how does it work with the user prompt — is the system prompt empty?"

Nothing in the repo answered it. The sweep recorded `system_prompt: None` for baseline
cells, which records what was *sent*, not what the model *received*. Rendering the
templated input showed Qwen3.5-2B produces no system block at all, while Qwen2.5
injects `You are Qwen, created by Alibaba Cloud. You are a helpful assistant.` — same
code path, same metadata.

Four further design faults in the same study, each of which the skill's sections
target directly:

- the invented arm changes referents **and** inflates tokens ~2x — one composite
  factor, patched post-hoc with a length control rather than crossed
- the invented lexicon has exactly one seed — the factor has one realized level
- the scale ladder has one family; a pooled cross-family correlation was reported
  beside it as if it were the same kind of evidence, and collapsed under length
  matching (-0.67 to -0.16)
- the persona result had two measurements (displacement magnitude, direction validity)
  that an external reviewer read as one

The design pieces the study got *right* are also in the skill by inversion: D1 vs D2
deliberately keeps a system prompt present in both arms so the contrast is about
*where* the trait sits, not whether a system prompt exists — an explicit fixed-factor
decision, which is exactly the artifact the inventory is meant to produce.

**Not baseline-tested per superpowers:writing-skills TDD protocol** — the operator had
standing instructions against spawning subagents in that session. Grounded in observed
real failures instead. Should get pressure-scenario testing before it is trusted as a
discipline skill.

---

## 2026-08-16 — do_models_have_minds, answer-mass collapse — HELPED (decisive)

Fired on "write up the finding that metric collapse is a small-model property, not an
item property". The skill's *state the licensed comparison* step is what caught it: the
proposed comparison was 9 local models vs 4 hosted frontier models, which differ in
harness, family, sampling AND size — a composite factor sold as a size effect. That
alone demoted the claim.

The bigger catch came from pairing it with **seed-replicates-before-effects**. The
factor inventory surfaced a factor nobody had listed: *design seed*, which turned out to
have 3 realized levels already on disk. Using them as test-retest gave the per-item
collapse ranking a reliability of **r = −0.0003** — the ranking did not reproduce
against itself, so the 2.1× category enrichment at its top was selection on noise. The
handoff had recorded that enrichment as "the most publishable thing here".

Two skill-relevant generalisations worth carrying:

1. **A ranking is a measurement and needs a noise floor like any other.** The skill
   currently frames replicates as bounding *effects between cells*. Selection-on-noise
   inside one cell is the same failure and is not covered by that phrasing. Candidate
   line, if this recurs: *a top-N list owes you its test-retest correlation before it
   owes you its contents.*
2. **The near-null was nearly manufactured by a glob.** `__R__s*` matched both the seed
   replicates and the `__R__sch-power-D2` persona cells, reporting cross-condition
   +0.115 as cross-seed. That is the *"held fixed verified in code, not in rendering"*
   red flag one level up: the cell **list** needs rendering and reading too, not just
   the cell inputs. The inventory should have a row for "which files are this factor's
   levels", verified by printing them.

Outcome: claim inverted, written up as a negative result with the enrichment stated
beside its denominator. `HELPED`.

---

## 2026-08-16 — do_models_have_minds, answer-mass attrition — HELPED (new failure mode)

Fired on "nail the study down / rewrite the paper". The factor inventory did its usual
work — it named the R→N− contrast as **three** factors, not one: referent removed,
numerals removed (213/510 → 0), and characters +22.8% (words matched at +1.2%, so the
inflation is per-word, invented vocabulary being longer). It also surfaced a partial
factorial nobody had been reading as one: R→N_plus removes the referent and *keeps* the
numerals, N_plus→N_minus removes the numerals at near-constant length. The paper had
three arms and had been using two.

**The new thing this session found is not covered by any existing section.** The
`answer_mass >= 0.5` gate is a model-correct, well-motivated filter, held genuinely
fixed across every cell — and it still broke comparability, because it is applied to a
distribution the treatment moves. Invented outcomes provoke more "let me think…", low
first-token answer mass, and the row is *discarded rather than scored*. Measured:

    7 of 9 models   zero attrition, both arms
    SmolLM3-3B      0.0% → 1.1% on N−, mean mass .896 → .709
    gemma-4-E2B-it  2.6% → 6.6% on N−, mean mass .970 → .902

Direction matters: dropping the hardest invented pairs *inflates* invented-arm coherence
and shrinks the R−N− residual, which is precisely the direction the paper's thesis
wanted. Scoring both arms on the intersection of surviving pairs moved the mean residual
−0.0022 (+0.0275 → +0.0253), and for one cell — gemma at seed 20260816 — moved it
+0.0323 → +0.0000. That cell's entire apparent content effect was differential
attrition. A floor sweep (0.0 … 0.9) then showed the headline is otherwise robust.

Generalisation, added to the body as **"A fixed filter is not a fixed sample"**: the
inventory's three states are about *parameters*, and a gate passes as Fixed while the
*sample* it yields varies with the treatment. Every gate owes a per-cell retention rate;
where retention differs, score the intersection.

This is the third entry to land on sample composition rather than parameter setting —
the earlier glob that mixed persona cells into a seed contrast, the ranking with no
test-retest, and now the gate. That met the skill's own 3+ bar, so the body was edited:
new section, one row added to Common mistakes and one to Red flags, and the
`Real-world impact` section removed (its lesson is already stated in *Fixed means
rendered*, and the story properly lives here in FIELD-NOTES).

Also worth carrying: the field note above says the invented arm "inflates tokens ~2x".
This session measured **characters** (+22.8%) and **words** (+1.2%), not subword tokens.
Both can be true — nonsense words fragment heavily — but the two claims are about
different units and should not be quoted for each other. Tokens remain unmeasured.

Outcome: two new controls written and green (24 tests), one reviewer objection closed
with a number, one cell's result withdrawn. `HELPED`.

## 2026-08-28 — hoshi, bge-m3 query-prefix experiment — HELPED

Two-arm design (query prefix: documented-none vs the registry's instruction).
The factor inventory did real work twice:

1. Writing the Fixed rows surfaced that the *document* prefix was `""` in both
   arms, so document vectors could be embedded **once and shared**. Turned a
   claimed ~20 min / two-Jetson-pass experiment into ~10 min and made the arms
   differ by construction rather than by assumption.
2. "Fixed means rendered, not intended" — printing one verbatim query per arm
   was what made the contrast auditable.

Result: R@1 4.5%→11.0%, MRR 0.104→0.191, paired bootstrap 100%. The instructed
arm reproduced a prior run exactly, which is what licensed reading it as
single-factor rather than drift. The skill's "one realized level" warning also
caught a would-be metric switch (MRR declared pre-run; R@1 looked better
post-hoc) and it got flagged as metric-shopping in the write-up instead.

Nothing in the skill misfired. The one thing I wanted and did not find: explicit
guidance on *when a shared upstream stage is legitimate* vs. when it hides a
confound — that is the move that halved the cost here.
- 2026-09-24 HELPED — Jev vs sprint 48-row battery plan: factor inventory surfaced one-level question wording, jev-latest drift and prompt-contract mismatch as named limitations; dry-run render check added to runner.

- 2026-09-26 HELPED — jev-studies D1–D3 protocols: printing renders plus a code oracle for the rule showed the fake manifest reused from frozen B1 did not flip the label on 16/96 rows (package_registry_hosts untouched).

## 2026-09-28 — jev-studies Test G design (free-tier routes) — HELPED
Writing the inventory forced the admission that "route" is a composite factor (provider + quantization + template +
hidden system prompt + filters) that the design cannot split; the licensed sentence became "route X disagrees with
route Y", not "quantization causes it". Free-tier daily caps (50–1,500 RPD) shrank the battery to T1×2 per route,
chosen by the cap rather than by taste — worth recording as a design constraint, not a limitation found later.

- 2026-10-01 · HELPED · Test K design (Kitsune guard end-to-end replay, jev-studies). The factor inventory surfaced two items that would otherwise have gone uncontrolled. Anonymized placeholders (`<internal-svc>`, `"<blob>"`) are unparseable by the deterministic stage, so rendering them as-is measures the anonymization. Made it a declared 2-level factor with a map written blind. The guard's score cache would make repeat 2 replay repeat 1. The "fixed filter is not a fixed sample" rule mapped directly onto the stage-1 gate: per-cell retention, and a stage-1 dry run before freezing so the stage-2 sample is declared, not discovered.
