# RunPod Execution Plan

## Exact Command Chain
- `python3.11 -m venv .runtime/maxwave/venv`
- `.runtime/maxwave/venv/bin/pip install --upgrade pip setuptools wheel`
- `.runtime/maxwave/venv/bin/pip install -r runpod_requirements_lock.txt`
- `.runtime/maxwave/venv/bin/python scripts/gate_m_resource_ingestion.py --out artifacts/2026-02-20_zpe_prosody_wave1 --seed 20260220`
- `.runtime/maxwave/venv/bin/python scripts/gate_m_claim_adjudication.py --out artifacts/2026-02-20_zpe_prosody_wave1 --seed 20260220`
- `.runtime/maxwave/venv/bin/python scripts/gate_e_eval_and_pack.py --out artifacts/2026-02-20_zpe_prosody_wave1 --seed 20260220`

## Expected Artifacts
- `mos_crosscheck_report.json`
- `prosody_transfer_eval.json`
- `prosody_retrieval_eval.json`
- `max_claim_adjudication.json`
- `quality_gate_scorecard.json`
- `handoff_manifest.json`