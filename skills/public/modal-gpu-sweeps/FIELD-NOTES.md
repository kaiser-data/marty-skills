# Field notes — modal-gpu-sweeps

Append-only evidence log. Protocol: **skills-that-learn**. One entry per firing.
Append always; edit `SKILL.md` only when a pattern appears across 3+ entries — except
`WRONG`, which justifies an immediate fix.

Tags: `HELPED` · `NO-TRIGGER` · `MISFIRE` · `IGNORED` · `WRONG`

---

## 2026-08-14 · secret-loyalities · HELPED
Trigger: wave 0 CPU dry-run across a 23-cell grid before any GPU started.
Outcome: caught a config failure that would have hit all 23 cells at GPU rates.
Gap: nothing - the wave structure held. Untested: --abort-on trailing-mean tuning.

## 2026-09-27 — jev-studies Test E (5 open decision models, one Modal server each) — HELPED
Wave 0 (CPU prefetch + `--help` probe) caught one wrong CLI assumption (jev-style `--release`) and pre-downloaded
~80 GB for free. It did NOT catch runtime failures that need a GPU: an unlocked lazy server start under
`@modal.concurrent` (5 servers → OOM), a server that 529s instead of queueing, a server rejecting the `model` field
(my readiness loop retried 4xx for 30 min at GPU rates), and a vLLM start-up ValueError. Lesson: add a wave 0.5 —
start each server once on its GPU with a single probe request and fail fast on 4xx — before the real run.
Also: `modal app stop` of "all ephemeral apps" killed a healthy parallel arm; stop by app ID only.

## 2026-09-27 — jev-studies Test F (7 arms in parallel, shared results dir) — HELPED
Anchor-cell wave 1 (Jev-Omni T1 reproducing an old run bit-for-bit) caught nothing wrong but made every later
Jev-Omni number trustworthy. Two new failure modes: (1) parallel arms diffing one shared output dir can steal each
other's files — give each arm its own staging dir; (2) a vLLM image without the CUDA toolkit dies when FlashInfer
JIT-compiles the sampler, and Modal silently restarts the failing @enter container (billed) — watch for repeated
tracebacks and stop the app by ID. Set VLLM_USE_FLASHINFER_SAMPLER=0 on slim images.
