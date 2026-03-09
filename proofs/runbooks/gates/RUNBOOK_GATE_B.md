# Gate B Runbook: Core Contour Encode/Decode

## Objective
Implement and verify `.zpros` encode/decode for F0, energy, duration contours with deterministic roundtrip behavior.

## Commands (Predeclared)
1. `python3 scripts/gate_b_build.py --out proofs/artifacts/2026-02-20_zpe_prosody_wave1`
2. `python3 -m unittest tests/test_packet_format.py tests/test_roundtrip.py`

## Expected Outputs
- Roundtrip report in `proofs/artifacts/2026-02-20_zpe_prosody_wave1/gate_b_roundtrip.json`
- Packet compliance checks pass

## Fail Signatures
- Decode length mismatch
- CRC/stream integrity mismatch
- Non-deterministic token stream hashes across same input

## Rollback
- Revert only encode/decode/packet modules to last green commit state within lane.
- Rerun Gate B plus downstream gates.

## Falsification Hook
- Inject frame-boundary corruption and truncated payloads; decoder must not crash and must emit structured error records.
