# Gate A Runbook: Runbook + Fixture/Resource Lock

## Objective
Establish deterministic execution context, resource provenance lock, and fixture generation policy before implementation claims.

## Preconditions
1. `RUNBOOK_ZPE_PROSODY_MASTER.md` exists.
2. Working directory is lane root.

## Commands (Predeclared)
1. `python3 scripts/gate_a_lock.py --out proofs/artifacts/2026-02-20_zpe_prosody_wave1`
2. `python3 scripts/generate_fixtures.py --out data/fixtures --seed 20260220`

## Expected Outputs
- `proofs/artifacts/2026-02-20_zpe_prosody_wave1/resource_lock.json`
- `proofs/artifacts/2026-02-20_zpe_prosody_wave1/command_log.txt` (initialized)
- `data/fixtures/manifest.json`

## Fail Signatures
- Missing `resource_lock.json`
- Fixture manifest lacks deterministic seed metadata
- Any resource item in Appendix B omitted from lock

## Rollback
- Remove partial fixture directory and rerun both commands.
- Do not proceed to Gate B until Appendix B items are fully listed.

## Falsification Hook
- Attempt resource unavailability simulation (missing package import/network fetch) and ensure substitution + comparability impact is logged.

## Appendix D/E Extension
1. Source `.env` before fixture/resource lock and record bootstrap status in command log.
2. Add `max_resource_lock.json` planning placeholders for all E3 resources before execution.
3. If `.env` parsing fails, log failure signature and fallback parser usage.
4. Initialize RunPod dependency lock target `proofs/artifacts/2026-02-20_zpe_prosody_wave1/runpod_requirements_lock.txt` for GPU-deferred paths.
