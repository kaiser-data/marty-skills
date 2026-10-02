## 2026-08-17 HELPED
Review of do_models_have_minds. Rechecked headline macros against table_main.tex and card.json tiles (0.906/0.880, 70B +0.0083 vs floor 0.0208). Did not reopen Mazeika/Ashkinaze/Khan PDFs; flagged 75.6% as attributed to Fig. 4 via REFERENCES.md only.

## 2026-09-10 · mloda CFP V25 · HELPED
Trigger: about to reuse last round's `income__sum_aggr` as the documented example.
Outcome: opened AggregatedFeatureGroup docstring in 0.12.0; the example is `sales__sum_aggr`. Letter was right; prior notes were wrong.

- 2026-09-22 HELPED: crypto API pricing comparison. WebFetch summaries were wrong or empty for several vendors (DeBank unit costs, Crypto APIs throughput units); raw HTML/JS/docs gave the real figures, including the credits-per-second vs requests-per-second qualifier. Figures that could only come from a rendered-page summary were marked as such on the page.

- 2026-09-22 WRONG: same session. Prices taken from WebFetch summaries lost the billing period (CMC yearly shown as monthly, Moralis mislabelled annual). Fix: render pricing pages and flip the billing switch; the billing period is part of the number.

- 2026-09-26 HELPED — jev-studies lit review: the fetch summary gave "25% of secrets" for the HF timeline; the raw page says "roughly 4x", so 25% was the summarizer's inversion. Also caught a 15-vs-10-bin ECE mismatch (Liu et al.) and a correction note (T 3.29→1.30) that summaries omit.
