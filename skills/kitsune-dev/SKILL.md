---
name: kitsune-dev
description: Hot-reload loop for developing your own MCP server through the Kitsune gateway — edit tool code, reload, and test in the same session without restarting the client. Use when building or iterating on a work-in-progress MCP server, when a tool's schema or behaviour changed and you want to see it live, when tool edits appear to have no effect (stale pooled process), or when you want an edit-reload-test loop (an MCP REPL) instead of restarting Claude Code on every change. Requires the kitsune MCP server in the session (connect, reload, shapeshift, call, release tools — all on the default lean profile).
license: MIT
metadata:
  author: kaiser-data
  upstream: https://github.com/kaiser-data/kitsune-mcp
---

# Kitsune dev — hot-reload your own MCP server

Normally a client (Claude Code, etc.) caches an MCP server's tool list at
startup, so changing a tool means restarting the client and losing the whole
session. Kitsune breaks that: it stays mounted as the stable gateway while your
work-in-progress server runs as a **child process** underneath. Cycle the child
— your session, context, and conversation survive every iteration. It is an MCP
REPL: edit → reload → test, in place. The REPL trio (`connect` / `release` /
`reload`) ships on the **default lean profile** — no forge required.

## Prerequisite

The `kitsune` MCP server must be in the session (check for `connect` /
`reload` / `shapeshift` tools). If missing, see the `kitsune-gateway` skill's
Prerequisite section — same setup.

## The loop

**Mount once:**

```python
connect("python /abs/path/to/server.py", name="dev")   # start the child process
shapeshift("dev")                                       # mount its tools → callable + client sees them
call("my_tool", arguments={"x": 1})                     # test
```

**After every edit — prefer one-call `reload()`:**

```python
reload("dev")                                           # kill stale process → start fresh code → remount
call("my_tool", arguments={"x": 1})                     # re-test
```

`reload(name)` folds the old release → connect → shapeshift cycle into one call
and always releases first, so you never hit the "Already connected … predates
your edit" footgun.

**Manual 3-step (only if you need to change the launch command):**

```python
release("dev")
connect("python /abs/path/to/server.py", name="dev")
shapeshift("dev")
```

**Done:**

```python
shapeshift()          # unmount tools → back to the lean floor
release("dev")         # ensure the child process is gone
```

## Why each step

- `connect()` accepts an **arbitrary shell command**, so it can launch a local
  file the registry has never heard of. It starts the process and registers it
  under `name`; it does *not* mount tools yet.
- `shapeshift("dev")` mounts the named connection's tools as the current form.
  It re-reads the tool list from the **live** process each time and fires the
  client's `tool_list_changed` notification — this is what surfaces added,
  removed, or re-typed tools without a client restart.
- `reload("dev")` = release + connect + shapeshift using the stored launch
  command. Prefer this after every code edit.
- `call()` routes to the pooled child **only when that server is the current
  form** — so a mount (`shapeshift` or the remount inside `reload`) is required
  before calling.
- `release("dev")` kills the process and clears both the warm pool and the
  session connection.

## The one footgun — never re-`connect()` without releasing first

Kitsune keeps a warm pool keyed by the exact command. Re-running `connect()`
with the **same command** returns `Already connected: dev (PID …)` and hands you
back the **old process running your old code**. Your edit silently appears to do
nothing.

Rule: after editing server code, call **`reload("dev")`** (or `release` first).
Never trust "Already connected" while iterating. If a tool's behaviour doesn't
match the source you just saved, you almost certainly skipped the release.

## Rules

1. **Absolute paths only.** `connect()` splits the command and runs it from
   Kitsune's working directory, not yours — a relative path resolves against the
   wrong root. Pass `/abs/path/to/server.py`.
2. **Always name it** (`name="dev"`). `reload()` / `release()` / `shapeshift()`
   target the connection by name.
3. **Prefer `reload()` after edits.** Use the manual 3-step only when changing
   the launch command itself.
4. **Read stderr for crashes.** `connect()` defaults to `inherit_stderr=True`,
   so a child that dies on import surfaces its traceback. A connect that returns
   no tools usually means the server crashed at startup — check the trace, fix,
   reload.
5. **Bump `timeout`** for slow starts: `connect(cmd, name="dev", timeout=120)`.
6. **One form at a time.** `shapeshift("dev")` / `reload("dev")` replaces the
   current form; you do not need to unmount before re-mounting during the loop.

## Minimal server to start from (FastMCP, stdio)

```python
# /abs/path/to/server.py
from fastmcp import FastMCP

mcp = FastMCP("dev-server")

@mcp.tool()
def greet(name: str) -> str:
    """Say hello to someone."""
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run()   # stdio transport — what connect() speaks
```

Edit a tool, save, `reload("dev")`, `call("greet", {"name": "world"})`.
The changed schema is live in the same session.

## When NOT to use this

- Consuming an existing registry server (browser automation, Notion, a scrape) —
  that's the `kitsune-gateway` skill's `search → shapeshift → call` loop, no
  `connect()` needed.
- A server that is stable and done — add it to the client's MCP config as a
  normal always-on entry; the gateway hop only earns its keep while the code is
  still moving.
