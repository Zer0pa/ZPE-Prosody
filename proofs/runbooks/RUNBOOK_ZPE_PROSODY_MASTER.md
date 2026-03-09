# ZPE Prosody Master Runbook

Scope root: `<repo-root>`
Primary proof root: `proofs/artifacts/2026-02-20_zpe_prosody_wave1`

## Purpose

This runbook is the live, portable execution surface for the repo boundary.

## Current Gate Order

1. Gate A
   - `python3 scripts/gate_a_lock.py --out proofs/artifacts/2026-02-20_zpe_prosody_wave1`
   - `python3 scripts/generate_fixtures.py --out data/fixtures --seed 20260220`
2. Gate B
   - `python3 scripts/gate_b_build.py --out proofs/artifacts/2026-02-20_zpe_prosody_wave1`
3. Gate C
   - `python3 scripts/gate_c_benchmarks.py --out proofs/artifacts/2026-02-20_zpe_prosody_wave1 --seed 20260220`
   - `python3 scripts/validate_thresholds.py --out proofs/artifacts/2026-02-20_zpe_prosody_wave1 --seed 20260220`
4. Gate D
   - `python3 scripts/gate_d_falsification.py --out proofs/artifacts/2026-02-20_zpe_prosody_wave1 --seed 20260220`
   - `python3 scripts/determinism_replay.py --out proofs/artifacts/2026-02-20_zpe_prosody_wave1 --runs 5`
5. Gate E
   - `python3 scripts/gate_e_eval_and_pack.py --out proofs/artifacts/2026-02-20_zpe_prosody_wave1 --seed 20260220`
6. Minimal regression
   - `python3 -m unittest discover -s tests -p 'test_*.py'`

## Important Correction

The historical outer-shell runbook documented `A -> B -> C -> D -> E` without the threshold-validation step. That is incomplete. Gate E depends on the threshold-validation artifact generated after Gate C.

## Historical Proof Boundary

The accepted bundle in `proofs/artifacts/2026-02-20_zpe_prosody_wave1/` remains historical authority for current status. Do not rewrite those historical artifact contents just to make old path strings prettier.

## Deferred Work

- Phase 4.5 performance augmentation
- Phase 5 blind-clone verification
- public release workflow
