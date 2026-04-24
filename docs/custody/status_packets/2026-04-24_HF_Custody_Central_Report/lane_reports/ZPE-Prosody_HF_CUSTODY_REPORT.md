# ZPE-Prosody HF Custody Report

LANE:
ZPE-Prosody

LOCAL_PATH:
/Users/Zer0pa/ZPE/ZPE Prosody/ZPE-Prosody

GITHUB_REMOTE:
origin https://github.com/Zer0pa/ZPE-Prosody.git

GITHUB_STATUS:
GitHub read-only correction pass. No git add, commit, push, PR, branch switch, history rewrite, or workflow edit. Current branch/status: `codex/prosody-branch-hygiene-2026-04-23`; working tree clean.

HF_TARGETS_CREATED_OR_REUSED:
- Dataset repo reused/verified: `Zer0pa/ZPE-Prosody-artifacts`
- Model repos: none needed; no local model/checkpoint files found in prior inventory.
- Buckets: none needed; no Prosody RunPod scratch/salvage directory found in prior targeted checks.

LIVE_HF_VERIFICATION:
- Auth check before HF action: `user=Architect-Prime orgs=Zer0pa`
- `hf datasets info Zer0pa/ZPE-Prosody-artifacts` succeeded.
- Live dataset id: `Zer0pa/ZPE-Prosody-artifacts`
- Live author: `Zer0pa`
- Private: `true`
- Live sha: `648d66465069356cb9b14419345bcd0a8f709d4e`
- `hf datasets info` sibling count: 56 including `.gitattributes`.
- Expected lane files from local `data/fixtures` plus `proofs/artifacts`: 55.
- Remote lane files excluding `.gitattributes`: 55.
- Missing expected files: 0.
- Extra lane files: 0.

UPLOADS_COMPLETED:
- `data/fixtures/manifest.json` is present at `Zer0pa/ZPE-Prosody-artifacts/data/fixtures/manifest.json`.
- `proofs/artifacts/` is present under `Zer0pa/ZPE-Prosody-artifacts/proofs/artifacts/`.
- Prior successful HF commits observed:
  - `18b6be863db986645cb74ebc0910e90d153948f3` for `data/fixtures/manifest.json`
  - `648d66465069356cb9b14419345bcd0a8f709d4e` for `proofs/artifacts/`
- Correction pass did not need to redo uploads because live Zer0pa storage exists and exact file comparison passed.

UPLOADS_NOT_DONE:
- No model/checkpoint upload: no `.pt`, `.pth`, `.ckpt`, `.safetensors`, `.onnx`, or equivalent local model artifact was found in prior inventory.
- No bucket upload: no Prosody RunPod scratch/salvage directory was found in prior targeted checks.
- Local Git stashes were not uploaded to HF because they are code/docs/small-proof material and must be handled by a later GitHub commit/push decision.

RUNPOD_ACCESS_REQUIRED:
No. Prior targeted RunPod checks on pod `7k3riasglemecu` found no active Prosody artifact directory at the expected paths: `/workspace/ZPE Prosody`, `/workspace/ZPE-Prosody`, `/workspace/artifacts`, `/workspace/data/ood`, `/workspace/data/ravdess`, `/workspace/artifacts/xtts_transfer`.

GITHUB_REQUIRED_LATER:
- `stash@{2026-04-23 22:42:44 +0200}`: README.md diff plus `WORKSTREAM_PLAN_2026-04-23.md`.
- `stash@{2026-04-14 10:30:14 +0200}`: CITATION.cff plus CONTRIBUTING.md diff.

REMAINING_MACHINE_LOSS_RISK:
- HF-class data/proof artifact risk: closed for local `data/fixtures` and `proofs/artifacts`; live Zer0pa dataset exists and expected file count matches exactly.
- Mac-only risk: two local Git stashes remain outside GitHub by instruction.
- RunPod-only risk: none identified for Prosody in targeted checks.
- Unknown-location risk: raw external corpora referenced by historical RunPod manifests may not be present locally, but committed proof artifacts and benchmark packs are live in Zer0pa HF storage.

NEXT_REQUIRED_ACTION:
NEEDS GITHUB COMMIT LATER
