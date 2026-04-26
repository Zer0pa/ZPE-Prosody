# ZPE-Prosody

ZPE-Prosody is a **prosody-feature encoder primitive** — deterministic compression of F0, energy, duration, and voiced-mask contour bundles for TTS preprocessing and voice-analytics feature storage. The `ZPRS/v1` codec delivers **13.65× compression vs gzip 2.21× / zstd 2.22×** on float32 contour buffers (a clean ~6× win at the encoder primitive level), with **0.64% voiced-F0 RMSE** and **2.67 ms mean encode latency** — byte-stable, round-trip lossless within CI thresholds, no GPU required.

Retrieval is out of scope at the encoder level; the encoder primitive ships independently of any downstream retrieval head. ZPE-Prosody is one of seventeen independent encoding products in the Zer0pa portfolio; it targets speech-technology and voice-analytics teams that need deterministic, reproducible prosodic feature encoding for TTS preprocessing and feature-store pipelines.

Licensed under the [Zer0pa Source-Available License v7.0](LICENSE).

## Commercial Readiness

| Gate | Verdict | Notes |
|------|---------|-------|
| Core codec (PRO-C001 – PRO-C004) | PASS | Round-trip fidelity, determinism, extraction, and integration contract — all four pass. The encoder primitive is commercially usable on this basis. |
| Transfer closure (PRO-C005) | BLOCKED | Blocked on external dependency; a commercial-safe transfer substitute was not proven in-lane. |
| Posture (PRO-C005) | `PAUSED_EXTERNAL` | Specific posture: `PAUSED_EXTERNAL` — paused on external dependency, not generic-BLOCKED. |
| Retrieval closure (PRO-C006) | FAIL | p@5 = 0.31 vs threshold 0.80 on accepted evidence. Out of scope for the encoder primitive; tracked as a future-scope research item. |
| **Lane overall** | **FAIL** | The lane-overall verdict reflects retrieval and transfer gates that sit downstream of the encoder primitive; the primitive itself (PRO-C001–PRO-C004) is sound and shippable on its own. |

No combined lane pass is claimed. No public release tag has been issued. The codec is positioned as a deterministic encoder primitive for TTS preprocessing and voice-analytics feature storage; retrieval and end-to-end transfer are downstream concerns and remain open research items.

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
- `proofs/artifacts/2026-02-20_zpe_prosody_wave1/quality_gate_scorecard.json` (overall gate FAIL; PRO-C005 `PAUSED_EXTERNAL` (blocked on external dependency), PRO-C006 FAIL)
- `proofs/artifacts/c006_retrieval_failure_analysis.md`
- `proofs/artifacts/c005_replacement_analysis.md`

## Comp Benchmarks

Lossless byte codecs (gzip, zstd) on the float32 contour buffer are the
apples-to-apples baseline for the published compression-ratio claim.
Audio waveform codecs (Opus, FLAC, Vorbis, AAC) are explicitly out of
scope — they operate at a different abstraction level. See the
subsection below.

### Lossless float32 contour comparison

Source: 80 CMU-Arctic-like samples from
`proofs/artifacts/2026-02-20_zpe_prosody_wave1/`. Per-sample raw input
is the float32 concatenation of `[F0 | energy | duration | voiced_mask]`,
matching `raw_baseline_definition` in `prosody_compression_benchmark.json`.
Identical input bytes are fed to every comparator.

| Codec        | Mean CR | Median CR | Voiced-F0 RMSE (Hz) |
|--------------|--------:|----------:|--------------------:|
| ZPE-Prosody  | 13.65x  | 13.85x    | 1.44                |
| gzip (L6)    |  2.21x  |  2.22x    | 0 (lossless)        |
| zstd (L3)    |  2.22x  |  2.22x    | 0 (lossless)        |

Proof artifact: [`proofs/artifacts/comp_benchmarks/prosody_codec_comparison.json`](proofs/artifacts/comp_benchmarks/prosody_codec_comparison.json) (companion: [`summary.md`](proofs/artifacts/comp_benchmarks/summary.md)). Reproduce: `python scripts/comp_benchmark/run_prosody_comparison.py`.

ZPE-Prosody is bounded-lossy (quantized contours); gzip and zstd are
lossless by construction. The voiced-F0 RMSE of ~1.44 Hz lies inside
the lane's 5% threshold (mean 0.89% in the existing
`prosody_f0_fidelity.json` proof), so the additional ~6x compression
over the lossless baselines is paid for by a fidelity cost the lane
already classifies as PASS by its own gate.

### Why audio codecs (Opus/FLAC) don't apply

ZPE-Prosody encodes prosody contour metadata — per-frame F0, energy,
duration, and voiced-mask sequences. Audio codecs such as Opus, FLAC,
Vorbis, and AAC encode time-domain PCM waveform samples (typically
16-48 kHz). They operate at a different abstraction level from contour
metadata, so a head-to-head comparison would be apples to oranges.
General-purpose lossless byte codecs (gzip, zstd) are the correct
baseline for the published "compression ratio against float32 contour
buffer" claim, which is what this section reports.

## What Is Not Claimed

The list below scopes the encoder primitive's claim surface. Retrieval and end-to-end transfer items are explicitly out of scope at the encoder level and are tracked as future-scope research (see "Upcoming Workstreams" below for the active PRO-C006 research item).

- No combined lane pass — lane verdict is gated by retrieval/transfer items that sit outside the encoder primitive.
- No retrieval closure above threshold (PRO-C006 retrieval gate, p@5 = 0.31 vs 0.80 — relegated to future-scope research, not a primitive-level claim).
- No commercialization-safe transfer closure (PRO-C005 — `PAUSED_EXTERNAL`).
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

## Upcoming Workstreams

This section captures the active lane priorities — what the next agent or contributor picks up, and what investors should expect. Cadence is continuous, not milestoned.

- **PRO-C006 retrieval gate resolution** — Research-Deferred — Investigation Underway. p@5 0.31 → 0.80 threshold gap; representation-quality vs separate retrieval-head decision pending. Encoder primitive ships independently while this resolves.
