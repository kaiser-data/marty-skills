---
name: jetson-bench-remote
description: Run the jetson-bench suite (LLM tok/s, TTS, STT, connectivity) against the Jetson Orin from the Mac, including the SSH tunnel needed to reach Ollama and diagnosis of cudaMalloc OOM failures. Use when benchmarking the Jetson voice stack remotely, when port 11434 is unreachable from outside the Jetson, when bench.py model tests return HTTP 500, or when Ollama works on-device but not over the tailnet.
license: MIT
metadata:
  author: kaiser-data
  primary-device: jetson-orin-nano-8gb
---

# jetson-bench from the Mac — remote benchmarking playbook

Client repo: [jetson-bench](https://github.com/kaiser-data/jetson-bench) (stdlib-only,
`python3 bench.py`). Local clones: `~/claude-projects/jetson-nano-bench/jetson-bench`
(Mac) and `~/dev/projects/jetson-bench` (Jetson — where the historical
`host: localhost` runs came from).

## Access facts (verified 2026-07)

- SSH user is **`marty@`** — `marty@100.78.34.27` / `marty@ubuntu.tailf8ce6d.ts.net`.
  Key auth works from the MacBook Air. `ubuntu@` is **denied**; don't retry it.
- `sudo` on the Jetson **requires a password** — nothing needing root can run
  over non-interactive SSH. Ask Marty to run root steps in a terminal.
- **Ollama binds to `127.0.0.1:11434` only** (no `OLLAMA_HOST` env on the service).
  The intended setup (`jetson-ai.sh` writes `OLLAMA_HOST=0.0.0.0:11434`) has
  drifted. Piper 5500, pipeline 8000, control 8080 listen externally and work
  fine over the tailnet. So: `/status` on 8080 says `llm.running: true` while
  11434 refuses external connections — that combination means *localhost
  binding*, not "service down".

## Reaching Ollama from the Mac: the IPv6 tunnel trick

The Mac runs its **own local Ollama on IPv4 `127.0.0.1:11434`** — a plain
`ssh -L 11434:...` fails with "address already in use", and worse, a sloppy
tunnel can silently benchmark the *Mac's* Ollama. Bind the tunnel to IPv6
loopback instead; macOS resolves `localhost` to `::1` first, so curl and
Python both hit the Jetson while the Mac's Ollama keeps IPv4:

```bash
ssh -o BatchMode=yes -o ExitOnForwardFailure=yes -f -N \
  -L "[::1]:11434:localhost:11434" \
  -L 5500:localhost:5500 -L 8000:localhost:8000 -L 8080:localhost:8080 \
  marty@100.78.34.27
```

**Always verify which Ollama you're talking to** before benchmarking —
the two ends run different versions:

```bash
curl -s http://127.0.0.1:11434/api/version   # Mac's local Ollama (IPv4)
curl -s 'http://[::1]:11434/api/version'     # Jetson via tunnel (IPv6)
python3 -c "import urllib.request; print(urllib.request.urlopen('http://localhost:11434/api/version').read())"
# → must match the Jetson's version, not the Mac's
```

Then run the full suite with `python3 bench.py --host localhost` — identical
conditions to the historical on-device runs. Throughput numbers stay valid over
the tunnel because tok/s comes from Ollama's own `eval_count / eval_duration`
(device-side); only model *load* wall-time gains a few ms of network.

Kill the tunnel afterwards: `lsof -nP -iTCP:11434 -sTCP:LISTEN` → kill the `ssh` pid.

## Voice-only runs

`python3 bench.py --host <jetson-ip> --skip-models` needs **no tunnel** —
connectivity + TTS + STT go through the externally-bound ports. (Requires the
fix in commit `cbfa831`; before it, bench.py aborted on Ollama failure even
with `--skip-models`.)

## HTTP 500 on model tests = CUDA out of memory

`/api/generate` returning 500 with models correctly installed means
`cudaMalloc failed: out of memory`. Get the real error body:

```bash
curl -s 'http://[::1]:11434/api/generate' \
  -d '{"model":"qwen3.5:0.8b","prompt":"hi","stream":false,"options":{"num_predict":5}}'
```

Jetson-specific trap: the 8 GB is a **unified CPU/GPU pool and CUDA buffers
cannot be swap-backed**, so `free -m` showing gigabytes "available" does not
mean a model can load — if swap is already in use, GPU allocations far smaller
than "available" RAM still fail. Check pressure (read-only):

```bash
ssh marty@100.78.34.27 "free -m | head -3; ps axo rss,comm --sort=-rss | head -12"
```

Usual suspects on this box: voice-pipeline python3 with Whisper loaded (~770 MB),
GNOME stack (~500 MB, shouldn't be running for benchmarks per the README),
long-running `claude`/`bun` processes. Remedies in escalating order: stop the
voice pipeline's Whisper, stop GNOME (`sudo systemctl stop gdm` — needs
password), reboot. Re-run the bench only after `swap used` is near zero.

## Publishing results

`bench.py` saves `results/bench-*.json` and rebuilds `dashboard.html` on the
machine it runs on. Commit + push from the Mac clone (conventional commits,
`fix:`/`chore:` style); `--push` does it automatically.
