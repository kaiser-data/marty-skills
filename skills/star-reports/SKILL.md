---
name: star-reports
description: Create, update, or regenerate landscape reports in the github-stars-analyzer report pipeline. Use when the user asks for a new report from the starred-repos dataset/graph, wants an existing report refreshed, extended, or ranked by task/use-case, asks how the reports pipeline works, or mentions reports/, scripts/reports/, build_index.py, or the app's Reports tab.
---

# Star-Reports Pipeline

Reports are **deterministic Python generators** over two local inputs — no API calls,
fully reproducible. Each generator curates a repo taxonomy by hand and renders
markdown + a meta sidecar; `build_index.py` orchestrates everything.

## Data flow

```
data/classified.json  ─┐  (repo metrics: stars, health, lifecycle, bus_factor…)
public/data/graph.json ┴→ scripts/reports/<slug>.py → reports/<slug>.md + <slug>.meta.json
                                                      └→ build_index.py →
                                                         charts injected (reports/assets/*.svg)
                                                         copies to public/reports/
                                                         public/reports/index.json (Reports tab)
data/snapshots/*.json  — one per data vintage; powers the ▲/▼ star-trend deltas
```

## Adding a new report

1. **Scan the dataset for candidates** before curating — keyword match over
   `full_name + description + topics` of `data/classified.json` repos. Pick
   ~25–40 repos; verify every curated name exists in the dataset. Watch for
   **name collisions** in the scan (e.g. `tk04/Marker` is a markdown editor,
   unrelated to `datalab-to/marker`) — check descriptions, not just names.
2. **Copy an existing generator as the template** — `rag_tooling.py` is the
   canonical one; `document_extraction.py` is the reference for reports with
   evidence-backed task rankings. Keep the house structure:
   - `TAXONOMY = {"owner/repo": ("Category", "one-line blurb"), …}` (curated by hand)
   - `ADJACENT = [(name, why-excluded), …]` — overlaps routed to sibling reports, kept honest
   - Sections in order: executive summary → pipeline/anatomy table → **Master
     comparison** table → per-category deep dives → optional spotlight/blueprint →
     graph analysis (communities, PageRank, inter-edges) → maintenance & risk →
     "Which one should you use?" → adjacent → methodology
   - Import shared helpers from `lib.py`: `fmt_stars` (star count + trend marker),
     `fmt_int`, `days_to_human`, `activity_label`, `make_node_for`, `CLASSIFIED`, `GRAPH`
   - Write `reports/<slug>.md` and `reports/<slug>.meta.json` (keys: slug, title,
     file, category, summary, tool_count, total_stars, categories, top_tools,
     snapshot, generated, generator)
3. **Register it** in the `GENERATORS` list in `scripts/reports/build_index.py`.
4. **Run the pipeline** (slow — snapshots + regenerates ALL reports; use a long timeout
   or background it):
   ```bash
   python3 scripts/reports/build_index.py
   ```
   For a quick iteration on one report only: `python3 scripts/reports/<slug>.py`
   (skips charts/index/public copy — always finish with a full `build_index.py` run).
5. **Verify**: generator prints `tools: N / N curated` with **no `WARNING missing:`
   line**; new slug appears in `public/reports/index.json`; chart SVGs exist in
   `reports/assets/<slug>-*.svg`; spot-check the markdown tables render (column
   counts must match the header — historic bug source).

## Task-ranked reports (web-research-backed)

When the user wants tools **ranked per task/use-case** (not just compared), use the
`document_extraction.py` pattern:

- A `TASK_RANKINGS = [(task, [(repo, note) × 3], evidence), …]` table rendered as
  `| Task | 🥇 First pick | 🥈 Second | 🥉 Third | Evidence / note |`.
- **Gather evidence via web search at authoring time** (benchmarks, head-to-head
  comparisons, vendor papers), then bake the findings into the generator as frozen
  text — generation itself stays deterministic and offline.
- Cite sources + retrieval date in Methodology, and flag that benchmark numbers are
  point-in-time / partly vendor-reported.
- **Keep rankings honest against the dataset**: if a ranked pick reads as
  Abandoned/stale in the snapshot (e.g. a top pick that stopped shipping), say so in
  the ranking note or the maintenance section's watch items.
- Frozen benchmark text does NOT refresh with `build_index.py` — re-verify citations
  manually when major model/tool releases land.

## Pitfalls

- **Markdown tables**: every row must have the same column count as the header
  (`"|" + "---|" * N`). Mismatches render broken in the app.
- **Charts are injected once**: `inject_charts()` skips files already containing
  `](assets/` — regenerating the .md resets that, the next build re-injects.
- `top_tools` needs ≥3 entries and `categories` ≥3 non-zero buckets for both
  SVGs to be generated.
- Trend markers (▲/▼) only appear once ≥2 snapshots exist in `data/snapshots/`.
- Meta `category` groups reports in the UI — reuse an existing one
  (check `reports/*.meta.json`; currently includes AI / RAG, Agents, Apps,
  Comparison, Documents, Efficiency, Engineering, Evaluation, Infrastructure,
  MCP, OpenClaw, Voice) before inventing a new one.
- Don't hand-edit `reports/*.md` or anything in `public/reports/` — they're
  generated; edit the generator and re-run.

## Refreshing data (upstream of reports)

The weekly GitHub Action refreshes `data/classified.json`; locally the chain is
`scripts/ingest.mjs → classify.mjs → precompute.mjs`, then `build_index.py`
re-snapshots and regenerates every report against the new vintage.
