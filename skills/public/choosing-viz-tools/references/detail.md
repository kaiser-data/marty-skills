# Tool detail

One anchored entry per tool. **Never read this file whole** (~4,300 tokens) — pull only the tools on your shortlist:

```
grep -A6 '^## owner/repo' references/detail.md
```

## AAChartModel/AAChartKit
Native / systems charting · 4,766★ · Objective-C · MIT · **Slowing** — 92d since push, bus factor 0.
- ✅ Highcharts' chart quality inside a native app; declarative, chainable API; broad chart coverage; long-lived project.
- ⚠️ **Wraps Highcharts — inherits its commercial licence for commercial apps**; web-view rendering costs memory and startup time; slowing maintenance; Swift Charts now covers many cases natively.
- 🎯 Apple-platform apps needing chart types Swift Charts doesn't cover — check the licence first.
- 🚩 **Wraps Highcharts** and inherits its commercial licence. The most commonly missed trap here.

## airbnb/visx
React charting library · 21,000★ · TypeScript · MIT · **Active**
- ✅ You own the DOM and the design entirely; tree-shakes to only what you import; no chart abstraction to fight; excellent for design-system-native charts.
- ⚠️ Not a chart library — you assemble axes, scales, and tooltips yourself; substantially more code per chart; steeper ramp; you inherit D3's mental model anyway.
- 🎯 Bespoke, design-system-consistent charts in React where control beats speed.

## alandefreitas/matplotplusplus
Native / systems charting · 4,914★ · C++ · MIT · **Slowing** — 131d since push, bus factor 0.
- ✅ Familiar matplotlib-like API from C++; wide chart coverage for a C++ library; multiple backends and export formats; header-friendly CMake integration.
- ⚠️ Depends on gnuplot for rendering in the common setup; heavy build; **low health / slow maintenance** in this snapshot; small community.
- 🎯 C++ scientific and simulation code that must plot without leaving the process.

## antvis/G2
Web charting library · 12,581★ · TypeScript · MIT · **Active**
- ✅ Grammar-of-graphics composability without leaving JS; strong statistical transforms; part of the wider AntV suite (G6 graphs, L7 geo, S2 tables); good animation primitives.
- ⚠️ Documentation and community are largely Chinese-language; API churned hard across v4→v5; smaller Western ecosystem means fewer StackOverflow answers.
- 🎯 Teams that want ggplot-style composition in a TypeScript frontend.

## apache/echarts
Web charting library · 67,048★ · TypeScript · Apache-2.0 · **Active**
- ✅ Enormous chart catalogue (incl. sankey, treemap, graph, geo); canvas renderer handles hundreds of thousands to millions of points; built-in dataZoom/toolbox/theming; strong i18n and accessibility work; Apache governance.
- ⚠️ Large bundle (~1 MB full build) unless you hand-assemble tree-shaken imports; imperative `setOption` config object is verbose and weakly typed; docs and issues skew Chinese-first; React/Vue wrappers are third-party.
- 🎯 Dense enterprise dashboards and any chart type the small libraries don't have.

## apache/superset
BI & dashboard platform · 74,220★ · Python · Apache-2.0 · **Active**
- ✅ Rich visualization catalogue; genuine multi-tenant BI (roles, row-level security, caching); warehouse-scale via SQLAlchemy; Apache-2.0 with no feature gating.
- ⚠️ Heavy to deploy and operate (Celery, Redis, metadata DB); upgrades are notoriously involved; the semantic layer is weaker than commercial BI; steeper for business users.
- 🎯 Technical data teams that want warehouse-scale, self-hosted BI.

## apexcharts/apexcharts.js
Web charting library · 15,123★ · JavaScript · NOASSERTION · **Active**
- ✅ Attractive out-of-the-box styling and animations; good annotation and mixed-chart support; official React/Vue/Angular wrappers; MIT.
- ⚠️ SVG rendering caps practical dataset size well below canvas libraries; less flexible than D3 for custom marks; some advanced features are documented only by example.
- 🎯 Product dashboards that must look good with little design work.

