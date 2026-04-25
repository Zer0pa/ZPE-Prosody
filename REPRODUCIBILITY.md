# Reproducibility

## Canonical Inputs

- `data/fixtures/manifest.json` - committed fixture manifest for repo-local checks.
- `proofs/artifacts/librispeech_benchmark/sample_manifest.json` - sample benchmark input manifest.
- `proofs/artifacts/2026-02-20_zpe_prosody_wave1/runpod_dataset_stage_manifest.json` - authority-bundle dataset staging manifest.

## Golden-Bundle Hash

Will be populated by the `receipt-bundle.yml` workflow in Wave 3.

## Verification Command

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
make repo-sanity
make package-sanity
make test
```

## Supported Runtimes

- Python 3.11+ for the base `zpe-prosody` package.
- Optional `api` extra for FastAPI and Uvicorn surfaces.
