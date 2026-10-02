# Field notes — detection-needs-a-denominator

Append-only evidence log. Protocol: **skills-that-learn**. One entry per firing.
Append always; edit `SKILL.md` only when a pattern appears across 3+ entries — except
`WRONG`, which justifies an immediate fix.

Tags: `HELPED` · `NO-TRIGGER` · `MISFIRE` · `IGNORED` · `WRONG`

---

## 2026-08-14 · secret-loyalities · HELPED
Trigger: an audit target resolved to 0 of 339 shared tensors changed - a surprise clean negative.
Outcome: became the only ground truth in the project; every threshold calibrated against it plus a base-vs-base self-check.
Gap: nothing. Worth watching: whether 'surprise negative is the most valuable artifact' generalises.

## 2026-09-25 — HELPED
GLiClass vs keyword relevance for github-stars-analyzer discovery. Negatives came from repos held by unrelated reports (far) and non-overlapping AI reports (near), with the threshold calibrated on half the negatives at 10% FPR. Tied discrete keyword scores pushed the measured FPR to 24% at the "10%" threshold, which was visible only because the FPR was reported. The shuffled-label self-check came out at about 0.5 as it should.

- 2026-09-26 HELPED — jev-studies D2: ran the scoring pipeline on random scores first (null self-check, AUROC ≈0.5 on every head) and kept thresholds calibrated on the benign calibration split, with no fitting on the 37 positives in the primary combiner.
