# Gate C Runbook: Fidelity/Compression/Latency Benchmarks

## Objective
Generate quantitative metrics for PRO-C001..PRO-C004 using deterministic evaluation sets.

## Commands (Predeclared)
1. `python3 scripts/gate_c_benchmarks.py --out proofs/artifacts/2026-02-20_zpe_prosody_wave1 --seed 20260220`
2. `python3 scripts/validate_thresholds.py --out proofs/artifacts/2026-02-20_zpe_prosody_wave1`

## Expected Outputs
- `prosody_compression_benchmark.json`
- `prosody_f0_fidelity.json`
- `prosody_energy_fidelity.json`
- `prosody_latency_benchmark.json`

## Fail Signatures
- Compression ratio below 15x
- F0 RMSE above 5%
- Energy RMSE above 3%
- Mean encode latency above 50 ms/utterance

## Rollback
- Patch quantization/packing or vectorization only.
- Re-run Gate C, then D and E.

## Falsification Hook
- Boundary perturbations and extractor fallback drift tests executed before claim promotion.
