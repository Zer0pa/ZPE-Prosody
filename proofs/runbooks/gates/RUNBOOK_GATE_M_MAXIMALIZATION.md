# Gate M Runbook: Appendix D/E Maximalization

## Objective
Close prior `INCONCLUSIVE` claim states using real resource attempts, protocol-bound evaluation, and full net-new ingestion evidence.

## Commands (Predeclared)
1. `python3 scripts/gate_m_resource_ingestion.py --out proofs/artifacts/2026-02-20_zpe_prosody_wave1 --seed 20260220`
2. `python3 scripts/gate_m_claim_adjudication.py --out proofs/artifacts/2026-02-20_zpe_prosody_wave1 --seed 20260220`
3. `python3 scripts/gate_e_eval_and_pack.py --out proofs/artifacts/2026-02-20_zpe_prosody_wave1 --seed 20260220`

## Expected Outputs
- `max_resource_lock.json`
- `max_resource_validation_log.md`
- `max_claim_resource_map.json`
- `impracticality_decisions.json`
- `mos_crosscheck_report.json`
- `net_new_gap_closure_matrix.json`
- `runpod_readiness_manifest.json` and `runpod_exec_plan.md` when any `IMP-COMPUTE`

## Hard Gates
1. M1: `PRO-C005` transitions to `PASS` or `FAIL` (not `INCONCLUSIVE`) if XTTS+MOS path executable.
2. M2: `PRO-C006` transitions to `PASS` or `FAIL` (not `INCONCLUSIVE`) if real RAVDESS + OOD path executable.
3. M3: overall quality gate updated with maximalization evidence.
4. M4: fallback path retained as controlled degradation only.
5. E-G1..E-G5 enforced exactly.
6. F-G1: open claims end as `PASS`, `FAIL`, or `PAUSED_EXTERNAL` (no unresolved `INCONCLUSIVE` at closure).
7. F-G2: NC/restricted resources must be explicitly bounded for commercial closure evidence.

## Fail Signatures
- Missing any Appendix E artifact.
- Any E3 resource not attempted with command evidence.
- Any impracticality decision without IMP code and claim mapping.
- Missing commercialization evidence when claim is marked `PAUSED_EXTERNAL`.
- RunPod lockfile absent for deferred GPU path.
- Commercial-safe replacement path exhaustion not evidenced with at least 3 concrete attempts.

## Rollback
- Patch only failing resource adapter or adjudication logic.
- Re-run Gate M and regenerate handoff manifest.

## Commercialization Adjudication
1. Record license state for XTTS and corpora in `impracticality_decisions.json`.
2. Attempt a commercial-safe alternative (`CosyVoice2` or equivalent permissive stack) with command evidence when primary path is NC/restricted.
3. If alternative cannot be executed in-lane, set affected claim `PAUSED_EXTERNAL` with claim-impact note.

## FAIL Recovery Push Addendum (2026-02-21)
1. Attempt replacement paths in sequence for `PRO-C005`:
   - CosyVoice2 native
   - CosyVoice2 containerized
   - Parler-TTS native
   - Piper native
2. Attempt commercial-safe emotional retrieval alternatives for `PRO-C006`; if none are equivalent, retain explicit `FAIL` or `PAUSED_EXTERNAL` with legal evidence.
3. Write internet-backed licensing/reproducibility trace to `proofs/artifacts/2026-02-20_zpe_prosody_wave1/internet_evidence_log.md`.
4. Emit `commercialization_risk_register.md` with risk IDs `RISK-002` and `RISK-003`, replacement status, and claim impact.
