# ZPE-Prosody Startup Prompt - 2026-04-24

You are the lane agent for **ZPE-Prosody** after a local Mac deletion/reclone event.

Assume no local state is trustworthy except what you can reclone from GitHub or fetch from Hugging Face. Do not narrate readiness or commercial progress unless the governing retrieval gate is actually met.

## Recovery Authorities

- GitHub repo: `https://github.com/Zer0pa/ZPE-Prosody`
- Local repo path after reclone: `/Users/Zer0pa/ZPE/ZPE Prosody/ZPE-Prosody`
- Hugging Face org: `Zer0pa`
- Expected HF identity check: `user=Architect-Prime orgs=Zer0pa`

Current Prosody recovery is GitHub-backed. No live Prosody HF dataset/model/bucket was found under `Zer0pa` on 2026-04-24:

- `Zer0pa/ZPE-Prosody-artifacts`: not found
- `Zer0pa/ZPE-Prosody-models`: not found
- `Zer0pa/ZPE-Prosody-scratch`: not found

The available token identified as `Architect-Prime` with `Zer0pa` membership, but creating `Zer0pa/ZPE-Prosody-artifacts` returned `403 Forbidden`. Do not claim HF custody exists for Prosody until live targets are verified.

## First Commands After Reclone

```bash
mkdir -p "/Users/Zer0pa/ZPE/ZPE Prosody"
git clone https://github.com/Zer0pa/ZPE-Prosody.git "/Users/Zer0pa/ZPE/ZPE Prosody/ZPE-Prosody"
cd "/Users/Zer0pa/ZPE/ZPE Prosody/ZPE-Prosody"
git fetch --all --prune
git status --short --branch
gh pr list --repo Zer0pa/ZPE-Prosody --state open --json number,title,headRefName,isDraft,url
```

If PR #34 has not been merged, recover the handoff/status packet archive from its branch:

```bash
git fetch origin codex/prosody-custody-handoff-2026-04-24
git switch codex/prosody-custody-handoff-2026-04-24
ls docs/custody/status_packets
```

If PR #34 has been merged, read the same files from `main`:

```bash
git switch main
git pull --ff-only
ls docs/custody/status_packets
```

## Current GitHub State To Verify

Open PRs as of this handoff:

- PR #33: `codex/h1-lane-hygiene-prosody` - `[codex] Prosody lane hygiene pass`, ready for review.
- PR #34: `codex/prosody-custody-handoff-2026-04-24` - `docs: archive Prosody custody handoff packets`, ready for review.
- PR #27: `reorientation/2026-04-17` - reorientation doc pass, still open and predates the H1/custody passes.

Relevant pushed branches:

- `main`: baseline at this handoff, current authority unless PRs are merged.
- `codex/h1-lane-hygiene-prosody`: H1 lane hygiene branch; includes metadata, CFF, reproducibility, Zenodo, security-policy corrections.
- `codex/prosody-custody-handoff-2026-04-24`: archives Prosody status packets and this restart prompt under GitHub custody.
- `codex/prosody-branch-hygiene-2026-04-23`: CPU retrieval feasibility work exists here; it is pushed but was not part of the H1 hygiene PR.
- `codex/prosody-lane-hygiene-2026-04-24`: duplicate hygiene branch, superseded by PR #33.
- `docs/pypi-live`, `docs/wedge-align`, `fix/broken-links`: small local-only branches were pushed to origin during custody cleanup.
- `chore/true-sal-v7-restamp-2026-04-22`, `chore/sal-v7-instantiation-2026-04-19`, `reorientation/2026-04-17`: older lane branches retained on origin.

Before doing new work, run:

```bash
git log --branches --not --remotes --oneline --decorate
git branch -vv
```

Expected custody-safe result: no local-only commits.

## Status Packet Archive

Status packets that previously lived only under `/Users/Zer0pa/Status_Packets` are preserved in PR #34 under:

```text
docs/custody/status_packets/
```

Read these first on restart:

