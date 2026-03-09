# Concept Open Questions Resolution

| Question | Status | Resolution | Evidence |
|---|---|---|---|
| Parselmouth GPL contamination risk | RESOLVED | Replaced runtime dependency with lane-local deterministic fallback extractor; packaging remains lane-local and no GPL linkage occurs in this build. | `artifacts/2026-02-20_zpe_prosody_wave1/resource_lock.json` |
| Required F0 frame rate for conditioning | RESOLVED | Standardized frame rate to 10ms (100 fps) across fixtures, encoder, decoder, and transfer bridge path. | `src/zpe_prosody/constants.py`, `artifacts/2026-02-20_zpe_prosody_wave1/integration_readiness_contract.json` |
| Can penn replace torchcrepe on CPU | INCONCLUSIVE | `penn` package unavailable in runtime; comparator benchmark not executed. | `artifacts/2026-02-20_zpe_prosody_wave1/resource_lock.json` |
| ElevenLabs storage format details | INCONCLUSIVE | Public implementation details unavailable in-lane; benchmark target inferred only at abstract contour-array level. | `artifacts/2026-02-20_zpe_prosody_wave1/residual_risk_register.md` |
| Impact of voiced/unvoiced boundary preservation on quality | RESOLVED | Boundary perturbation campaign executed; codec remained stable with bounded fidelity drift. | `artifacts/2026-02-20_zpe_prosody_wave1/falsification_results.md` |
| MOS >=4 with F0+energy only | PAUSED_EXTERNAL | Transfer closure follows max-wave adjudication (PASS/FAIL/PAUSED_EXTERNAL) with explicit MOS/licensing evidence chain. | `artifacts/2026-02-20_zpe_prosody_wave1/prosody_transfer_eval.json` |