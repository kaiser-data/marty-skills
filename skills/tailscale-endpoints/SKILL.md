---
name: tailscale-endpoints
description: Call self-hosted APIs across the tailnet, especially the Jetson voice AI box (Ollama LLM, voice pipeline, Piper TTS, control API). Use when a device needs to reach the Jetson's endpoints over Tailscale — voice/speak requests, remote start/stop/model-switch, OpenAI-compatible LLM calls from a laptop/Pi/phone — or when debugging an unreachable tailnet service.
license: MIT
metadata:
  author: kaiser-data
  primary-device: jetson-orin-nano-8gb
---

# Tailnet endpoints — calling the Jetson (and friends)

## Finding devices

```bash
tailscale status                # live device list with 100.x.y.z IPs
tailscale ip -4                 # this device's tailnet IP
tailscale ping <device>         # reachability + direct vs relayed (DERP)
```

Prefer **MagicDNS names** over raw IPs — this tailnet's suffix is `tailf8ce6d.ts.net`,
so the Jetson (hostname `ubuntu`) is:

```
http://ubuntu.tailf8ce6d.ts.net:<port>     # or short: http://ubuntu:<port>
```

Known devices: `ubuntu` = Jetson Orin (the AI box) · `raspberrypi` · `pizero` ·
`martins-macbook-air-2` · `ubuntu-4gb-nbg1-1` (Hetzner VPS).

## The Jetson AI box — endpoint catalogue

Repo: [jetson-headless-inference](https://github.com/kaiser-data/jetson-headless-inference)

| Port | Service | Key endpoints |
|---|---|---|
| 11434 | Ollama LLM | `/v1/chat/completions` (OpenAI-compatible), `/api/generate`, `/api/ps` |
| 8000 | Voice pipeline | `POST /voice/chat` (LLM→speech), `POST /voice/tts` (text→speech), `GET /health` |
| 8080 | Control API | `GET /status`, `POST /speak`, `POST /control/start|stop|switch`, `POST /bt/connect`, `POST /sync`, `GET /sync/status` |
| 5500 | Piper TTS | `POST /v1/audio/speech` (OpenAI-compatible), `GET /health` |

### Auth

If `VOICE_API_TOKEN` is set on the Jetson, ports **8000 and 8080** require
`Authorization: Bearer <token>` on everything **except `/health`**. Ollama
(11434) and Piper (5500) have no auth — the tailnet is the boundary.

### Recipes

```bash
J=http://ubuntu.tailf8ce6d.ts.net

# Is everything up? One call:
curl -s $J:8080/status | python3 -m json.tool

# Make the Jetson speak in the room (returns transcript JSON):
curl -s -X POST $J:8080/speak -H "Content-Type: application/json" \
  -d '{"prompt":"Summarize my day.","use_tools":true}'

# Stream a spoken answer to this device as WAV:
curl -s -X POST $J:8000/voice/chat -H "Content-Type: application/json" \
  -d '{"prompt":"Tell me a joke.","voice":"en","output":"stream"}' -o answer.wav

# Remote-start voice mode / hot-swap the model:
curl -s -X POST $J:8080/control/start  -d '{"mode":"voice"}'
curl -s -X POST $J:8080/control/switch -d '{"model":"phi4-mini"}'
```

```python
# Any OpenAI SDK app works unchanged — just point base_url at the tailnet:
from openai import OpenAI
client = OpenAI(base_url="http://ubuntu.tailf8ce6d.ts.net:11434/v1", api_key="ollama")
```

## Gotchas that waste time

- **Use long timeouts.** LLM generation on the Orin runs 8–35 tok/s; a full
  answer can take 30–120 s. Set client timeouts to 180 s (the control API's
  own `/speak` proxy uses 180 s). Prefer `output:"stream"` — audio bytes start
  flowing after the first sentence.
- **Check `/status` before blaming the network.** The box may be in the wrong
  mode (LLM not loaded, pipeline stopped). `POST /control/start {"mode":"voice"}`
  fixes it remotely; starting takes 10–30 s and runs in the background.
- **`voice` values**: `en` (male, ryan-high) · `en_female` (lessac) · `de`
  (thorsten). Unknown voice → 404.
- **`save_to` is a bare filename**, stored on the *Jetson* under
  `~/.local/share/jetson-ai/recordings/` — it is not a path and not on the
  client. To get audio locally, use `output:"stream"` or `"both"` and save the
  response body.
- **`use_tools:true`** answers from the Jetson's local calendar/email cache;
  if answers seem stale, `POST /speak`-adjacent fix is `POST $J:8080/sync` first.
- **Connection refused vs timeout**: refused = service down on the Jetson
  (`systemctl --user status jetson-*` there); timeout = tailnet issue —
  `tailscale ping ubuntu`, check the peer isn't `offline` in `tailscale status`.
- **Don't expose beyond the tailnet.** No `tailscale funnel` on these ports:
  Ollama is auth-less by design, and 8000/8080 fall back to server-side cloud
  API keys when a request omits its own.
