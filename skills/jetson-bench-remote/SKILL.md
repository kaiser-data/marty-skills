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

## Preferred: the automatic loop

`./run-full-test.sh` (in the bench repo) does the whole cycle unattended:
suspend → WoL wake (timed, ~9–11 s) → verify auto-`MAXN_SUPER` → bench →
push results → back to sleep. It **auto-bridges Ollama over SSH** when 11434
is loopback-bound, with an endpoint-identity check — the manual tunnel below
is only needed for ad-hoc debugging. LAN example:
`JETSON_HOST=192.168.0.115 WOL_BROADCAST=192.168.0.255 ./run-full-test.sh`
(add `--stay-awake` to skip the final suspend).

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

## HTTP 500 on model tests = CUDA out of memory (SOLVED 2026-07-11)

`/api/generate` returning 500 with models correctly installed means
`cudaMalloc failed: out of memory`. Get the real error body:

```bash
curl -s 'http://[::1]:11434/api/generate' \
  -d '{"model":"qwen3.5:0.8b","prompt":"hi","stream":false,"options":{"num_predict":5}}'
```

**Root cause (verified):** the 8 GB is a unified CPU/GPU pool, CUDA buffers
cannot be swap-backed, **and on Tegra `cudaMalloc` fails instead of forcing
page-cache reclaim**. Worst part: reading the GGUF blob during load fills the
page cache with the model file itself (~2.5 GB for qwen3.5:4b), which then
starves the very CUDA allocation the read was feeding — that's why 4b/phi4-mini
failed on this box on *every* recorded run even with 5 GB "available" and
swap=0. `free -m`'s "available" is a lie for CUDA purposes; only "free" counts.

**The fix — user-space only, no sudo (built into `bench.py --mem-prep user@host`,
run-full-test.sh passes it automatically):**

1. **Balloon**: allocate+touch ~4.6 GB in a throwaway python process on the
   Jetson, then exit — forces the kernel to evict page cache and swap idle
   anon pages (e.g. the resident Whisper).
2. **fadvise loop**: while the model loads, a background loop runs
   `os.posix_fadvise(blob_fd, 0, 0, POSIX_FADV_DONTNEED)` on the model's blob
   (world-readable, path from `/api/show` modelfile `FROM` line) every 0.5 s
   so its read-cache can't refill.

With this recipe (GNOME + voice stack still running!): qwen3.5:4b **14.4 tok/s**
(load ~12 s), phi4-mini **18.0 tok/s** (load ~9 s) — first successful runs ever
for both. Works at Ollama's default ctx and `num_ctx=2048`.

Escalation if the recipe isn't enough: stop the voice pipeline's Whisper
(`systemctl --user stop jetson-pipeline` — user unit, no sudo, **ask Marty
first**: the permission classifier blocks remote service stops), stop GNOME
(`sudo systemctl stop gdm` — whitelisted in `/etc/sudoers.d/jetson-maint`),
reboot. Note qwen3.5:4b is really 4.7B Q4_K_M **plus a 24-block vision tower**;
weights buffer alone is 2.46 GiB. Also note qwen3.5 is a thinking model —
its `/api/generate` output lands in the `thinking` field, `response` may be
empty; `eval_count`/`eval_duration` (what bench.py uses) stay correct.

## Publishing results

`bench.py` saves `results/bench-*.json` and rebuilds `dashboard.html` on the
machine it runs on. Commit + push from the Mac clone (conventional commits,
`fix:`/`chore:` style); `--push` does it automatically.
