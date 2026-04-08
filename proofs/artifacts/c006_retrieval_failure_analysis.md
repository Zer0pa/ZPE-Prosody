# PRO-C006 Retrieval Failure Analysis

## Accepted Gate State

Current accepted gate state: `FAIL`

Accepted reason from the tracked wave-1 bundle:

> RAVDESS/OOD retrieval metrics below thresholds.

This matters because the retrieval route was actually executed. The accepted blocker is not "missing environment" or "missing corpus access." The accepted blocker is performance.

## What Retrieval Closure Means Here

For this lane, retrieval closure means:

- the real emotional-speech retrieval leg must clear threshold
- the OOD stress leg must also clear threshold

The tracked adjudication shows both legs were run and both failed.

## What Was Attempted

Tracked executed path:

- real `RAVDESS` retrieval evaluation
- OOD retrieval stress evaluation using the tracked `emovome_or_emovoice` route

Tracked results:

| Leg | Dataset | Result | Threshold | Outcome |
|---|---|---:|---:|---|
| in-domain | `RAVDESS` | `p@5 = 0.3066666666666667` | `0.80` | `FAIL` |
| OOD | `emovome_or_emovoice` | `p@5 = 0.17073170731707318` | `0.65` | `FAIL` |

Why it failed:

- the in-domain retrieval score is far below threshold
- the OOD score is even further below threshold
- the miss is too large to describe as noise, packaging drift, or a minor threshold gap

## Is The Gate Achievable?

Possibly, but not with a simple rerun narrative.

The current evidence supports this conclusion:

- if the current retrieval method stays unchanged, the gate should be treated as a likely descope candidate
- if the claim must stay intact, the retrieval representation and scoring path need a material redesign

The gap from `0.3067` to `0.80` on the main leg is too large for "retry and hope."

## Credible Next Paths

### Path 1: Redesign Retrieval

Keep the claim and improve the method:

- replace or augment the current contour-statistics embedding
- introduce stronger temporal or learned prosody features
- re-run on a commercial-safe emotional corpus pair

This is the only path that preserves the current gate meaning.

### Path 2: Descope The Claim

If the present retrieval surface is the intended product boundary, narrow the claim:

- single-corpus retrieval only
- weaker retrieval framing
- retrieval as supporting evidence, not commercialization closure

This is the honest path if redesign is out of scope.

### Path 3: Park The Gate

Preserve the failure evidence, stop active work on the gate, and revisit only when a stronger retrieval method family is ready.

## Recommended Corpus Direction

If the retrieval claim remains alive, the cleaner next corpus direction is:

1. `CREMA-D` for the primary English emotional retrieval leg
2. `EMO-DB` for a secondary OOD leg

This introduces language shift on the OOD leg, but it is explicit and commercially cleaner than leaning on `RAVDESS` and non-commercial corpus substitutes.

## Decision

Current verdict: `redesign or descope`

The accepted blocker is a real retrieval miss. A better corpus alone is not enough. Without a materially stronger retrieval method, `PRO-C006` should stay `FAIL`.
