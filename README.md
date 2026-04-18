<p align="center">
  <img src=".github/assets/readme/zpe-masthead.gif" alt="ZPE Prosody Masthead" width="100%">
</p>

---

## What This Is

Deterministic prosody encoding for F0 contours and rhythm patterns where replay must stay stable across runs, platforms, and library versions. The lane remains `FAIL`: compression and fidelity are real, but retrieval closure missed badly enough that the commercial wedge is still blocked.

ZPE-Prosody is aimed at speech-technology and voice-analytics infrastructure teams that care about reproducible prosodic features, not generic audio compression. The current authority packet proves a narrow, auditable codec surface. It does not prove release readiness, commercialization-safe transfer, or retrieval performance strong enough to carry the lane.

| Field | Value |
|-------|-------|
| Architecture | PROSODIC_CONTOUR |
| Encoding | F0_DELTA_V1 |

## Key Metrics

| Metric | Value | Baseline |
|--------|-------|----------|
| COMPRESSION | 16.60× | — |
| F0_RMSE | 0.89% | — |
| ENERGY_RMSE | 2.08% | — |
| RETRIEVAL_P@5 | 0.31 | 0.80 gate |

Source: [before_after_metrics.json](proofs/artifacts/2026-02-20_zpe_prosody_wave1/before_after_metrics.json), [prosody_compression_benchmark.json](proofs/artifacts/2026-02-20_zpe_prosody_wave1/prosody_compression_benchmark.json), [prosody_f0_fidelity.json](proofs/artifacts/2026-02-20_zpe_prosody_wave1/prosody_f0_fidelity.json), [prosody_energy_fidelity.json](proofs/artifacts/2026-02-20_zpe_prosody_wave1/prosody_energy_fidelity.json), [c006_retrieval_failure_analysis.md](proofs/artifacts/c006_retrieval_failure_analysis.md)

## Competitive Benchmarks

No promoted competitive benchmark is live on the current authority surface. The honest reading is narrower: this repo has a real prosody codec packet with real failure evidence on retrieval, so it should not be read as a speech-codec winner table.

| Comparator Surface | Current Reading | Notes |
|--------------------|-----------------|-------|
| Head-to-head public benchmark | Not promoted | Retrieval closure failed, so no commercial-safe comparator claim survives the current packet |

## What We Prove

- Mean compression ratio of `16.60×` on the tracked Wave-1 corpus.
- F0 fidelity at `0.89%` mean RMSE and energy fidelity at `2.08%` mean RMSE on the tracked evaluation slice.
- Bit-stable deterministic replay on the committed Wave-1 determinism path.
- The retrieval route was actually executed and actually failed; the lane block is performance, not missing environment setup.

## What We Don't Claim

- No claim of lane pass.
- No claim of retrieval closure above threshold.
- No claim of commercialization-safe transfer or public release readiness.
- No claim of human MOS validation or speech-codec comparator leadership.
- No claim that the paused external dependency path is closed.

## Commercial Readiness

| Field | Value |
|-------|-------|
| Verdict | FAIL |
| Commit SHA | 3115c5dfb737 |
| Confidence | 94.0% |
| Source | `proofs/artifacts/2026-02-20_zpe_prosody_wave1/quality_gate_scorecard.json`, `proofs/artifacts/c006_retrieval_failure_analysis.md` |

The current lane is useful as a bounded proof packet for deterministic prosody encoding, but not as a released commercial wedge. The blocker is explicit and material: the retrieval method missed badly enough that redesign or descope is the honest next path.

## Tests and Verification

| Code | Check | Verdict |
|------|-------|---------|
| V_01 | Compression benchmark | PASS |
| V_02 | F0 fidelity | PASS |
| V_03 | Energy fidelity | PASS |
| V_04 | Determinism replay | PASS |
| V_05 | Retrieval evaluation | FAIL |

## Proof Anchors

| Path | State |
|------|-------|
| `proofs/artifacts/2026-02-20_zpe_prosody_wave1/prosody_compression_benchmark.json` | VERIFIED |
| `proofs/artifacts/2026-02-20_zpe_prosody_wave1/prosody_f0_fidelity.json` | VERIFIED |
| `proofs/artifacts/2026-02-20_zpe_prosody_wave1/prosody_energy_fidelity.json` | VERIFIED |
| `proofs/artifacts/2026-02-20_zpe_prosody_wave1/determinism_replay_results.json` | VERIFIED |
| `proofs/artifacts/2026-02-20_zpe_prosody_wave1/quality_gate_scorecard.json` | VERIFIED |
| `proofs/artifacts/c006_retrieval_failure_analysis.md` | VERIFIED |

## Repo Shape

| Field | Value |
|-------|-------|
| Proof Anchors | 6 |
| Modality Lanes | 1 |
| Authority Source | `proofs/artifacts/c006_retrieval_failure_analysis.md` |

- `src/zpe_prosody/`: installable codec package.
- `tests/`: repo-local regression checks.
- `scripts/`: operator scripts and packaging helpers.
- `proofs/`: Wave-1 evidence and adjudication artifacts.
- `docs/`: architecture and legal-boundary notes.

## Quick Start

```bash
# Install from PyPI
pip install zpe-prosody
```

Or install from source for the repo-local verification path:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
make repo-sanity
make package-sanity
make test
```

Optional extras:

- `python -m pip install ".[api]"` for the FastAPI/Uvicorn wrapper.
- `python -m pip install ".[benchmarks]"` for the NumPy-backed benchmark helpers.

The base wheel ships only `src/zpe_prosody`. `scripts/` remains a repo-local operator surface, not an installed CLI contract. Read [docs/LEGAL_BOUNDARIES.md](docs/LEGAL_BOUNDARIES.md) before widening any claim from this repo state.
