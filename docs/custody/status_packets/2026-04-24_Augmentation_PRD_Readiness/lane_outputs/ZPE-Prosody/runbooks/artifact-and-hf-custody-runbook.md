# Artifact And HF Custody Runbook

## Purpose

Ensure that every large dataset, validation corpus, benchmark pack, proof bundle, model weight, checkpoint, RunPod salvage payload, and large intermediate output used by Prosody augmentation is recoverable from live `Zer0pa` Hugging Face storage.

## Owner / Agent Type

Custody agent.

## Input Artifacts

- Central custody report: `/Users/Zer0pa/Status_Packets/2026-04-24_HF_Custody_Central_Report/lane_reports/ZPE-Prosody_HF_CUSTODY_REPORT.md`
- Local `data/fixtures/`
- Local `proofs/artifacts/`
- Future benchmark outputs from retrieval feasibility.
- Future RunPod outputs if any.

## Procedure

1. Normalize auth before any HF action:
   - `unset HF_TOKEN`
   - `unset HUGGINGFACE_HUB_TOKEN`
   - `unset HF_HOME`
   - `hf auth whoami`
2. Stop if auth is not `user=Architect-Prime orgs=Zer0pa`.
3. Verify existing dataset:
   - `hf datasets info Zer0pa/ZPE-Prosody-artifacts`
4. Confirm expected files:
   - local expected files are `data/fixtures` plus `proofs/artifacts`;
   - remote lane files must match excluding `.gitattributes`.
5. For new large artifacts:
   - upload datasets/proofs to `Zer0pa/ZPE-Prosody-artifacts`;
   - upload model weights/checkpoints to `Zer0pa/ZPE-Prosody-models`;
   - upload RunPod scratch/salvage to `Zer0pa/ZPE-Prosody-scratch`.
6. Write or update an upload manifest with local path, HF path, commit id, and verification count.

## Output Artifacts

- HF verification note.
- Upload manifest.
- Missing artifact report if any local or RunPod-only payload is found.

## Acceptance Gate

- Live `Zer0pa` HF target exists.
- Expected file count matches.
- New large artifacts are uploaded before they are cited in proofs or docs.

## Failure Mode

If an artifact exists only on Mac or RunPod and cannot be uploaded, report the exact path and block any authority claim depending on it.

## Resource Requirement

Mac plus HF. RunPod only if the artifact exists remotely and not locally.
