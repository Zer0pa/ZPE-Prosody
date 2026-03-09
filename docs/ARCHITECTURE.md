# Architecture

## Core Package

`src/zpe_prosody/` contains the private staging package.

Module layout:
- `codec.py`: packet encode/decode for `ZPRS/v1`
- `extract.py`: deterministic contour generation and fallback extraction
- `eval.py`: fidelity and benchmark helpers
- `retrieval.py`: contour embedding and retrieval scoring
- `transfer.py`: transfer shaping and MOS proxy logic
- `api_service.py`: optional FastAPI-shaped API surface with an in-process fallback contract

## Proof And Gate Surface

- `scripts/`: lane gate scripts and packaging helpers
- `tests/`: lightweight unit suite
- `proofs/artifacts/2026-02-20_zpe_prosody_wave1/`: accepted adjudicated bundle
- `proofs/runbooks/`: live runbooks for the repo boundary

## Repo Boundary Discipline

- external corpora are excluded from the repo
- quarantine assets are excluded from the repo
- scratch runtimes and caches are excluded from the repo
- the repo contains only the material needed for private staging, inspection, and future verification
