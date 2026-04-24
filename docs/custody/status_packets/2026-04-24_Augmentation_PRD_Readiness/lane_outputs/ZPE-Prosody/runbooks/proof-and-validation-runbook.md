# Proof And Validation Runbook

## Purpose

Reproduce current authority metrics and define the exact evidence needed for the augmentation wave.

## Owner / Agent Type

Validation agent.

## Input Artifacts

- `proofs/artifacts/2026-02-20_zpe_prosody_wave1/before_after_metrics.json`
- `proofs/artifacts/2026-02-20_zpe_prosody_wave1/quality_gate_scorecard.json`
- `proofs/artifacts/2026-02-20_zpe_prosody_wave1/prosody_retrieval_eval.json`
- `proofs/artifacts/c006_retrieval_failure_analysis.md`
- `proofs/artifacts/librispeech_benchmark/`
- `scripts/`
- `tests/`

## Procedure

1. Run local verification:
   - `make test`
   - `python3 -m json.tool docs/market_surface.json`
2. Record current authority metrics:
   - compression `16.5952x`;
   - F0 RMSE `0.8925%`;
   - energy RMSE `2.0780%`;
   - retrieval p@5 `0.3067`;
   - OOD p@5 `0.1707`;
   - quality score `47/50`.
3. Reproduce or rerun the current retrieval protocol before adding alternatives.
4. Require every new result to include:
   - command;
   - corpus/license note;
   - seed/config;
   - p@5 and OOD p@5;
   - comparison to current baseline;
   - pass/fail verdict.
5. Preserve adverse results.

## Output Artifacts

- Current authority map.
- New benchmark result JSONs.
- Failure analysis update.
- Corpus license note.

## Acceptance Gate

- New results are directly comparable to the current failed baseline.
- Retrieval pass is not inferred from codec pass.
- All new numeric values have a file path.

## Failure Mode

If any result cannot be reproduced or compared to the baseline, it cannot support a public claim.

## Resource Requirement

Mac for current tests and small CPU sweeps. CPU pod optional for repeated sweeps. GPU not used in this phase.
