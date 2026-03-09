# Gate D Runbook: Malformed/Adversarial/Determinism

## Objective
Validate crash safety, adversarial robustness, and deterministic replay consistency.

## Commands (Predeclared)
1. `python3 scripts/gate_d_falsification.py --out proofs/artifacts/2026-02-20_zpe_prosody_wave1 --seed 20260220`
2. `python3 scripts/determinism_replay.py --out proofs/artifacts/2026-02-20_zpe_prosody_wave1 --runs 5`

## Expected Outputs
- `falsification_results.md`
- `determinism_replay_results.json`
- uncaught crash rate 0%

## Fail Signatures
- Any unhandled exception in malformed corpus
- Determinism hash mismatch across 5/5 runs

## Rollback
- Patch error handling and deterministic state control.
- Rerun Gate D and downstream Gate E.

## Falsification Hook
- DT-PRO-1 through DT-PRO-5 campaigns are required before any claim status upgrade.
