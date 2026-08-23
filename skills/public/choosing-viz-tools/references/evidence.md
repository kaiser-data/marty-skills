# Evidence

Why the rankings are ordered the way they are. Read only when a pick is challenged or the case is unusual.

## Ranked use cases, with evidence
 — which tool for which job

Ranked picks per job. Dataset metrics say who is *healthy*; the notes and evidence column say who is *right for the job*.

| Use case | 🥇 First pick | 🥈 Second | 🥉 Third | Evidence / note |
|---|---|---|---|---|
| **Standard business charts in a web app (line/bar/pie)** | `Chart.js` — smallest sane default, trivial API | `apexcharts.js` — better-looking defaults, still simple | `frappe/charts` — ~14 KB when weight is the constraint | Chart.js is ~60 KB (≈14 KB tree-shaken for basic charts) and covers the common types; reach further only when it fails you. |
| **Charts in a React app with minimal effort** | `recharts` — the idiomatic React default | `nivo` — nicer defaults, canvas variants available | `tremor` — whole dashboard UI, not just charts | Consensus 2026 guidance: Recharts as the practical React default; switch to canvas-based libs when volume bites. |
| **Dense dashboards / 10k+ points in the browser** | `echarts` — canvas renderer, millions of points | `uPlot` — ~50 KB, fastest time-series render | `perspective` — WASM engine for millions of streaming rows | Chart.js and SVG libraries (Recharts, ApexCharts) degrade noticeably above ~10k points; ECharts is documented at 10M+. |
| **Fully bespoke, one-of-a-kind visualization** | `d3` — total control, the reference implementation | `visx` — D3 maths with React rendering | `G2` — grammar-based composition in TS | D3 is a toolkit, not a chart library — budget for building axes, legends, and accessibility yourself. |
| **Financial / trading charts** | `lightweight-charts` — purpose-built, ~45 KB, streaming | `highcharts` — Highstock package, commercial licence | `echarts` — candlestick support, free | Lightweight-charts gives trading-desk interaction feel; indicators are in TradingView's paid Charting Library, not this one. |
| **Large-scale geospatial visualization** | `deck.gl` — GPU layers, millions of features | `kepler.gl` — ready-made app on top of deck.gl | `echarts` — adequate for modest geo overlays | deck.gl is the library; kepler.gl is the app — pick by whether you're building or exploring. |
| **Publication-quality static figures (Python)** | `matplotlib` — the publication standard, vector output | `plotnine` — ggplot2 grammar, matplotlib backend | `lets-plot` — grammar + good geospatial | Journals expect vector PDF/EPS; all three deliver it. Choose by API taste, not capability. |
| **Exploratory analysis in a notebook** | `plotly.py` — Plotly Express, one-line interactive charts | `altair` — concise grammar with linked selections | `holoviews` — re-plot repeatedly with minimal code | Altair embeds data in the spec — use vegafusion or URL data for large frames. |
| **Zero-code exploration of a DataFrame** | `pygwalker` — Tableau-style drag-and-drop in one line | `dtale` — deep pandas inspection + code export | `panel` — when it needs to become an app | EDA tools, not production charting — expect to rewrite the final chart properly. |
| **Charts described as data (spec-driven / LLM-generated)** | `vega-lite` — portable JSON spec, the LLM-friendly format | `vega` — when Vega-Lite's ceiling is reached | `mcp-mermaid` — agent-callable diagram/chart tool over MCP | Vega-Lite specs are diffable JSON, which makes them the most reliable target for model-generated charts. |
| **ML model demo with a UI in an afternoon** | `gradio` — purpose-built for model demos + Spaces | `streamlit` — more general, better charting | `dash` — if it will outlive the demo | Gradio's image/audio/chat components are why it wins here; its charting is weaker than Streamlit's. |
| **Python data app that must survive production** | `dash` — explicit callbacks, Flask deployment | `reflex` — compiles to React, real app architecture | `taipy` — per-user state + scenario orchestration | Streamlit's rerun-everything model is the documented pain point at scale; all three fix it differently. |
| **Self-service BI for non-technical users** | `metabase` — easiest adoption, question builder | `superset` — richer viz, heavier to run | `redash` — simplest if everyone writes SQL | 2026 comparisons converge on Metabase for usability, Superset for depth — Redash is effectively in maintenance mode. |
| **Warehouse-scale BI for a technical data team** | `superset` — 40+ viz types, RLS, caching | `rill` — DuckDB speed, dashboards as code | `WrenAI` — governed text-to-SQL on top | Superset is the deepest self-hosted option; budget real operational effort for Celery/Redis/upgrades. |
| **Dashboards reviewed in git (BI as code)** | `evidence` — SQL + markdown → static data site | `rill` — dashboards as YAML, local-first | `grafana-foundation-sdk` — typed Grafana dashboards in 5 languages | All three trade point-and-click authoring for reviewability — non-technical self-service is the cost. |
| **Infrastructure metrics & alerting** | `grafana` — the standard; ~200 data sources | `openobserve` — single binary, logs+metrics+traces | `kibana` — if the data already lives in Elastic | Grafana remains the leading choice for live metrics and alert-driven dashboards. |
| **Log-centric troubleshooting** | `kibana` — Discover/Lens/ES\|QL over Elasticsearch | `openobserve` — much cheaper storage, younger | `grafana` — via Loki, if already on Grafana | Kibana is strongest when logs and search are central — and only really useful with Elastic behind it. |
| **Natural-language questions → charts (for people or agents)** | `WrenAI` — governed semantic layer over text-to-SQL | `rill` — explicitly designed for agent-driven BI | `metabase` — safest fallback: a guided question builder | The failure mode is confidently wrong SQL — the semantic layer, not the model, is what makes this safe. |
| **Internal tool with charts *and* write actions** | `ToolJet` — low-code CRUD + charts + 50 connectors | `reflex` — code-first alternative, full control | `taipy` — when scenarios/what-if are involved | Dashboards are read-only; if users must also edit data, a BI tool is the wrong shape. |
| **Charts in a desktop .NET application** | `ScottPlot` — the clear .NET winner, millions of points | — | — | No serious open-source competition in .NET desktop plotting; ScottPlot supports WinForms/WPF/Avalonia. |
| **Charts in a native iOS / macOS app** | `AAChartKit` — broad chart coverage — check the Highcharts licence | `core-plot` — truly native Core Graphics, dated API | — | Apple's own Swift Charts now covers most common cases natively — reach for these only for chart types it lacks. |
| **Charts from a Go or C++ service (no browser)** | `gonum/plot` — Go, vector output, no CGo | `matplotplusplus` — C++17, matplotlib-shaped API | — | Both are static-image generators with low maintenance signal in this snapshot — vendor or pin them. |
| **Presentable tables (not charts) in a report** | `great-tables` — publication-quality display tables in Python | — | — | Frequently the actual requirement behind 'make me a chart' — a table that reads well beats a weak chart. |
| **Architecture & flow diagrams (not data charts)** | `excalidraw` — fastest sketching, hand-drawn feel | `drawio-desktop` — formal notations, exhaustive shape libraries | `beautiful-mermaid` — text-defined, git-diffable diagrams | Diagrams are drawn, not data-bound — a different job from every other row in this table. |

