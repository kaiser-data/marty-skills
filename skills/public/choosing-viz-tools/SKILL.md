---
name: choosing-viz-tools
description: Use when picking a charting library, dashboard tool, BI platform, or visualization framework — "which chart library should I use", "what should I build this dashboard in", "how do I visualise this data", "best tool for a board deck / trading chart / geospatial map / notebook plot", or when a tool is already chosen and you want it sanity-checked against the case. Recommends from 61 curated tools with maintenance signals; it does not write chart code.
---

# Choosing visualization tools

Recommend a tool for a specific visualization or dashboard case. **Recommend and
justify — do not scaffold or write chart code.** Stop at the verdict.

The answer depends on the business case, not the chart type. "Bar chart of
revenue" resolves to `great-tables` for a board deck, `metabase` for analyst
peers, and `d3` for a public-facing piece. Route before you pick.

## Procedure

1. **Infer the dimensions** from what the user said. Do not interrogate — "board
   deck" alone gives you audience, surface, volume and effort. Ask at most one
   question, and only when the answer would change the pick.
2. **Match a job row** below → shortlist of 2–3. If nothing matches, read
   `references/tools.tsv` (~1,200 tokens) and route on attributes instead.
3. **Pull detail for the shortlist only** — never read that file whole (8k tokens):
   ```
   awk '/^## (owner\/repo|owner\/repo2)$/,/^$/' references/detail.md
   ```
4. **Apply the maintenance rule** (below), then answer in the output shape.

## Dimensions

| | |
|---|---|
| **Job** | one chart · dashboard · report/deck · exploration · diagram |
| **Author** | dev in code · analyst in SQL · business user clicking · LLM/agent |
| **Surface** | browser app · notebook · desktop/native · static site or PDF · mobile |
| **Volume** | <10k · 10k–1M · >1M / streaming |
| **Ops** | it's a dependency · it's a platform you run |
| **Licence** | permissive only · AGPL/open-core fine · commercial budget |
| **Effort** | hours · days · weeks (bespoke) |
| **Audience** | executive/board · analyst peers · developers · non-technical self-serve · public/press |

**Audience overrides chart type.** board → few numbers, static, PDF-exportable,
interaction is a liability · analysts → filters and drill-down · developers →
operational dashboards and alerting · non-technical → a question builder, not a
library · public/press → design control, bespoke.

**Effort is a constraint, not a preference.** hours → `gradio`, `metabase`,
copy-paste components · days → `echarts`, `superset`, `dash`, `rill` · weeks →
`d3`, `visx`, `deck.gl`; spend this only when the design *is* the point.

**Volume has a cliff.** SVG renderers (Recharts, ApexCharts, Chart.js) degrade
past ~10k points; above that you need canvas or WASM.

## Jobs → shortlist

<!-- GENERATED:JOBS -->
```
standard web charts (line/bar/pie)  Chart.js= > apexcharts.js > frappe/charts✗
react app, minimal effort           recharts > nivo > tremor✗
dense dashboard, >10k points        echarts > uPlot= > perspective
bespoke / one-of-a-kind             d3= > visx > G2
financial / trading                 lightweight-charts > highcharts > echarts
geospatial, large scale             deck.gl > kepler.gl > echarts
publication figures (Python)        matplotlib= > plotnine > lets-plot
notebook exploration                plotly.py > altair > holoviews
zero-code DataFrame poking          pygwalker > dtale~ > panel
spec-driven / LLM-generated         vega-lite > vega > mcp-mermaid~
ML demo UI in an afternoon          gradio > streamlit > dash
Python data app, production         dash > reflex > taipy~
self-service BI, non-technical      metabase > superset > redash~
warehouse-scale BI, data team       superset > rill > WrenAI
BI as code, git-reviewed            evidence~ > rill > grafana-foundation-sdk
infra metrics & alerting            grafana > openobserve > kibana
log troubleshooting                 kibana > openobserve
natural-language → charts           WrenAI > rill > metabase
internal tool, charts + writes      ToolJet > reflex > taipy~
desktop .NET                        ScottPlot
native iOS / macOS                  AAChartKit~ > core-plot~
Go / C++ service, no browser        gonum/plot= > matplotplusplus~
presentable tables, not charts      great-tables
architecture / flow diagrams        excalidraw > drawio-desktop > beautiful-mermaid~
```

`✗` Stalled — never a first pick.  `~` Slowing — usable, pin it.  `=` Stable — finished, not dead.
<!-- /GENERATED:JOBS -->

## Maintenance rule

A low health score means opposite things for a finished library and a dead one.
The labels above carry that judgment; the dataset alone cannot.

- **Stalled `✗` → never a first pick.** Say why, and promote the next option.
- **Slowing `~`** → can still win. Flag it and say "pin the version".
- **Stable `=`** → not a concern. Say *finished, not dead* if the user
  questions the low activity.

This is the only place maintenance overrides fit. Everywhere else, fit leads.

## Output shape

```
CASE   <one line restating the case>
ROUTED <the dimensions you inferred, and what you assumed>

▶ PICK   owner/repo  ★stars · licence
         <why it fits this case in one line>
         MAINTENANCE  <label + consequence, only if not Active>

  ALT    <second> — <the trade-off vs the pick>
  ALT    <third>  — <the trade-off vs the pick>

  TRAP   <licence, perf cliff, or effort surprise>
  NOT    <a tool they might expect, and why it's wrong here>
```

Close with the data vintage so a stale recommendation is visibly stale.

## Rules

- **State assumptions.** You inferred the dimensions — say which, so they can
  correct you.
- **Name the gap.** If the corpus has no good answer, say so rather than
  promoting a weak local match. A workaround presented as a fit is the worst
  failure mode here.
- **Licence disqualifies silently.** `highcharts` and `AAChartKit` are
  commercial; `grafana` and `metabase` are AGPL open-core; `kibana` is SSPL.
- `references/evidence.md` (2.5k tokens) only when a pick is challenged.

## Sources

Baked from `github-stars-analyzer` — capability prose from
`reports/charting-stack.md`, metrics from `data/classified.json`. Refresh:
`python3 scripts/build_viz_skill.py` in that repo.

Capability claims are **not** README-scraped: that method reports Chart.js as an
SVG renderer (it is canvas-only) by matching shields.io badge URLs.
