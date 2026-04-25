# ZPE-Prosody

Deterministic prosody packet encoding for repo-local F0, energy, duration, and voiced-mask contour bundles. This README promotes only claims that have both a committed proof artifact and a CI test exercising the behavior.

No investor/commercial pass claim is made here. Historical proof artifacts record prior compression, fidelity, transfer, and retrieval adjudication, but the exact numeric scorecard is not promoted from the README because current CI does not exercise those historical metrics end to end.

## CI-Anchored Claims

| Claim | Proof Artifact | CI Test |
|-------|----------------|---------|
| `ZPRS/v1` packets encode and decode contour bundles without changing frame shape or voiced-mask length. | `proofs/artifacts/2026-02-20_zpe_prosody_wave1/gate_b_roundtrip.json` | `tests/test_packet_format.py::PacketFormatTests::test_encode_decode_shape` |
| Malformed packet magic is rejected through a structured decode error. | `proofs/artifacts/2026-02-20_zpe_prosody_wave1/gate_d_falsification_summary.json` | `tests/test_packet_format.py::PacketFormatTests::test_bad_magic_raises` |
| Round-trip F0 and energy reconstruction stay below the current CI thresholds on generated contour fixtures. | `proofs/artifacts/2026-02-20_zpe_prosody_wave1/prosody_f0_fidelity.json`, `proofs/artifacts/2026-02-20_zpe_prosody_wave1/prosody_energy_fidelity.json` | `tests/test_roundtrip.py::RoundTripTests::test_roundtrip_fidelity` |
| Encoding the same contour bundle with the same metadata is byte-stable. | `proofs/artifacts/2026-02-20_zpe_prosody_wave1/determinism_replay_results.json` | `tests/test_roundtrip.py::RoundTripTests::test_deterministic_bytes` |
| The in-process API contract supports encode, decode, transfer, and advertised endpoint capability checks. | `proofs/artifacts/2026-02-20_zpe_prosody_wave1/integration_readiness_contract.json` | `tests/test_api_contract.py` |

## Non-Promoted Historical Artifacts

The following proof artifacts remain in the repository for audit lineage, but their exact claims are not promoted in this README because there is no current CI test exercising them:

- `proofs/artifacts/2026-02-20_zpe_prosody_wave1/before_after_metrics.json`
- `proofs/artifacts/2026-02-20_zpe_prosody_wave1/prosody_compression_benchmark.json`
- `proofs/artifacts/2026-02-20_zpe_prosody_wave1/prosody_retrieval_eval.json`
- `proofs/artifacts/2026-02-20_zpe_prosody_wave1/quality_gate_scorecard.json`
- `proofs/artifacts/c006_retrieval_failure_analysis.md`

## What Is Not Claimed

- No lane pass.
- No retrieval closure above threshold.
- No commercialization-safe transfer closure.
- No public release-readiness claim.
- No speech-codec comparator leadership.
- No exact historical scorecard metric claim from the README front door.

## Repo Shape

- `src/zpe_prosody/`: installable codec package.
- `tests/`: CI-backed package, packet, API, and round-trip checks.
- `scripts/verify_release_surface.py`: package surface sanity helper used by `make package-sanity`.
- `proofs/`: historical adjudication artifacts and audit lineage.
- `docs/`: architecture, legal-boundary, market-surface, and family notes.

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
make repo-sanity
make package-sanity
make test
```

Optional API wrapper dependency:

```bash
python -m pip install ".[api]"
```

The base wheel ships only `src/zpe_prosody`. No CLI or historical gate harness is packaged as a runtime contract. Read [docs/LEGAL_BOUNDARIES.md](docs/LEGAL_BOUNDARIES.md) before widening any claim from this repo state.
