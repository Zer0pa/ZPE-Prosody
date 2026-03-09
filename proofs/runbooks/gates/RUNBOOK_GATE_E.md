# Gate E Runbook: Retrieval/Transfer Eval + Packaging

## Objective
Run retrieval and transfer evaluation, integration checks, regression pass, and finalize artifact handoff.

## Commands (Predeclared)
1. `python3 scripts/gate_e_eval_and_pack.py --out proofs/artifacts/2026-02-20_zpe_prosody_wave1 --seed 20260220`
2. `python3 -m unittest discover -s tests -p 'test_*.py' > proofs/artifacts/2026-02-20_zpe_prosody_wave1/regression_results.txt`

## Expected Outputs
- `prosody_retrieval_eval.json`
- `prosody_transfer_eval.json`
- `handoff_manifest.json`
- Appendix C contract files

## Fail Signatures
- Retrieval P@5 below 0.80
- Transfer MOS below 4.0
- Missing any required artifact contract output

## Rollback
- Patch retrieval/transfer scoring or packaging schema issues.
- Rerun Gate E and regenerate manifest.

## Falsification Hook
- Confusion-set retrieval test and transfer quality floor test run before claim promotion.

## Appendix D/E Extension
1. Validate E-G1..E-G5 in packaging stage.
2. Emit net-new ingestion artifacts and runpod readiness artifacts (if any `IMP-COMPUTE`).
3. Ensure claim-status transition explicitly documents whether M1/M2 became `PASS`, `FAIL`, or `PAUSED_EXTERNAL` with commercialization evidence.
4. Validate final closure gate F-G1/F-G2 before writing `handoff_manifest.json`.