```text
docs/custody/status_packets/README.md
docs/custody/status_packets/2026-04-24_HF_Custody_Central_Report/lane_reports/ZPE-Prosody_HF_CUSTODY_REPORT.md
docs/custody/status_packets/2026-04-24_Augmentation_PRD_Readiness/lane_outputs/ZPE-Prosody/READINESS_REPORT.md
docs/custody/status_packets/2026-04-24_Augmentation_PRD_Readiness/lane_outputs/ZPE-Prosody/AUGMENTED_PRD.md
docs/custody/status_packets/2026-04-24_Augmentation_PRD_Readiness/lane_outputs/ZPE-Prosody/RUNBOOK_INDEX.md
docs/custody/status_packets/2026-04-24_Augmentation_PRD_Readiness/lane_outputs/ZPE-Prosody/GPD_EXECUTION_PLAN.md
```

Runbooks are under:

```text
docs/custody/status_packets/2026-04-24_Augmentation_PRD_Readiness/lane_outputs/ZPE-Prosody/runbooks/
```

## Sovereign Prosody Metrics

Treat these as authority facts unless newer committed proof artifacts supersede them:

- Compression: `16.5952x`
- F0 RMSE: `0.8925%`
- Quality score: `47/50`
- Retrieval p@5: `0.3067` vs `0.80` gate
- Commercial lane: `FAIL`

Retrieval is the sovereign blocker. Do not turn compression, F0, or quality wins into commercial readiness. Do not move to GPU work until a CPU-first retrieval feasibility pass justifies it.

## Immediate Work Discipline

1. Reconstruct state from GitHub first.
2. Verify PR #33 and PR #34 status.
3. If owner has merged #33/#34, start from updated `main`.
4. If not merged, use the relevant PR branch for the work being continued.
5. Keep retrieval in scope; treat the `0.80` p@5 gate as the authority gate.
6. Keep code/docs/package posture honest: no beta/commercial success narrative while retrieval fails.
7. Do not invent `.gpd/ROADMAP.md` or `.gpd/STATE.md`; this repo had no active `.gpd` project when checked.
8. Use Mac CPU for small feasibility and validation work.
9. Use RunPod only if CPU feasibility shows remote compute is required or if evidence exists only on RunPod.
10. Use HF for any newly generated large corpora, benchmark packs, model weights, checkpoints, RunPod salvage, or large proof bundles. If Zer0pa HF writes still fail, stop and report the exact target and command that failed.

## Validation Commands

Use Python 3.11 when available:

```bash
python3.11 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
make PYTHON=python repo-sanity package-sanity test
```

If disk is too tight for a venv, the lightweight fallback used during custody was:

```bash
PYTHONPATH=src make PYTHON=python3.11 repo-sanity package-sanity test
```

CFF/build validation for the H1 branch:

```bash
cffconvert --validate -i CITATION.cff
python -m build --outdir /tmp/prosody-h1-build
```

Clean generated bloat after validation:

```bash
rm -rf .venv dist build src/zpe_prosody.egg-info scripts/__pycache__ src/zpe_prosody/__pycache__ tests/__pycache__
```

## HF Check Before Any HF Action

```bash
unset HF_TOKEN
unset HUGGINGFACE_HUB_TOKEN
unset HF_HOME
hf auth whoami
```

Expected ideal output:

```text
user=Architect-Prime orgs=Zer0pa
```

If normalized auth fails but environment-token auth works, record that distinction. Do not print tokens. Do not run `hf auth token`.

If large Prosody artifacts are generated or discovered, intended targets are:

```bash
hf repos create Zer0pa/ZPE-Prosody-artifacts --type dataset --private --exist-ok
hf repos create Zer0pa/ZPE-Prosody-models --type model --private --exist-ok
hf buckets create Zer0pa/ZPE-Prosody-scratch --private --exist-ok
```

If these commands return `403`, block on HF org-write repair. Do not pretend HF custody is complete.

## Deletion Readiness Statement

As of this prompt, the Prosody lane can be recloned from GitHub and continued without relying on the current Mac for repo code, small proof artifacts, hygiene changes, custody handoff documents, or restart instructions.

Deletion caveat: Prosody has no verified live HF artifacts under `Zer0pa`; this is acceptable only because no model/checkpoint files or >20 MB local Prosody artifacts were found in the repo during the custody scan and current Prosody proof/data artifacts are GitHub-sized and already pushed. Any future large retrieval corpus, RunPod salvage, checkpoint, or benchmark pack must go to HF before deletion.
