# ZPE Prosody

`ZPE Prosody` is the private staging repo for the ZPE Prosody Wave-1 lane.

Current accepted authority remains negative:
- overall lane verdict: `FAIL`
- accepted claim snapshot: `PRO-C001 PASS`, `PRO-C002 PASS`, `PRO-C003 PASS`, `PRO-C004 PASS`, `PRO-C005 PAUSED_EXTERNAL`, `PRO-C006 FAIL`
- accepted adjudicated bundle: `proofs/artifacts/2026-02-20_zpe_prosody_wave1/`

This repo is a clean private repo boundary for inspection and staging. It is not a public release surface and it does not claim launch readiness.

## What Is Here

- `src/zpe_prosody/`: the lane package
- `scripts/`: gate and packaging scripts
- `tests/`: lightweight unit coverage
- `data/fixtures/`: deterministic fixture manifest used by the lane scripts
- `proofs/`: proof index, final status, runbooks, and the adjudicated bundle
- `docs/`: architecture, legal boundaries, release-contract notes

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
make package-sanity
make test
```

## Current Truth Boundaries

- The proof bundle under `proofs/artifacts/2026-02-20_zpe_prosody_wave1/` is the accepted historical authority for current lane status.
- External corpora, quarantine assets, and operator scratch runtimes are intentionally kept outside this repo.
- Historical proof artifacts retain some original machine-local paths. Those are evidence lineage, not current setup instructions.

## Read Next

- `proofs/PROOF_INDEX.md`
- `proofs/FINAL_STATUS.md`
- `AUDITOR_PLAYBOOK.md`
- `PUBLIC_AUDIT_LIMITS.md`
- `docs/README.md`

## What Is Not Claimed

- no public release readiness
- no commercial-safe transfer closure
- no retrieval closure on a commercial-safe emotional corpus
- no Phase 4.5 performance augmentation or Phase 5 blind-clone verification yet
