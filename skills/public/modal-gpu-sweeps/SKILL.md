---
name: modal-gpu-sweeps
description: Use when running a grid, sweep, or fan-out of GPU training or inference jobs on Modal, or any rented-GPU platform billed by the second. Symptoms - a config matrix of runs to launch, "let's just kick off the grid", a first GPU run that dies on a typo or an OOM after paying for warm-up, no way to resume a half-finished sweep, per-run cost unknown until the invoice, wanting to change one hyperparameter without editing the shared config.
---

# Modal GPU Sweeps

## Overview

Rented GPUs bill for your mistakes at the same rate as your science. Nearly every failure
in a sweep — a bad path, a missing column, a shape error, a config typo — is reachable on
CPU for cents, *before* any GPU starts.

**Core principle: every failure mode that can be triggered without a GPU must be triggered
without a GPU first.**

## The wave structure

Never launch a grid as one command. Launch it as waves with a decision between each.

| Wave | What runs | Cost | Purpose |
|---|---|---|---|
| **0** | Every cell, CPU only, `--dry-run` | cents | Data generation + config validation + CPU gates for the *whole* grid |
| **1** | The anchor cell and its control | ~$0.50 | Prove the real pipeline end to end on one cell |
| **2** | The remaining cells, `--skip-existing` | the bulk | Only launched if wave 1 landed |

```bash
modal run train.py --dry-run --grid                       # wave 0 — never skip
modal run train.py --organisms ANCHOR,ANCHOR_control \
                   --epoch-checkpoints                     # wave 1
modal run train.py --grid --skip-existing --kl-abort 0.05  # wave 2
```

Wave 0 is the one people skip and the one that pays. It has caught real failures that
would otherwise have burned GPU minutes across every cell simultaneously.

## Four flags to build before you need them

Add these to the runner *before* the first real wave. Retrofitting them mid-sweep means
relaunching.

- **`--dry-run`** — runs data generation and every CPU-side gate, skips the GPU. The wave-0
  enabler.
- **`--skip-existing`** — makes a sweep *resumable*. Without it, one dead cell means
  rerunning the ones that already succeeded, at full price.
- **`--epoch-checkpoints`** — save and score per epoch. Turns one run into three points on
  a quality/cost frontier for the price of two extra evals. Also answers "did an
  intermediate checkpoint beat the endpoint?" without a second sweep.
- **`--abort-on METRIC THRESHOLD`** — kill a run whose **trailing mean** says it cannot
  land. Keep the partial artifact: a cell that failed loudly at epoch 1 is a data point,
  not a waste.

Use the trailing mean, never the instantaneous value — single-step metrics are noisy
enough to abort healthy runs.

## Vary parameters without editing the shared config

```bash
modal run train.py --set LEARNING_RATE=1e-4 --organisms CELL_X
```

**Never edit the shared config file to change one cell.** Every other cell is compared
against the anchor defined there; editing it silently redefines the baseline for runs that
already completed, and nothing will warn you.

## Gate each cell against its own control

If cells have per-cell controls, resolve the control *per cell* (`control_for(name)`),
never a single global one. A global control silently gates cell B against cell A's
baseline, and the resulting numbers look fine.

## Common mistakes

| Mistake | Cost |
|---|---|
| Launching the full grid first | Every cell fails at once, at GPU rates |
| No `--skip-existing` | One crash = rerun the whole sweep |
| Aborting on instantaneous metric | Healthy runs killed by noise |
| Editing shared config per cell | Baseline drifts; earlier results become incomparable |
| Discarding aborted-run artifacts | Throws away the "this cannot land" evidence |
| No per-run cost record | Cannot answer "what did this experiment cost" afterwards |

Write one provenance record per run — config hash, cost, wall time, outcome — as the run
finishes. Reconstructing it later is guesswork.

## Real-world impact

A 23-cell grid across four waves, ~$20 total compute, with the presence-detection result
costing $0.26 of GPU time. Wave 0 caught a config failure that would have hit all 23 cells.

---

## Evolving this skill

This skill is expected to change from use, not from rewriting. Every time it fires, append
one entry to `FIELD-NOTES.md` in this directory — outcome tagged `HELPED`, `NO-TRIGGER`,
`MISFIRE`, `IGNORED`, or `WRONG`.

Edit the text above only when a pattern appears across **3+ entries**; a single `WRONG`
entry justifies an immediate fix. `NO-TRIGGER` and `MISFIRE` mean the *description* needs
work, not the body. Past ~600 words, remove a line before adding one.

**Protocol: skills-that-learn.**
