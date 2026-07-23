---
name: kitsune-gateway
description: Mount any of 130,000+ MCP servers on demand through the Kitsune MCP hub instead of keeping heavy servers always-on. Use when a task needs an MCP server that is not loaded in the session (browser automation, Notion, GitHub, time, weather, any registry server), when an unfamiliar API surface makes CLI guessing risky, when iterating on a local MCP with connect/reload, or when deciding between always-on MCP, CLI fallback, and on-demand mounting. Requires the kitsune MCP server in the session.
license: MIT
metadata:
  author: kaiser-data
  upstream: https://github.com/kaiser-data/kitsune-mcp
---

# Kitsune gateway — any MCP server, on demand

Kitsune is a dynamic MCP proxy: **9 lean tools** (`status, search, auth,
shapeshift, call, auto, connect, release, reload`) at a fixed **~1,774-token
floor**. `shapeshift()` mounts a target server's tools as first-class tools at
runtime and releases them when done — no restart. The lean profile also includes
the MCP REPL trio (`connect` / `release` / `reload`) for live local-server
iteration. Community npm/PyPI mounts **cage in Docker by default** when Docker is
present (`sandbox=False` or `KITSUNE_SANDBOX=off` to opt out).

## Prerequisite

The `kitsune` MCP server must be in the session (check for a `status` /
`shapeshift` tool). If missing:

- kogitsune session: launch a kit that includes the `kitsune` catalog item,
  or add `"+kitsune"` to the kit's `mcp:` list in `kits.yaml`.
- plain session: copy the `kitsune` entry from `~/.claude/mcp-on-demand.json`
  into the project's `.mcp.json`, or `claude --mcp-config` with it.

Do NOT install new always-on servers to solve a one-off need — that is
exactly what this skill avoids.

## Core loop

```python
search("web scraping")                            # 7 registries; rows end with ready: high|mid|low
shapeshift("firecrawl", tools=["scrape_url"])     # surgical mount: only the tools needed
call("scrape_url", arguments={"url": "https://…"})
shapeshift()                                      # ALWAYS unmount when done → back to floor
```

Community / long-tail:

```python
shapeshift("some-npm-mcp", confirm=True)          # cages in Docker by default when available
shapeshift("some-npm-mcp", confirm=True, sandbox=False)  # opt out of the cage
```

One-shot when the server is known:

```python
auto("current time in Tokyo", server_hint="mcp-server-time")
```

`auto()` without `server_hint` routes by semantic search and can misfire —
use `search()` first when unsure.

Local MCP REPL (edit → reload → test) — see the `kitsune-dev` skill:

```python
connect("python /abs/path/to/server.py", name="dev")
shapeshift("dev")
reload("dev")    # after every code edit
```

Credentials:

```python
auth("BRAVE_API_KEY")            # check
auth("BRAVE_API_KEY", "sk-…")    # set; hosted servers can trigger OAuth flows
```

Smithery-hosted servers (HTTP, no local install) need `SMITHERY_API_KEY`.

## Decision rule — CLI vs kitsune vs dedicated session

| Situation | Use |
|---|---|
| Top-20 command of a CLI you know cold (`git status`, `gh pr list`) | plain Bash — ~0 tokens, fine |
| Long-tail or unfamiliar API surface; a wrong call has real cost | kitsune — schema-validated |
| One-off need for a server not loaded (Notion lookup, a scrape, a conversion) | kitsune `search → shapeshift → call → shapeshift()` |
| Iterating on your own MCP server mid-session | kitsune `connect → shapeshift → reload` (`kitsune-dev`) |
| Session will hammer ONE server all day (long browser-QA run, heavy DB work) | dedicated always-on server / kogitsune kit — the per-call hop isn't worth it |
| The one server you need costs under ~1.8K tokens always-on | always-on is cheaper than kitsune's floor — break-even rule |

## Rules

1. **Surgical mounts**: pass `tools=[…]` to `shapeshift` — mount the 2 tools
   you need, not the server's 30.
2. **Always release**: call `shapeshift()` (no args) after the task; leaving a
   form mounted re-creates the always-on bloat this skill exists to avoid.
3. **One form at a time**: shapeshift replaces the current form; finish one
   server's work before mounting the next.
4. **Never harvest/absorb configs without explicit user confirmation**
   (`setup(action=…)` modifies MCP client configs — forge-only).
5. `status()` shows auth state, mounted form, and GATEWAY bloat warnings —
   run it first when anything is unclear.
6. **Trust the default cage** for community mounts when Docker is present;
   only pass `sandbox=False` when you knowingly need host FS/network.
