<p align="center">
  <img src=".github/assets/readme/zpe-masthead.gif" alt="ZPE Prosody Masthead" width="100%">
</p>

---

<a id="commercial-front-door"></a>

<a id="what-this-is"></a>


## Quick Start

<a id="quickstart"></a>
<p>
  <img src=".github/assets/readme/section-bars/quick-start.svg" alt="QUICK START" width="100%">
</p>

```bash
# Install from PyPI
pip install zpe-prosody
```

Or install from source (development):

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
make repo-sanity
make package-sanity
make test
```
Optional install surfaces:
- `python -m pip install ".[api]"` for the FastAPI/Uvicorn wrapper
- `python -m pip install ".[benchmarks]"` for the NumPy-backed benchmark helpers

Technical release truth:
- The base wheel ships only the `src/zpe_prosody` package.
- `scripts/` remains a repo-local operational harness, not an installed CLI surface.
- `make package-sanity` builds sdist and wheel, then verifies isolated base, `api`, and `benchmarks` installs from the built wheel.

<p>
  <img src=".github/assets/readme/zpe-masthead-option-3.4.gif" alt="ZPE Prosody Upper Insert" width="100%">
</p>


## What This Is

<p>
  <img src=".github/assets/readme/section-bars/what-this-is.svg" alt="WHAT THIS IS" width="100%">
</p>

Deterministic prosody encoding — F0 contours and rhythm patterns that produce identical outputs across runs, platforms, and library versions. **Lane verdict: FAIL.**

ZPE-Prosody targets speech-technology and voice-analytics infrastructure teams who need auditability and reproducibility in their speech analysis pipelines. The architecture applies. Four of six gates pass. But the lane has not cleared — retrieval closure failed and an external dependency blocks a fifth gate.

**Readiness: private-stage, lane verdict FAIL.** Not a public release surface. No commercial-safe transfer closure.

| Field | Value |
|-------|-------|
| Architecture | PROSODIC_CONTOUR |
| Encoding | F0_DELTA_V1 |

<table width="100%" cellpadding="0" cellspacing="0">
  <tr>
    <td align="center">
      <a href="#quickstart"><img src=".github/assets/readme/nav/quickstart-and-license.svg" alt="Quickstart" width="180"></a>
    </td>
    <td align="center">
      <a href="#what-this-is"><img src=".github/assets/readme/nav/what-this-is.svg" alt="What This Is" width="180"></a>
    </td>
    <td align="center">
      <a href="#canonical-authority"><img src=".github/assets/readme/nav/current-authority.svg" alt="Current Authority" width="180"></a>
    </td>
    <td align="center">
      <a href="#supporting-docs"><img src=".github/assets/readme/nav/go-next.svg" alt="Go Next" width="180"></a>
    </td>
  </tr>
</table>


## Commercial Readiness

<a id="canonical-authority"></a>
<p>
  <img src=".github/assets/readme/section-bars/lane-status-snapshot.svg" alt="LANE STATUS SNAPSHOT" width="100%">
</p>
| Field | Value |
|-------|-------|
| Verdict | FAIL |
| Commit SHA | 27fecfdc506f |
| Confidence | 67% |
| Source | proofs/FINAL_STATUS.md |

> **Evaluators:** Lane verdict FAIL — PRO-C006 retrieval closure below threshold. Proof artifacts preserved for reference. Contact hello@zer0pa.com.

<p>
  <img src=".github/assets/readme/zpe-masthead-option-3.6.gif" alt="ZPE Prosody Authority Insert" width="100%">
</p>


## Key Metrics

| Metric | Value | Baseline |
|--------|-------|----------|
| COMPRESSION | 16.60× | 13.01× on LibriSpeech test-clean |
| F0_RMSE | 0.89% | vs WORLD ~5–10 Hz |
| ENERGY_RMSE | 2.08% | — |
| GATES | 4/6 | closure; retrieval blocked |

> Note: Retrieval gate (P@5) scored 0.31 vs 0.80 threshold — removed from headline metrics in commit 136d79f; 4/6 reflects remaining non-retrieval gates.
>
> Source: [before_after_metrics.json](proofs/artifacts/2026-02-20_zpe_prosody_wave1/before_after_metrics.json) | [c006_retrieval_failure_analysis.md](proofs/artifacts/c006_retrieval_failure_analysis.md)

<p>
  <img src=".github/assets/readme/zpe-masthead-option-3.5.gif" alt="ZPE Prosody Lower Insert" width="100%">
</p>


## What We Prove

> Auditable guarantees backed by committed proof artifacts. Start at `AUDITOR_PLAYBOOK.md`.

- Codec round-trip fidelity (PRO-C001 PASS)
- Deterministic reproducibility (PRO-C002 PASS)
- Prosodic feature extraction (PRO-C003 PASS)
- Test coverage (PRO-C004 PASS)


## What We Don't Claim

<p>
  <img src=".github/assets/readme/section-bars/out-of-scope.svg" alt="OUT OF SCOPE" width="100%">
</p>
- No claim of lane pass (verdict is FAIL)
- No claim of retrieval closure above threshold (PRO-C006 FAIL)
- No claim of external dependency resolution (PRO-C005 PAUSED)
- Parity between wave-1 corpus compression (16.59×) and real LibriSpeech (13.01×) — gap is expected from corpus difficulty difference
- No claim of release readiness or commercial transfer
- 8-primitive directional encoding — codec uses delta + zigzag + varint + RLE + zlib pipeline; no directional primitives exist in source
- Retrieval quality — P@5 gate failed (0.31 vs 0.80 threshold)
- Human-validated MOS — MOS metric is an arithmetic proxy (see `src/zpe_prosody/transfer.py::mos_proxy`), not a human listening test


## Tests and Verification

| Code | Check | Verdict |
|------|-------|---------|
| V_01 | Codec round-trip fidelity (PRO-C001) | PASS |
| V_02 | Deterministic reproducibility (PRO-C002) | PASS |
| V_03 | Prosodic feature extraction (PRO-C003) | PASS |
| V_04 | Test coverage (PRO-C004) | PASS |
| V_05 | External dependency resolution (PRO-C005) | INC |
| V_06 | Retrieval closure (PRO-C006) | FAIL |


## Proof Anchors

| Path | State |
|------|-------|
| proofs/FINAL_STATUS.md | VERIFIED |
| proofs/PROOF_INDEX.md | VERIFIED |
| proofs/artifacts/2026-02-20_zpe_prosody_wave1/ | VERIFIED |

<p>
  <img src=".github/assets/readme/zpe-masthead-option-3-2.gif" alt="ZPE Prosody Mid Masthead" width="100%">
</p>

<a id="supporting-docs"></a>
<p>
  <img src=".github/assets/readme/section-bars/where-to-go.svg" alt="WHERE TO GO" width="100%">
</p>
Supporting docs and authority anchors (start here for verification):
- `docs/CANONICAL_DOC_REGISTRY.md`
- `proofs/PROOF_INDEX.md`
- `proofs/FINAL_STATUS.md`
- `AUDITOR_PLAYBOOK.md`
- `PUBLIC_AUDIT_LIMITS.md`
- `docs/README.md`
- `docs/ARCHITECTURE.md`
- `docs/LEGAL_BOUNDARIES.md`


## Repo Shape

<p>
  <img src=".github/assets/readme/section-bars/repo-shape.svg" alt="REPO SHAPE" width="100%">
</p>
| Field | Value |
|-------|-------|
| Proof Anchors | 3 |
| Modality Lanes | 1 |
| Authority Source | proofs/FINAL_STATUS.md |

- `src/zpe_prosody/`: lane package
- `scripts/`: gate and packaging scripts
- `tests/`: unit coverage
- `data/fixtures/`: deterministic fixtures
- `proofs/`: proof index, final status, runbooks, adjudicated bundle
- `docs/`: architecture, legal boundaries, release-contract notes

<p>
  <img src=".github/assets/readme/zpe-masthead-option-3-3.gif" alt="ZPE Prosody Lower Masthead" width="100%">
</p>


## Ecosystem

<p>
  <img src=".github/assets/readme/section-bars/family-alignment.svg" alt="ZPE ECOSYSTEM" width="100%">
</p>
This package is part of the [Zer0pa ZPE](https://github.com/Zer0pa) codec portfolio.

See also:
- [ZPE-IMC](https://github.com/Zer0pa/ZPE-IMC)
- `zpe-iot`
- `zpe-xr`
- `zpe-robotics`
- `zpe-geo`
- `zpe-finance`
- `zpe-ink`
- `zpe-neuro`
- `zpe-mocap`
- `zpe-bio`

**Observability:** [Comet dashboard](https://www.comet.com/zer0pa/zpe-prosody/view/new/panels) (public)

## Who This Is For

| | |
|---|---|
| **Ideal first buyer** | Speech-technology or voice-analytics infrastructure team needing deterministic prosodic signal encoding (future — lane not yet cleared) |
| **Pain** | Prosody feature pipelines are non-deterministic across library versions and platforms — audit replay fails silently |
| **Deployment** | Python package (`pip install zpe-prosody`), available on PyPI. FastAPI wrapper via `.[api]` extra |
| **Family position** | Validates ZPE encoding applicability to speech-prosody signal domains. Lane verdict FAIL. Staged/validation tier alongside Neuro, Mocap, and Bio |
