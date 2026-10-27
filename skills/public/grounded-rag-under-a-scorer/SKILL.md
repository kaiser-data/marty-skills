---
name: grounded-rag-under-a-scorer
description: Use when building or tuning retrieval-augmented generation that must return a verdict or answer plus cited evidence from long documents (PDFs, booklets, reports, contracts), especially when a scorer judges evidence by fuzzy text matching, counts tokens or processing time, or ranks teams in a hackathon or benchmark. Symptoms - choosing an embedder or chunk size, deciding whether to cite whole pages or quotes, a full-document baseline that is slow or truncated, a prompt tweak that "helped" on one dev run, CPU parsing and embedding that may count against a time budget.
---

# Grounded RAG under a scorer

## Overview

The scorer, not intuition, decides what "good evidence" and "fast" mean. Read its code first,
measure retrieval without the LLM, and treat any single-run difference below the rerun noise as
zero. Every number below was measured on a multilingual claim-verification task (DE/FR/IT voting
booklets, Apertus-8B, 150 dev claims per task, official scorer).

Sources: our system, [kaiser-data/hack-apertus-booklet-nli](https://github.com/kaiser-data/hack-apertus-booklet-nli)
(Hack Apertus 2026, Track 2A). The "document structure first" numbers come from Team Fact Attack's
system on the same task, [JJukic/Apertus-Team-Fact-Attack-2026](https://github.com/JJukic/Apertus-Team-Fact-Attack-2026)
(Apache-2.0), whose contents-guided part selection we then measured on our own test claims.

## Quick reference

| Decision | Measured lesson |
|---|---|
| Evidence granularity | Read how matching works. With `partial_ratio` (shorter text must lie inside the longer), **sentence quotes 0.757 > ~900-char passages 0.616 > whole pages 0.535** Hit@5. Gold passages often include headings that a page does not reproduce contiguously, so "cite the whole page" loses. |
| Filling evidence slots | If only the first k items are scored and extra items cost nothing, fill them: cited sentences first, then the best sentences from the rest of the retrieved context. Deduplicate before filling. Label supplementary items honestly in user-facing UIs. |
| Embedder | Check `max_seq_length` against chunk length, then measure recall **and CPU seconds per document on evaluator-like hardware**. Dev, 338 claims, 4 vCPU: MiniLM (128-token limit) recall@16 0.911 at 3.3 s/document; multilingual-e5-large 0.965 at 83 s; Qwen3-Embedding-0.6B 0.970 (recall@8 0.944) at ~200 s. If the clock counts non-LLM time, the small model can win overall even though it retrieves worse; without a time budget or with a GPU, take the large one and halve k. |
| Lexical signal | BM25 fused by reciprocal rank helped only at small k (MiniLM recall@8 0.769 → 0.805) and not at k=16 (0.911 → 0.905); with e5/Qwen it hurt at every k ≤ 16. Measure it; do not add it by default. |
| Context size | Full document vs top-16 passages on the same 60 claims: F1 0.735 at 31k tokens (6/60 runaway outputs that never emit a label) vs 0.861 at 3.4k. On dev, top-8 vs top-16: 0.850 at 1.8k vs 0.890 at 3.4k tokens. |
| Retrieval vs reasoning | Get an oracle bound for free if the benchmark has a "given passage" variant: gold passage 0.930 vs retrieval 0.857. Better recall alone did not move F1 (recall@16 0.911 → 0.926, F1 0.890 → 0.878): the bottleneck was **distraction**, not missing text. Symptom: many gold-Neutral claims predicted Contradiction (29 of our 68 test errors), because another vote's or the other side's text sits in the context. The fix is less, better-chosen context, not more recall. |
| Evidence by id | Number the passages and let the model return ids. Then emit the cited passages verbatim from your own parse. Quotes stay exact, output drops to ~55 tokens and p95 latency to a third. Build evidence from the same parser the gold annotations came from (PyMuPDF text: 0.87 Hit@5, pypdf 0.80). |
| Document structure first | Before tuning an embedder, check whether the input names where the answer lives (a speaker or part in the claim's first words, a title field) and whether the document has a map (contents page, outline, headings). If both exist, select that part with the map and fall back to retrieval when no part is found. Measured by Team Fact Attack on the same booklets and scorer (with Apertus-v1.5-70B-thinking): the claim's part instead of 8 retrieved pages raised F1 0.949 → 0.968 and Hit@5 0.881 → 0.975, with 55 % fewer tokens. On our 976 test claims their full system beat our top-16 RAG 0.976 vs 0.930 (date-bootstrap CI of the gap +0.025 to +0.069) at half the tokens. |
| Routing signal | Route on an explicit cue (the claim's opening phrase, the given title matched to contents entries), never on embedding similarity between claim and section. Our embedding-based vote routing cut recall@16 0.91 → 0.82 and was dropped. That result says the cue was wrong, not that selecting a part is wrong. |
| Metadata | Use what the input gives you (e.g. the topic/vote name) in the prompt (+3 claims on one task, no loss on the other). |
| Bigger LLM | Check what the scorer charges. If tokens are counted (same tokenizer across sizes) and LLM latency is excluded, a larger model is free: 70B vs 8B, same prompt and retrieval, task A 0.905–0.925 vs 0.857, given-passage task 0.98 vs 0.93, identical input tokens. Pick the model at runtime from the endpoint's `/v1/models` (short timeout, no retries) with a fallback on "model not found". |

## Measuring

1. **Retrieval offline, no LLM:** recall@k of the annotated passage on all dev claims, plus CPU
   seconds per document, on hardware like the evaluator's (not a laptop).
2. **Simulate before you run.** Cascades and routing rules can often be scored on existing run
   files (a k=8 → k=16 "escalate when neutral" cascade simulated at 0.877 vs 0.890, 2% fewer
   tokens: rejected without a GPU minute).
3. **Inspect the inputs before choosing a retriever.** Read 30 claims and the document's contents
   page. Count how many claims name their source part in the first ~30 characters. If most do, the
   first experiment is cue → part → contents pages, measured offline as Hit@5 and tokens.
4. **Compare on identical cases.** When another system's per-case predictions are public, rescore
   them with the official scorer on your own test ids and bootstrap the gap over documents or dates.
   Different splits make headline numbers incomparable.
5. **Rerun noise first.** An identical config rerun at temperature 0 moved macro-F1 by 0.027
   (batched GPU inference is not bit-exact; near-tied passages reorder). A claim-level paired
   bootstrap does not see run-to-run variation. Below ~0.03, call it a tie.

## Time budgets that exclude LLM latency

If the clock counts only time with no LLM request in flight, never preprocess every document up
front. Prepare each document lazily inside the worker threads (one lock per document, one global
lock around non-thread-safe parsers such as PyMuPDF) so parsing and embedding overlap other
cases' requests. Measure it in a container that holds only the document task, as the evaluator runs
it: 0.22 s of non-LLM time per case (33 of 386 s, 150 cases, 18 documents, 6 workers). A file that
mixes in tasks without documents hides the preparation behind their requests and reads too low.

## Contract robustness (each one bit us)

- Split JSONL on `"\n"`, not `str.splitlines()` (U+2028 inside a string breaks a line).
- Write and flush each answer as it completes; bounded retries; on failure emit a valid default.
- Fall back from structured output only on an "unsupported format" error, per request; any 400
  disabling the schema globally makes results depend on case order.
- Bake model weights into the image and test with the network off. ONNX models over 2 GB keep
  their weights in an external file; onnxruntime rejects it behind Hugging Face cache symlinks
  ("External data path escapes model directory"); copy the blobs into the model directory first.
- Classify "unknown model" errors from the message only (error bodies carry types like
  `invalid_request_error`), never on a context-length error, and switch once per failed model.

## Common mistakes

- Treating "chunk + embed + top-k" as the default when the document has a contents page and the
  query names its section.
- Generalising one failed routing attempt into "routing hurts" without checking which signal it used.
- Picking the embedder from a leaderboard without checking truncation and CPU cost per document.
- Citing whole pages because they "contain" the passage, without running the scorer.
- Adopting a prompt change from one dev run (one such change: 0.890 → 0.864, reverted).
- Reporting a laptop latency; measure on the evaluator-like CPU.
