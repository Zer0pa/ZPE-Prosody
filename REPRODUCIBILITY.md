# ZPE-Prosody Reproducibility

## Canonical Inputs

- `data/fixtures/manifest.json` — deterministic local fixture manifest used by repo tests and gate scripts.
- `proofs/artifacts/2026-02-20_zpe_prosody_wave1/` — accepted Wave-1 proof bundle for compression, fidelity, determinism, transfer adjudication, and retrieval adjudication.
- `proofs/artifacts/librispeech_benchmark/` — retained real-speech LibriSpeech benchmark artifacts.
- `proofs/artifacts/c006_retrieval_failure_analysis.md` — accepted retrieval failure analysis and blocker record.

External emotional-speech corpora are not committed to this repo. Their accepted results are represented by the retained proof artifacts above.

## Golden-Bundle Hash

Will be populated by the `receipt-bundle.yml` workflow in Wave 3.

## Verification Command

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
make PYTHON=python repo-sanity
make PYTHON=python package-sanity
make PYTHON=python test
```

## Supported Runtimes

- Python `>=3.11`.
- Base package has no runtime dependencies.
- Optional `api` extra installs FastAPI/Uvicorn for the wrapper surface.
- Optional `benchmarks` extra installs NumPy-backed benchmark helpers.
- No installed CLI is claimed; `scripts/` remains a repo-local operator surface.
