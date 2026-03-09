# Auditor Playbook

This is the shortest honest verification path for the private staging repo.

## What You Can Verify Here

- the repo boundary is clean and private-first
- the package imports and minimal test surface are live
- the accepted historical proof bundle is present
- the current lane verdict is still `FAIL`

## Quick Verification

```bash
git clone <private-url> zpe-prosody
cd zpe-prosody
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
make package-sanity
make test
```

## Expected Current Truth

- package name: `zpe-prosody`
- packet format: `ZPRS/v1`
- minimal unit suite: passes
- accepted lane verdict: `FAIL`
- accepted claim status:
  - `PRO-C001 PASS`
  - `PRO-C002 PASS`
  - `PRO-C003 PASS`
  - `PRO-C004 PASS`
  - `PRO-C005 PAUSED_EXTERNAL`
  - `PRO-C006 FAIL`

## Proof Anchors

- `proofs/PROOF_INDEX.md`
- `proofs/FINAL_STATUS.md`
- `proofs/artifacts/2026-02-20_zpe_prosody_wave1/quality_gate_scorecard.json`
- `proofs/artifacts/2026-02-20_zpe_prosody_wave1/claim_status_delta.md`
- `proofs/artifacts/2026-02-20_zpe_prosody_wave1/handoff_manifest.json`

## What This Playbook Does Not Establish

- Phase 4.5 performance augmentation
- Phase 5 blind-clone verification
- public release readiness
- commercial-safe closure for `PRO-C005`
- retrieval closure for `PRO-C006`