## Avaiga/taipy
Data-app framework · 19,397★ · Python · Apache-2.0 · **Slowing** — 6d since push, bus factor 0.
- ✅ Per-user state isolation and an async backend (unlike Streamlit's rerun model); built-in scenario/pipeline management for what-if analysis; designed for business-facing apps.
- ⚠️ More code and more concepts than Streamlit for a simple app; smaller community and component ecosystem; the orchestration half is wasted if you only want a dashboard.
- 🎯 Business-facing Python apps with scenario/what-if workflows.

## bokeh/bokeh
Python plotting · 20,428★ · TypeScript · BSD-3-Clause · **Active**
- ✅ Python callbacks can run server-side (no JS required) via `bokeh serve`; strong streaming and large-data story (with Datashader); composable widgets; BSD-3.
- ⚠️ Heavier concepts than Plotly for simple charts; the server model adds deployment burden; smaller community and slower momentum than Plotly/Altair.
- 🎯 Streaming/live Python dashboards that need server-side callbacks.

## c3js/c3
Web charting library · 9,347★ · JavaScript · MIT · **Stable** — Effectively feature-frozen. Fine for codebases already on it — not a new-project choice.
- ✅ Simple declarative config over real D3 output; stable, small, easy to theme with CSS; still receiving maintenance commits.
- ⚠️ Effectively feature-frozen; built on D3 v5-era patterns; limited chart types; the problem it solved is now solved better by Observable Plot and ECharts.
- 🎯 Legacy codebases already on C3 — not a new-project choice.

## Canner/WrenAI
BI & dashboard platform · 17,179★ · Python · NOASSERTION · **Active**
- ✅ Semantic/context layer keeps LLM-generated SQL grounded and governed; answers arrive as charts, not just tables; MCP-friendly for agent workflows; very active.
- ⚠️ Accuracy still depends on modelling discipline — a bad semantic layer produces confidently wrong charts; requires an LLM provider (cost + data-egress questions); young category.
- 🎯 Letting non-analysts (or agents) ask questions of a governed warehouse.

## chartjs/Chart.js
Web charting library · 67,634★ · JavaScript · MIT · **Stable** — Mature and deliberately small in scope; the plugin ecosystem absorbs most feature demand rather than the core.
- ✅ Trivial learning curve; small (~60 KB, ~14 KB tree-shaken for basic charts); huge plugin ecosystem; framework-agnostic with well-maintained React/Vue bindings; MIT.
- ⚠️ Only ~8 core chart types; performance degrades noticeably past ~10k points; canvas output isn't selectable/exportable as vector; deep customisation means writing plugins.
- 🎯 Standard business charts (line/bar/pie/doughnut) at typical data volumes.

## core-plot/core-plot
Native / systems charting · 2,762★ · Objective-C · BSD-3-Clause · **Slowing** — Dated API and Apple's own Swift Charts now covers most of its ground natively.
- ✅ Genuinely native rendering (no JS bridge); fine-grained drawing control; BSD licence; long track record.
- ⚠️ Dated API from the pre-Swift era; slow maintenance; steep learning curve; largely superseded by Apple's Swift Charts for new work.
- 🎯 Legacy Apple codebases already using it.

## d3/d3
Low-level / high-performance · 113,436★ · Shell · ISC · **Stable** — Feature-complete and API-frozen since v7; the reference implementation everything else is built on. Low commit rate here means finished.
- ✅ Total expressive freedom; the scales/shape/geo/force modules are the reference implementations; modular (import only `d3-scale` if that's all you need); unmatched learning material.
- ⚠️ Very steep learning curve; you write and maintain everything including axes, legends, and accessibility; direct DOM manipulation clashes with React's model; slow to ship simple charts.
- 🎯 Custom, one-of-a-kind visualizations — and as a dependency of everything else.

## deliveryhero/grafyaml
Dashboards as code · 44★ · Python · Apache-2.0 · **Active**
- ✅ YAML is far more reviewable than Grafana's dashboard JSON; minimal tooling; easy to slot into existing CI; still maintained.
- ⚠️ Thin abstraction — you still need to know the underlying JSON model; small community; no type checking; limited to what the YAML mapping exposes.
- 🎯 Small teams wanting reviewable dashboards without adopting an SDK.

## elastic/kibana
BI & dashboard platform · 21,230★ · TypeScript · NOASSERTION · **Active**
- ✅ Unmatched for log/search exploration (Discover, Lens, ES\
- ⚠️ QL); tight security/APM/observability integration; mature alerting and ML jobs.
- 🎯 Only really useful with Elasticsearch behind it; heavy resource footprint; the SSPL/Elastic licence change still rules it out for some; the UI sprawls across many overlapping apps.
- 🚩 Elastic Licence / SSPL — not OSI-approved, and rejected outright by some corporate policies.

## evidence-dev/evidence
BI & dashboard platform · 6,838★ · JavaScript · MIT · **Slowing** — 174d since push, bus factor 0.
- ✅ Dashboards live in version control and review like code; markdown+SQL is fast to author; static output deploys anywhere; excellent for reproducible reporting.
- ⚠️ No point-and-click authoring — non-technical users can't self-serve; static build model doesn't fit ad-hoc exploration; smaller component library than mature BI tools.
- 🎯 Engineering-led reporting where dashboards should be reviewed like code.

## excalidraw/excalidraw
Diagrams & AI charts · 129,346★ · TypeScript · MIT · **Active**
- ✅ Effortless, genuinely fast sketching; hand-drawn style reads as 'draft' which encourages iteration; local-first with an open file format; embeddable library; huge adoption.
- ⚠️ Not a data-charting tool — no data binding whatsoever; the sketch aesthetic is wrong for formal documentation; collaboration/storage features push toward Excalidraw+.
- 🎯 Architecture sketches, whiteboarding, and diagrams-in-docs.

## frappe/charts
Web charting library · 15,088★ · JavaScript · MIT · **Stalled** — 405d since push, health 5.
- ✅ Tiny footprint and no dependencies; genuinely pleasant defaults; heatmap (GitHub-contribution style) built in; MIT.
- ⚠️ Small chart catalogue; sparse maintenance; no serious large-dataset story; limited interactivity beyond tooltips.
- 🎯 Weight-sensitive pages and simple embedded charts.

## getredash/redash
BI & dashboard platform · 28,739★ · Python · BSD-2-Clause · **Slowing** — Commits continue, but the project is widely read as being in maintenance mode — feature work has moved elsewhere.
- ✅ Extremely simple model (query → visualization → dashboard); 50+ data sources; low operational weight; good for SQL-fluent teams.
- ⚠️ Development has been slow since the Databricks acquisition; visualization options are thin; no semantic layer or modelling; effectively in maintenance mode.
- 🎯 SQL-fluent teams that want dashboards without a BI platform.

## gonum/plot
Native / systems charting · 2,963★ · Go · BSD-3-Clause · **Stable** — Low-churn Go plotting under the Gonum umbrella. Static output, little surface to break.
- ✅ Idiomatic Go with no CGo or browser needed; vector output (SVG/PDF/EPS); integrates with the Gonum numeric libraries; BSD-3.
- ⚠️ Static images only, no interactivity; limited chart types and styling; **low health and slow maintenance** in this snapshot; API is spartan.
- 🎯 Server-side chart image generation from Go without a JS runtime.

## gradio-app/gradio
Data-app framework · 43,311★ · Python · Apache-2.0 · **Active**
- ✅ Purpose-built for model demos (image/audio/chat components are excellent); instant public share links; deep Hugging Face Spaces integration; auto-generated REST API.
- ⚠️ Charting is an afterthought compared to Streamlit; not designed for traffic or complex multi-page apps; layout control is limited; app structure gets messy past a few screens.
- 🎯 ML model demos, chat UIs, and Hugging Face Spaces.

## grafana/grafana
BI & dashboard platform · 76,153★ · TypeScript · AGPL-3.0 · **Active**
- ✅ Best-in-class time-series dashboards and alerting; plugs into anything (Prometheus, Loki, SQL, Elasticsearch, cloud); huge dashboard library; excellent health/activity metrics in this dataset (see comparison table).
- ⚠️ Awkward for non-time-series BI (joins, drill-downs, pivots); dashboard JSON is painful to review in git without a codegen layer; AGPL core with enterprise features gated; query-language burden shifts to the data source.
- 🎯 Infrastructure, metrics, and any alert-driven operational dashboard.
- 🚩 AGPL open-core: self-hosting is free, but SSO and fine-grained permissions are enterprise-only.

## grafana/grafana-foundation-sdk
Dashboards as code · 248★ · PHP · Apache-2.0 · **Active**
- ✅ First-party and versioned against Grafana schemas; strong typing catches invalid dashboards at compile time; multi-language; actively maintained.
- ⚠️ Still maturing, with API churn between Grafana versions; more verbose than writing JSON for simple dashboards; you must track schema versions.
- 🎯 Teams standardising Grafana dashboards as reviewed, typed code.

## has2k1/plotnine
Grammar of graphics · 4,753★ · Python · MIT · **Active**
- ✅ If you know ggplot2, you already know it; excellent faceting and statistical layers; publication-grade static output via matplotlib; consistent, principled API.
- ⚠️ Static only — no interactivity; matplotlib backend means matplotlib's speed and styling constraints; smaller ecosystem than matplotlib/seaborn; slower on large frames.
- 🎯 Publication figures for anyone coming from R/ggplot2.

## highcharts/highcharts
Web charting library · 12,479★ · TypeScript · NOASSERTION · **Active**
- ✅ Best-in-class accessibility module (screen-reader sonification, keyboard nav); mature stock/maps/gantt packages; export server; enterprise support and long-term API stability.
- ⚠️ **Not free for commercial use** — proprietary licence with per-developer pricing; large bundle; the licence alone disqualifies it for many OSS/SaaS teams.
- 🎯 Regulated or accessibility-mandated products with budget for a licence.
- 🚩 **Proprietary for commercial use** — per-developer paid licence, not an open-source dependency.

## holoviz/holoviews
Python plotting · 2,901★ · Python · BSD-3-Clause · **Active**
- ✅ Extremely concise for exploratory work; backend-agnostic (same code → Bokeh or matplotlib); composes plots with `+` and `*`; pairs with Datashader for billion-point rendering.
- ⚠️ Heavy abstraction — debugging means understanding the backend anyway; sparse error messages; steep conceptual learning curve; small community.
- 🎯 Iterative exploratory analysis where you re-plot constantly.

## holoviz/panel
Python plotting · 5,731★ · Python · BSD-3-Clause · **Active**
- ✅ Backend-agnostic: embeds matplotlib, Plotly, Bokeh, Altair, Vega, and DataFrames alike; works inside notebooks *and* as a served app; mature templating.
- ⚠️ Large API surface with several overlapping ways to do things; documentation sprawl; smaller community than Streamlit; more concepts before the first app runs.
- 🎯 Python dashboards that must mix plotting libraries rather than commit to one.

## hustcc/mcp-mermaid
Diagrams & AI charts · 621★ · TypeScript · MIT · **Slowing** — 88d since push, bus factor 1.
- ✅ Gives agents a real diagramming capability over MCP; text-in/diagram-out fits LLMs perfectly; trivial to wire into Claude Code or any MCP client.
- ⚠️ Inherits every Mermaid limitation (layout quality, chart-type range); thin wrapper with **declining maintenance**; single-maintainer risk.
- 🎯 Letting an agent produce diagrams inside a conversation or doc pipeline.

## JetBrains/lets-plot
Grammar of graphics · 1,779★ · Kotlin · MIT · **Active**
- ✅ Same grammar from Python and Kotlin/JVM; genuinely good geospatial support; renders in Jupyter, Datalore, and Kotlin notebooks; actively developed by a funded team.
- ⚠️ Much smaller community than ggplot2/matplotlib; Kotlin-first documentation in places; fewer third-party extensions; another rendering stack to learn.
- 🎯 JVM/Kotlin data teams, and Python users who want ggplot without the R baggage.

## jgraph/drawio-desktop
Diagrams & AI charts · 62,495★ · JavaScript · Apache-2.0 · **Active**
- ✅ Exhaustive shape libraries (AWS/Azure/GCP/UML/BPMN/network); fully offline and local-file based; no account required; stable and battle-tested.
- ⚠️ Dated Electron UI; XML file format is unpleasant to diff; no data binding — diagrams are drawn, not generated from data; manual layout work.
- 🎯 Formal architecture, network, and process diagrams that must follow a notation.

## K-Phoen/grabana
Dashboards as code · 729★ · Go · MIT · **Stalled** — 453d since push, health 6.
- ✅ Pleasant Go builder API and a YAML DSL; good fit for Go-based platform tooling; supports alerts as code.
- ⚠️ **Reads as abandoned in this snapshot** (no pushes in well over a year); trails current Grafana schema; the official Go Foundation SDK now covers the same ground.
- 🎯 Existing Go dashboard pipelines only — not a new-project choice.

## Kanaries/pygwalker
Python plotting · 15,932★ · Python · Apache-2.0 · **Active**
- ✅ `pyg.walk(df)` and you have pivot + chart exploration; no chart code at all; works in Jupyter/Streamlit/Colab; exports the resulting spec.
- ⚠️ Exploration tool, not a production chart library; struggles on very large frames without a compute backend; the free tier nudges toward the commercial Kanaries cloud.
- 🎯 Fast visual EDA on a DataFrame before writing any chart code.

## keplergl/kepler.gl
Low-level / high-performance · 11,959★ · TypeScript · MIT · **Active**
- ✅ No-code map analysis for large datasets; layer/filter/time-playback UI included; embeddable as a React component; exports configs as JSON.
- ⚠️ Opinionated app, not a library — customisation means forking behaviour; Redux-coupled embedding is awkward; maintenance has slowed since the Uber era.
- 🎯 Ad-hoc geospatial exploration without building a mapping app.

## leeoniya/uPlot
Low-level / high-performance · 10,400★ · JavaScript · MIT · **Stable** — Deliberately finished: a small, focused time-series renderer. But bus factor 0 — one author, no succession.
- ✅ Renders hundreds of thousands of points in milliseconds; ~50 KB with zero dependencies; memory-frugal; the benchmark other libraries are measured against.
- ⚠️ Deliberately narrow — time-series shapes only, no pie/treemap/geo; terse, low-level API; minimal built-in interactivity; you build the polish yourself.
- 🎯 Dense time-series panels and anything where render latency is the requirement.

## lukilabs/beautiful-mermaid
Diagrams & AI charts · 10,809★ · TypeScript · MIT · **Slowing** — 97d since push, bus factor 0.
- ✅ Text-defined diagrams mean git-diffable, LLM-generatable output; substantially better looking than stock Mermaid; drops into docs pipelines.
- ⚠️ Bound to Mermaid's syntax and layout engine (auto-layout is often mediocre); **declining maintenance signal** in this snapshot; presentation layer only.
- 🎯 Diagrams in docs and READMEs that should look designed.

## man-group/dtale
Python plotting · 5,213★ · TypeScript · LGPL-2.1 · **Slowing** — 19d since push, bus factor 0.
- ✅ Deep pandas-specific tooling (correlations, missing-value analysis, code export); shows the pandas code for each operation; runs from notebook, CLI, or Flask.
- ⚠️ Purely an inspection/EDA tool; heavy Flask app for what is often a quick look; not embeddable as a component; pandas-centric.
- 🎯 Interrogating an unfamiliar DataFrame in depth.

## matplotlib/matplotlib
Python plotting · 23,073★ · Python · no licence file · **Stable** — The Python publication standard, under NumFOCUS governance. Slow by design.
- ✅ Can draw literally anything; the publication standard for scientific figures; vector output (PDF/SVG/EPS); enormous documentation and 20 years of StackOverflow answers; PSF-style licence.
- ⚠️ Two competing APIs (pyplot state machine vs. object-oriented) confuse newcomers; verbose for anything non-trivial; dated defaults; no real interactivity; slow on large datasets.
- 🎯 Publication figures and any plot that must be exactly right.

## metabase/metabase
BI & dashboard platform · 48,666★ · Clojure · NOASSERTION · **Active**
- ✅ Fastest setup of any BI platform here; the notebook/question builder genuinely works for business users; good embedding story; sane defaults.
- ⚠️ Visualization catalogue is comparatively basic; complex analytical modelling hits a ceiling quickly; the useful embedding/SSO features sit behind the commercial edition (AGPL core).
- 🎯 Self-service BI where adoption by non-technical users is the deciding factor.
- 🚩 AGPL open-core: SSO, permissions and some embedding features are enterprise-only.

## observablehq/plot
Web charting library · 5,348★ · HTML · ISC · **Active**
- ✅ Extremely terse for exploratory charts; sensible statistical defaults (bins, stacks, facets); built on and interoperable with D3; ISC licence.
- ⚠️ Deliberately exploratory-first — less suited to pixel-exact product charts; interaction model is thinner than ECharts/Highcharts; smaller plugin ecosystem.
- 🎯 Fast exploratory charts in notebooks and internal tools.

## openobserve/openobserve
BI & dashboard platform · 20,592★ · TypeScript · AGPL-3.0 · **Active**
- ✅ Claims order-of-magnitude storage savings vs. Elasticsearch; single binary, trivial to run; logs + metrics + traces + dashboards in one product; very healthy activity in this dataset.
- ⚠️ Much younger and smaller ecosystem than Grafana/Kibana; fewer integrations and community dashboards; open-core with features reserved for the enterprise tier.
- 🎯 Small teams that want an all-in-one observability stack without Elastic's bill.

## perspective-dev/perspective
Low-level / high-performance · 11,099★ · Rust · Apache-2.0 · **Active**
- ✅ Handles millions of rows client-side via WASM + Apache Arrow; pivots, filters, and charts over streaming updates; works in the browser, Jupyter, and as a server.
- ⚠️ Heavy, unusual architecture (WASM binary + web components); steep conceptual ramp; overkill for static datasets; smaller community than mainstream charting.
- 🎯 Real-time, million-row analytical grids that must stay interactive in the browser.

## plotly/dash
Data-app framework · 24,373★ · Python · MIT · **Active**
- ✅ Explicit callback graph scales to genuinely complex apps; runs on Flask so it deploys like any WSGI app; the most 'production' of the Python options; mature enterprise story.
- ⚠️ Far more boilerplate than Streamlit; callback chains get hard to reason about; tied to Plotly for charting; the good enterprise features (auth, scaling) are commercial.
- 🎯 Production Python dashboards that outgrew Streamlit.

## plotly/plotly.js
Web charting library · 18,282★ · JavaScript · MIT · **Active**
- ✅ 40+ chart types including 3D, contour, and statistical plots; zoom/pan/hover/export toolbar out of the box; identical JSON figure spec across JS/Python/R.
- ⚠️ Very heavy bundle (bundles D3 + gl-vis internally); the JSON figure format is verbose; styling fights you if you want a bespoke look; MIT core but commercial upsell around Dash.
- 🎯 Scientific and engineering charts, and anything already using Plotly in Python/R.

## plotly/plotly.py
Python plotting · 18,731★ · Python · MIT · **Active**
- ✅ Interactivity (hover/zoom/select) for free in notebooks and web; Plotly Express is genuinely concise; 3D and statistical chart types; the same figure object powers Dash.
- ⚠️ Large output payloads bloat notebooks and slow rendering; styling defaults are hard to override cleanly; the free/enterprise boundary around Dash causes confusion.
- 🎯 Interactive exploration in notebooks, and any chart destined for a Dash app.

## plouc/nivo
React charting library · 14,082★ · TypeScript · MIT · **Active**
- ✅ Beautiful defaults and a superb interactive docs/playground; canvas variants for larger datasets; SSR support; motion via react-spring.
- ⚠️ Heavy dependency footprint; each chart family has its own prop vocabulary to learn; theming is powerful but verbose; bundle size adds up quickly.
- 🎯 Design-led React dashboards where visual polish matters more than bundle size.

## posit-dev/great-tables
Python plotting · 2,714★ · Python · MIT · **Active**
- ✅ Turns DataFrames into genuinely presentable tables (spanners, footnotes, formatting, nanoplots); the missing piece in most reporting stacks; Posit maintenance.
- ⚠️ Display only — not interactive, not sortable, not a data grid; young API; another dependency for something teams often hand-roll.
- 🎯 Report and dashboard tables that need to look designed rather than dumped.

## recharts/recharts
React charting library · 27,490★ · TypeScript · MIT · **Active**
- ✅ Idiomatic React composition (`<LineChart><XAxis/><Tooltip/>`); declarative and easy to reason about; responsive container built in; MIT; the most-recommended React default.
- ⚠️ SVG-only — struggles well before 10k points; animation and layout bugs surface in complex compositions; customisation beyond the component props gets awkward fast.
- 🎯 The default choice for typical React dashboards with modest data volumes.

## reflex-dev/reflex
Data-app framework · 28,791★ · Python · Apache-2.0 · **Active**
- ✅ Real web-app architecture (components, routing, state) without writing JS; compiles to React/Next.js so the output is a normal SPA; excellent health/activity in this dataset.
- ⚠️ Much larger conceptual surface than Streamlit; the Python→React compilation leaks when you need custom JS; younger ecosystem; debugging spans two runtimes.
- 🎯 Python teams shipping a real web app, not a script with widgets.

## reflex-dev/xy
Python plotting · 1,610★ · Python · Apache-2.0 · **Active**
- ✅ Very fast rendering; clean modern API; first-class inside Reflex apps; hot development pace with a funded team behind it.
- ⚠️ Young and small — API stability, chart coverage, and ecosystem are all unproven; documentation is thin; effectively single-vendor.
- 🎯 Reflex apps, and experiments where speed matters more than maturity.

## rilldata/rill
BI & dashboard platform · 2,803★ · Go · Apache-2.0 · **Active**
- ✅ Genuinely fast exploratory slicing (embedded DuckDB); dashboards-as-YAML; local-first development loop; deliberately designed to be driven by agents as well as humans.
- ⚠️ Young project with a narrower feature set than Superset/Metabase; opinionated metrics-layer model; open-source core alongside a commercial cloud.
- 🎯 Fast metric exploration for teams comfortable defining dashboards in code.

## ScottPlot/ScottPlot
Native / systems charting · 6,696★ · C# · MIT · **Active**
- ✅ By far the strongest .NET plotting option; renders millions of points interactively; supports every major .NET UI framework; MIT; excellent docs and cookbook.
- ⚠️ .NET-only; desktop-oriented (no first-class web story); smaller community than the web libraries; single primary maintainer.
- 🎯 Desktop .NET applications that need real interactive plots.

## streamlit/streamlit
Data-app framework · 45,512★ · Python · Apache-2.0 · **Active**
- ✅ Lowest possible friction (a script becomes an app); enormous component ecosystem; free Community Cloud hosting; renders matplotlib/Plotly/Altair/Vega directly.
- ⚠️ The rerun-on-every-interaction model becomes a correctness and performance problem as apps grow; state management is bolted on; limited layout control; not built for high traffic or multi-user production.
- 🎯 Internal prototypes and demos that will stay simple.

## ToolJet/ToolJet
BI & dashboard platform · 38,304★ · JavaScript · AGPL-3.0 · **Active**
- ✅ Builds full CRUD internal tools, not just read-only dashboards; 50+ connectors; self-hostable; very healthy maintenance signal.
- ⚠️ A low-code app builder first and a charting tool second — visualization options are basic; vendor lock-in to its app model; complex logic in a visual builder ages badly.
- 🎯 Internal tools that need charts *and* write actions in one place.

## tradingview/lightweight-charts
Low-level / high-performance · 16,931★ · TypeScript · Apache-2.0 · **Active**
- ✅ Purpose-built for financial series: candlestick/OHLC, real-time streaming updates, professional pan/zoom feel; tiny; Apache-2.0.
- ⚠️ Financial charts only — no general chart types; indicator library is not included (that's the paid Charting Library); attribution notice required.
- 🎯 Trading, crypto, and any price/time chart that must feel native.

## tremorlabs/tremor
React charting library · 3,560★ · TypeScript · Apache-2.0 · **Stalled** — 305d since push, health 12.
- ✅ Fastest path to a competent-looking dashboard; Tailwind-native; components are copied into your repo so you can edit them; KPI/stat tiles included, not just charts.
- ⚠️ Requires Tailwind; inherits every Recharts performance limit; shifted to a copy-paste model which complicates upgrades; opinionated visual style is hard to fully escape.
- 🎯 Tailwind/Next.js dashboards that need to look finished this week.

## vega/altair
Grammar of graphics · 10,450★ · Python · BSD-3-Clause · **Active**
- ✅ Very concise, highly readable chart code; interactive selections and linked brushing come free; native pandas/Polars support; output is a portable Vega-Lite spec.
- ⚠️ Historically awkward with large data (data is embedded in the spec unless you use `vegafusion`/URLs); customisation ceiling is Vega-Lite's; static export needs extra deps.
- 🎯 Exploratory statistical charts in notebooks, especially with linked interaction.

## vega/vega
Grammar of graphics · 11,953★ · JavaScript · BSD-3-Clause · **Active**
- ✅ Far more expressive than Vega-Lite (custom interaction, layouts, transforms) while staying declarative; renders to canvas or SVG; strong academic pedigree (UW IDL).
- ⚠️ Verbose specs that get unwieldy fast; steeper than both Vega-Lite and most imperative libraries; debugging a large spec is genuinely painful.
- 🎯 Custom interactive graphics that must still be declarative and serializable.

## vega/vega-lite
Grammar of graphics · 5,444★ · TypeScript · BSD-3-Clause · **Active**
- ✅ Charts are portable JSON, which makes them diffable, generatable, and **the most LLM-friendly chart format**; sensible defaults infer scales and legends; excellent faceting/layering; BSD-3.
- ⚠️ Escaping the grammar for a bespoke design means dropping to Vega or another library; rendering performance is modest; error messages on malformed specs are cryptic.
- 🎯 Spec-driven charts, embedded analytics, and charts generated by agents or LLMs.

## visgl/deck.gl
Low-level / high-performance · 14,364★ · TypeScript · MIT · **Active**
- ✅ GPU rendering of millions of points/arcs/hexbins; composable layer model; integrates with MapLibre/Mapbox/Google Maps; battle-tested at Uber scale.
- ⚠️ GPU-only mental model with real memory/driver pitfalls; heavy bundle; overkill for anything under ~100k features; documentation assumes graphics familiarity.
- 🎯 Large-scale geospatial visualization and GPU-accelerated point clouds.

## weaveworks/grafanalib
Dashboards as code · 1,971★ · Python · Apache-2.0 · **Stalled** — 246d since push, health 16.
- ✅ Pythonic dashboard construction with reusable functions; large body of existing examples; simple to integrate into Python CI.
- ⚠️ **Declining in this dataset** — Weaveworks shut down and maintenance has stalled; lags current Grafana panel schemas; superseded by grafana-foundation-sdk.
- 🎯 Legacy Python dashboard pipelines — migrate new work to the Foundation SDK.
