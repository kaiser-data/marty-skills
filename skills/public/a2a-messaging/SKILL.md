---
name: a2a-messaging
description: 'Use when messaging another coding agent on a different machine or from another vendor via the a2a CLI (claude-A2A-Comm) — sending, reading an inbox, registering, checking peers — and especially before reporting that a peer is silent, has not replied, or that a message was delivered. Triggers include a2a, A2A hub, agent-to-agent, cross-machine agent coordination, no reply from a peer, keine Antwort, hub is up but nothing arrives, agent not registered.'
---

# A2A Messaging

## Overview

The `a2a` CLI talks to whichever hub its **environment** points at. Point it at nothing and it
silently creates and uses a *private local hub* where you are the only agent — every send fails
and every inbox is empty. Nothing warns you.

**Core principle: an empty inbox is not evidence of silence. It is evidence about one hub.**
Before you draw any conclusion about a peer, prove which hub you are on.

## The Rule

Run this **first**, in every shell where you use `a2a`:

```bash
set -a; . ~/.a2a-env; set +a
export PATH="/path/to/claude-A2A-Comm/bin:$PATH"   # clone from github.com/kaiser-data/claude-A2A-Comm
a2a peers          # must list the peers you expect, not just you
```

`~/.a2a-env` holds `A2A_HUB_URL` and `A2A_TOKEN`. Shell state does not persist between tool
calls — so source it again in **every** call, not once per session.

Then check you are not alone:

```bash
curl -s "$A2A_HUB_URL/health"      # {"ok": true, "agents": 3}  — needs no token
```

`agents: 1` means you are on a decoy hub. Stop and fix the environment.

## Verification Contract

You may state a message was delivered only when **both** hold:

1. `a2a peers` listed the recipient *before* the send, and
2. `a2a send` exited **0**.

You may state a peer is silent only when you have read `a2a inbox --all --peek` on a hub whose
`/health` shows the peers you expect.

Anything else is an unverified claim. Say "I could not verify" instead.

## Quick Reference

| Task | Command |
|---|---|
| Who am I / who is out there | `a2a whoami` · `a2a peers` |
| Register this session | `a2a register <name> --desc "what you work on"` |
| Send | `a2a send <peer> "text"` — **check `$?`** |
| Send to all | `a2a broadcast "text"` |
| Read new, mark read | `a2a inbox` |
| Inspect without consuming | `a2a inbox --all --peek` |
| Archive before acting | `a2a inbox --all --peek --json > inbox-$(date +%F).json` |
| Block for a reply | `a2a wait --timeout 300` (exit 3 = timeout) |
| Hub lifecycle (local only) | `a2a status` · `up` · `down` |

Identity resolution: `--from` flag > `A2A_NAME` > `.a2a-identity` file in CWD.

**Always archive a full inbox to a file before reading it.** Messages run tens of thousands of
characters; a truncated terminal read silently hides later messages. Count them, then read.

## Failure Modes

**Silent wrong-hub.** With `A2A_HUB_URL` unset, the CLI resolves to `127.0.0.1` and will
`start_daemon()` a local hub if none runs. Registration *succeeds* there. `a2a status` reports
"up". Everything looks healthy while you are alone in an empty room.

**Failed send read as success.** Sending to a peer absent from the current hub's registry prints
`error: agent '<peer>' not registered` to **stderr** and exits **1**. Nothing is delivered. An
agent skimming for stdout output sees nothing unusual and reports the message as sent.

The two compound: wrong hub → peer not in registry → every send fails → inbox stays empty →
"they are not answering." Meanwhile the replies sit unread on the real hub.

## Rationalizations

| Excuse | Reality |
|---|---|
| "`a2a status` says the hub is up" | `status` describes the **local** hub. Up ≠ the shared one. |
| "Registration worked, so I'm connected" | Registration succeeds on a decoy hub too. It proves nothing. |
| "The send printed nothing, so it went out" | The error goes to stderr with exit 1. Check `$?`. |
| "Hours with no reply — they're silent" | Read the inbox on the *shared* hub before saying that. |
| "Inbox is empty" | Empty on **which** hub? And did you pass `--all`? |
| "I'll just send it again" | Same environment, same wrong hub, same failure. |
| "I sourced the env earlier" | Shell state dies between tool calls. Source it again. |
| "`peers` only lists me, they must be offline" | More likely you are on the wrong hub. Check `/health`. |

## Red Flags — Stop and Check the Hub

- You are about to write "no reply", "keine Antwort", "silent", or "waiting on \<peer\>"
- `a2a peers` lists only you
- `A2A_HUB_URL` is unset, or `/health` reports `agents: 1`
- You concluded a send succeeded from the *absence* of output
- You are writing a status report or handoff document that describes a peer's behaviour

**Each of these means: source the env, run `/health` and `a2a peers`, then re-check the inbox.**

## When NOT to Use

Same-machine Claude Code sessions — use built-in session messaging (`ListAgents`, `SendMessage`).
It ships with the product, knows which sessions are busy, and needs no hub. Reach for `a2a` only
for **another machine**, **another vendor**, or A2A protocol interop.

## Hosting a Remote Hub

The hub binds `127.0.0.1` by default, reachable only from its own machine. A shared hub must be
started with an explicit bind and a token:

```bash
A2A_TOKEN=<32+ chars> a2a up --bind <tailnet-ip>
```

Bind to a private-network address, never a public one. `/health` is intentionally unauthenticated;
every other endpoint requires the bearer token. Give each client the same `A2A_HUB_URL` and
`A2A_TOKEN` via its own `~/.a2a-env` (mode `600`).

## Real-World Impact

A session concluded its two peers had gone silent, and wrote that into a handoff document as
"unanswered messages" plus a forensic proof built from the local hub's registry, empty `tasks/`
directory, and access log. Every artefact was real; all of it described a decoy hub. On the
shared hub sat **seven** unread messages — a confirmed API contract, a full 40k-character spec,
four security findings, and three decisions that invalidated already-written code. One
`a2a peers` would have shown it.
