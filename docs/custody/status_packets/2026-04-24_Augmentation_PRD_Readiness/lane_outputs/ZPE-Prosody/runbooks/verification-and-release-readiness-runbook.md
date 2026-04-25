# Verification And Release Readiness Runbook

## Purpose

Decide whether any repo-front-door, release, or commercial-readiness surface can change after the augmentation wave.

## Owner / Agent Type

Verification/release agent.

## Input Artifacts

- New benchmark results.
- Updated proof artifacts.
- HF upload manifest.
- README and docs.
- Repo playbook and ethos docs.
- Mechanics-layer audit brief.

## Procedure

1. Verify tests:
   - `make test`
   - package sanity if relevant.
2. Verify proof paths:
   - every README proof anchor resolves;
   - every new metric has a proof file.
3. Verify Commercial Readiness:
   - `Verdict` remains `FAIL` unless authority gate passes or a new narrowed authority is explicitly accepted.
4. Verify mechanics:
   - no mechanics block is promoted before artifact grounding;
   - failure surface remains explicit.
5. Verify custody:
   - all large result bundles are in `Zer0pa/ZPE-Prosody-artifacts`;
   - model weights, if any, are in `Zer0pa/ZPE-Prosody-models`.
6. Verify GitHub requirements:
   - no local stash or untracked doc is silently dropped;
   - branch/PR path is explicit.

## Output Artifacts

- Verification report.
- Release/no-release decision.
- GitHub-required changes list.
- HF custody update list.

## Acceptance Gate

Public docs can change only after the underlying proof artifacts support the change. Commercial pass can be claimed only if retrieval gates pass or the lane is formally narrowed with a new accepted authority surface.

## Failure Mode

A docs-only improvement that makes the lane look passed while retrieval is still failed is a hard failure.

## Resource Requirement

Mac plus GitHub later if authorized. HF for proof bundle verification. No RunPod unless remote artifacts exist.
