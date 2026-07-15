---
name: kitsune-improve
description: Make any low-quality MCP server reliably usable through the Kitsune gateway — diagnose weak tool definitions, correct them, and mount a clean surface — without adding tools to Kitsune. Use when a community/long-tail MCP server has vague or missing tool descriptions, thin schemas (no required args), name collisions, or confusing parameters; when the agent keeps making wrong calls against a server; when you want to harden a raw npm/PyPI server before trusting it; or when improving your OWN MCP server's tool definitions. Companion to kitsune-dev (develop) and kitsune-gateway (mount). Requires the kitsune MCP server in the session (test, inspect, shapeshift, call tools).
license: MIT
metadata:
  author: kaiser-data
  upstream: https://github.com/kaiser-data/kitsune-mcp
---

# Kitsune improve — turn a raw MCP server into a reliable one

The long tail of 130k MCP servers is exactly where tool definitions are worst:
missing descriptions, schemas with no `required` array, cryptic parameter
names, tools that collide with each other. An agent handed that surface makes
wrong calls. This skill fixes the *usage*, not by bloating Kitsune with an
`improve()` tool, but by driving the tools Kitsune already has — the agent (you)
is the improvement engine; Kitsune supplies the diagnosis and the clean mount.

This is the "improve" companion to `kitsune-dev` (develop your own server) and
`kitsune-gateway` (reach any server). Kitsune stays slim; the intelligence
lives here.

## Prerequisite

The `kitsune` MCP server must be in the session (check for `test` / `inspect` /
`shapeshift`). If missing, see the `kitsune-gateway` skill's Prerequisite
section — same setup.

## The loop: diagnose → improve → apply

### 1. Diagnose

```python
test("server-id", level="full")   # 0–100 score + concrete weaknesses
inspect("server-id")              # live tools, schemas, required creds, resource docs
```

`test()` flags the fixable problems directly: thin schemas (`properties` but no
`required`), invalid/missing schemas, name collisions with Kitsune's base tools,
missing description. `inspect()` surfaces the server's *own* resource docs — the
raw material for writing better descriptions.

Read both. Decide which tools actually matter for the task (usually 2–5 of
however many the server exposes) and which are noise.

### 2. Improve (you write this — no LLM inside Kitsune)

For the tools that matter, produce a **corrected usage map**:

- **Descriptions** — where a tool's description is vague or absent, write a
  one-line "when to use this / when not to" from the resource docs + the tool
  name. This is what stops adjacent-name confusion (`read_file` vs
  `read_text_file` vs `read_media_file`).
- **Required args** — when the registry schema omits `required`, note which
  params are actually mandatory (Kitsune already refetches the live schema on
  `shapeshift`, but confirm from the docs and record the real ones).
- **Gotchas** — enum casing, path formats, singular-vs-plural verbs, anything
  the schema doesn't spell out.

Keep it to the tools you'll use. This map is the improvement.

### 3. Apply

- **Lean-mount only the good tools** — this *is* the applied improvement: fewer,
  clearer tools mean sharper selection.

  ```python
  shapeshift("server-id", tools=["the_tool", "the_other"], sandbox=True, confirm=True)
  ```

  `sandbox=True` runs an untrusted npm/PyPI server caged in Docker (no host
  filesystem, cap-drop ALL, read-only rootfs); drop it if you already trust the
  source. `tools=[...]` mounts only what your usage map kept.

- **Wrap an HTTP-backed tool with a clean schema** — if the weak tool is a plain
  HTTP endpoint, `craft()` a replacement with the description and params you
  wish it had:

  ```python
  craft("clear_name", "https://api.example.com/thing", method="POST",
        description="Does X. Use when Y.")
  ```

  (`craft()` backs a tool with an HTTP endpoint — it does not re-wrap an
  existing stdio MCP tool. For stdio servers, the lean mount + usage map is the
  fix.)

- **Persist across sessions (optional)** — if this is a server you'll reuse,
  save the corrected usage map next to the project (e.g. `docs/mcp-<server>.md`)
  and re-read it before mounting next time. Cheap, no tool, survives restarts.

## Improving your OWN server (dev mode)

When it's your server, the diagnosis becomes a fix list for the *code*:

1. `test("dev", level="full")` after `connect(...)` (see `kitsune-dev`).
2. For each weakness, edit the tool definition in your server:
   - add a `description` that says when to use the tool,
   - add the `required` array to each `inputSchema`,
   - rename params that collide or mislead.
3. Reload with the `kitsune-dev` loop (`release` → `connect` → `shapeshift`) and
   re-run `test()` — watch the score climb. Ship when it's ≥ "Good".

## Checklist

- [ ] Ran `test(..., "full")` and `inspect(...)` before mounting.
- [ ] Kept only the 2–5 tools the task needs; the rest are noise.
- [ ] Wrote a one-line "when to use" for every vague/undocumented tool kept.
- [ ] Confirmed the real required args from the docs, not just the schema.
- [ ] Mounted lean (+ `sandbox=True` for untrusted sources).
- [ ] For a reusable server: saved the usage map so next session starts clean.
