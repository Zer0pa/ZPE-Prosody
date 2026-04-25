# ZPE-Prosody

Deterministic prosody packet encoding for repo-local F0, energy, duration, and voiced-mask contour bundles. This README promotes only claims that have both a committed proof artifact and a CI test exercising the behavior, or are explicitly annotated as proof-artifact-level records not re-run per CI push.

No investor/commercial pass claim is made here. Historical proof artifacts record prior compression, fidelity, transfer, and retrieval adjudication. Retrieval (PRO-C006) remains FAIL; transfer closure (PRO-C005) remains PAUSED_EXTERNAL. Neither gate result is promoted here.

## CI-Anchored Claims

| Claim | Proof Artifact | CI Test |
|-------|----------------|---------|
| `ZPRS/v1` packets encode and decode contour bundles without changing frame shape or voiced-mask length. | `proofs/artifacts/2026-02-20_zpe_prosody_wave1/gate_b_roundtrip.json` | `tests/test_packet_format.py::PacketFormatTests::test_encode_decode_shape` |
| Malformed packet magic is rejected through a structured decode error. | `proofs/artifacts/2026-02-20_zpe_prosody_wave1/gate_d_falsification_summary.json` | `tests/test_packet_format.py::PacketFormatTests::test_bad_magic_raises` |
| Round-trip F0 and energy reconstruction stay below the current CI thresholds on generated contour fixtures. | `proofs/artifacts/2026-02-20_zpe_prosody_wave1/prosody_f0_fidelity.json`, `proofs/artifacts/2026-02-20_zpe_prosody_wave1/prosody_energy_fidelity.json` | `tests/test_roundtrip.py::RoundTripTests::test_roundtrip_fidelity` |
| Encoding the same contour bundle with the same metadata is byte-stable. | `proofs/artifacts/2026-02-20_zpe_prosody_wave1/determinism_replay_results.json` | `tests/test_roundtrip.py::RoundTripTests::test_deterministic_bytes` |
| The in-process API contract supports encode, decode, transfer, and advertised endpoint capability checks. | `proofs/artifacts/2026-02-20_zpe_prosody_wave1/integration_readiness_contract.json` | `tests/test_api_contract.py` |

## Measured Performance (Proof-Artifact Records)

These metrics come from committed proof-artifact runs, not reasserted per CI push. Each number is anchored to a specific artifact file; the artifact commit is the evidence. CI thresholds are broader than these measured values by design — the proof runs set the floor, CI guards against regression.

**Compression** (baseline: raw float32 arrays for F0, energy, duration, voiced\_mask)

| Dataset | Samples | Mean ratio | p50 ratio | p95 ratio | CI threshold | Artifact |
|---------|---------|-----------|-----------|-----------|--------------|----------|
| LibriSpeech `test-clean` (real speech, OpenSLR) | 100 utterances | **13.0×** | 13.0× | 16.6× | — | `proofs/artifacts/librispeech_benchmark/compression_benchmark.json` |
| Librispeech-like fixtures | 140 | **16.6×** | 16.6× | 20.0× | ≥15× | `proofs/artifacts/2026-02-20_zpe_prosody_wave1/prosody_compression_benchmark.json` |

**Fidelity** (round-trip encode → decode)

| Metric | Dataset | Samples | Mean | p95 | CI threshold | Artifact |
|--------|---------|---------|------|-----|--------------|----------|
| Voiced-F0 RMSE | LibriSpeech `test-clean` (real) | 100 | **0.64%** | 1.21% | — | `proofs/artifacts/librispeech_benchmark/f0_fidelity.json` |
| Voiced-F0 RMSE | CMU Arctic-like fixtures | 80 | **0.89%** | 1.01% | 5.0% | `proofs/artifacts/2026-02-20_zpe_prosody_wave1/prosody_f0_fidelity.json` |
| Energy RMSE | CMU Arctic-like fixtures | 80 | **2.08%** | 2.18% | 3.0% | `proofs/artifacts/2026-02-20_zpe_prosody_wave1/prosody_energy_fidelity.json` |
| Duration (timing) RMSE | LibriSpeech `test-clean` (real) | 100 | **0.000 ms** | 0.000 ms | — | `proofs/artifacts/librispeech_benchmark/timing_fidelity.json` |

**Encode latency** (single-threaded, no GPU)

| Dataset | Samples | Mean | p95 | Artifact |
|---------|---------|------|-----|----------|
| LibriSpeech `test-clean` (real) | 100 | **2.67 ms** | 5.18 ms | `proofs/artifacts/librispeech_benchmark/latency_benchmark.json` |
| Librispeech-like fixtures | 140 | **2.59 ms** | 4.14 ms | `proofs/artifacts/2026-02-20_zpe_prosody_wave1/prosody_latency_benchmark.json` |

**Robustness** (malformed-packet falsification campaign)

| Test | Result | Artifact |
|------|--------|----------|
| Malformed packet cases | 4/4 decode errors caught, 0.0 uncaught crash rate | `proofs/artifacts/2026-02-20_zpe_prosody_wave1/gate_d_falsification_summary.json` |
| Determinism replay | 5/5 hash-identical runs | `proofs/artifacts/2026-02-20_zpe_prosody_wave1/determinism_replay_results.json` |

## Non-Promoted Historical Artifacts

The following proof artifacts remain in the repository for audit lineage, but their exact claims are not promoted in this README:

- `proofs/artifacts/2026-02-20_zpe_prosody_wave1/before_after_metrics.json`
- `proofs/artifacts/2026-02-20_zpe_prosody_wave1/prosody_retrieval_eval.json` (PRO-C006: FAIL — p@5=0.31 vs threshold 0.80)
- `proofs/artifacts/2026-02-20_zpe_prosody_wave1/quality_gate_scorecard.json` (overall gate FAIL; PRO-C005 PAUSED_EXTERNAL, PRO-C006 FAIL)
- `proofs/artifacts/c006_retrieval_failure_analysis.md`
- `proofs/artifacts/c005_replacement_analysis.md`

## What Is Not Claimed

- No lane pass.
- No retrieval closure above threshold.
- No commercialization-safe transfer closure.
- No public release-readiness claim.
- No speech-codec comparator leadership vs production systems.
- No MOS claim — transfer evaluation was not executed end to end with a commercially safe transfer stack.

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