## Licensing traps


The one dimension that silently disqualifies an otherwise-correct choice:

- **`highcharts` is proprietary for commercial use.** It is genuinely excellent — especially its accessibility module — but it is a per-developer paid licence, not an open-source dependency.
- **`AAChartKit` wraps Highcharts**, and therefore inherits that licence for commercial apps. This is the most commonly missed trap in the table above.
- **`grafana` (AGPL) and `metabase` (AGPL)** are open-core: self-hosting is free, but SSO, fine-grained permissions, and some embedding features are enterprise-only.
- **`kibana`** is under the Elastic Licence / SSPL, which is not OSI-approved and is rejected by some corporate policies outright.
- **`apache/echarts` and `apache/superset`** are Apache-2.0 with no feature gating — the safest picks in their respective rows if licensing is the binding constraint.

## Spotlight: the SVG/canvas line, and why most chart choices go wrong

Almost every 'our dashboard got slow' story in this landscape is the same story: an SVG-based library asked to draw more marks than the DOM can carry.

- **SVG libraries** (`Recharts`, `ApexCharts`, `nivo`'s SVG variants, `frappe/charts`, `c3`) create one DOM node per mark. That is wonderful for styling, CSS transitions, and accessibility — and it falls over somewhere between 5k and 10k points.
- **Canvas libraries** (`Chart.js`, `ECharts`, `uPlot`, `nivo`'s canvas variants, `ScottPlot`) draw pixels. You lose per-element CSS and easy hit-testing; you gain one to two orders of magnitude of headroom. `ECharts` documents rendering at 10M+ points.
- **GPU/WASM** (`deck.gl`, `perspective`) move the work off the main thread entirely. This is the only tier that survives millions of *streaming* rows, and it costs real architectural complexity.

The practical rule: **decide the data volume before the library.** Retrofitting a canvas renderer into a component tree built around SVG charts is close to a rewrite. The second rule: **downsample before you upgrade** — `uPlot`-class performance on aggregated data usually beats GPU rendering on raw data, and it's far less code.
