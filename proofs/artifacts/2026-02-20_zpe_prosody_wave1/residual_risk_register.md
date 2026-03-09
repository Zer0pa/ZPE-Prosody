# Residual Risk Register

| Risk ID | Description | Severity | Mitigation | Status | Evidence |
|---|---|---|---|---|---|
| RISK-001 | External extractors (torchcrepe/parselmouth/penn) unavailable in runtime. | High | Keep claims requiring extractor comparators constrained; use deterministic fallback with logged impact. | OPEN | `artifacts/2026-02-20_zpe_prosody_wave1/resource_lock.json` |
| RISK-002 | Transfer path uses restricted or partially unavailable TTS/MOS stack in current lane. | High | Claim state is `PAUSED_EXTERNAL` until commercial-safe transfer stack is fully reproducible. | OPEN | `artifacts/2026-02-20_zpe_prosody_wave1/prosody_transfer_eval.json` |
| RISK-003 | Emotional retrieval corpus licensing/equivalence is not fully proven for commercialization. | Medium | Claim state is `FAIL` until commercial-safe corpus closure is completed. | OPEN | `artifacts/2026-02-20_zpe_prosody_wave1/prosody_retrieval_eval.json` |
| RISK-004 | FastAPI/Uvicorn absent; integration validated via equivalent in-process contract only. | Medium | Run same contract tests on FastAPI deployment target before launch. | OPEN | `artifacts/2026-02-20_zpe_prosody_wave1/integration_readiness_contract.json` |