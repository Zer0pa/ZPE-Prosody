# ZPE-Prosody Runbook Index

This index lists the execution runbooks required for the ZPE-Prosody augmentation wave.

| Runbook | Purpose | Owner / Agent Type | Input Artifacts | Output Artifacts | Acceptance Gate | Failure Mode | Required Resource |
|---|---|---|---|---|---|---|---|
| `runbooks/repo-truth-and-governance-runbook.md` | Establish repo truth, governance posture, branch state, and parser-safe doc constraints before implementation | senior repo agent | README, docs, pyproject, PR list, stashes, proof anchors, governance docs | repo truth memo, GitHub-required task list | clean baseline, no hidden claim drift | stale PR/stash/doc drift contaminates execution | Mac |
| `runbooks/artifact-and-hf-custody-runbook.md` | Keep large artifacts, corpora, proof bundles, model weights, and RunPod salvage in HF custody | custody agent | HF custody report, local data/proofs, future benchmark outputs | HF target map, upload manifests, live verification | live Zer0pa HF target contains expected files | artifact exists only on Mac/RunPod | Mac + HF; RunPod only if remote artifact exists |
| `runbooks/proof-and-validation-runbook.md` | Reproduce authority metrics and define exact benchmark evidence for new work | validation agent | Wave-1 bundle, LibriSpeech benchmark, C006 failure analysis, scripts/tests | authority map, result JSONs, failure analysis | metrics reproduce and new results compare against baseline | green tests used as substitute for retrieval gate | Mac; CPU pod optional |
| `runbooks/implementation-runbook.md` | Implement bounded CPU retrieval feasibility without broadening claims | implementation agent | `src/zpe_prosody/retrieval.py`, fixture manifest, retrieval protocol | code patch, benchmark harness, small result artifacts | p@5 lift measured without codec regression | method changes but no authority comparison | Mac CPU |
| `runbooks/retrieval-feasibility-runbook.md` | Run and adjudicate CPU retrieval rescue versus descope decision | experiment agent | current retrieval baseline, corpus protocol, comparator configs | p@5 table, OOD table, go/descope verdict | intermediate lift or explicit kill | mixed evidence turned into pass narrative | Mac CPU first; CPU pod optional; GPU not first |
| `runbooks/verification-and-release-readiness-runbook.md` | Decide whether docs/release surface can change after evidence lands | verifier/release agent | new proofs, mechanics artifact, README/doc constraints | readiness report, docs checklist, release/no-release verdict | no public claim exceeds authority | README implies commercial pass while retrieval fails | Mac + GitHub later |

Execution order:

1. Repo truth and governance.
2. Artifact and HF custody.
3. Proof and validation.
4. Implementation.
5. Retrieval feasibility adjudication.
6. Verification and release readiness.

No public posture change happens before steps 1 through 5 produce proof-backed evidence.
