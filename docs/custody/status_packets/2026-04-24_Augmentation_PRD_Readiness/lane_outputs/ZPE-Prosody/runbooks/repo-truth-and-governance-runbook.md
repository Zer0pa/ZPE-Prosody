# Repo Truth And Governance Runbook

## Purpose

Establish the exact ZPE-Prosody repo truth before any augmentation implementation. This prevents branch drift, parser drift, stale PRs, or hidden local stashes from becoming part of a false execution story.

## Owner / Agent Type

Senior repo/governance agent.

## Input Artifacts

- `/Users/Zer0pa/ZPE/ZPE Prosody/ZPE-Prosody/README.md`
- `/Users/Zer0pa/ZPE/ZPE Prosody/ZPE-Prosody/docs/ARCHITECTURE.md`
- `/Users/Zer0pa/ZPE/ZPE Prosody/ZPE-Prosody/docs/market_surface.json`
- `/Users/Zer0pa/ZPE/ZPE Prosody/ZPE-Prosody/pyproject.toml`
- `/Users/Zer0pa/ZPE/ZPE Prosody/ZPE-Prosody/proofs/artifacts/`
- Governance docs in the augmentation brief folder.
- Central HF custody report for ZPE-Prosody.

## Procedure

1. Run read-only status checks:
   - `git status --short --branch`
   - `git remote -v`
   - `git stash list --date=iso`
   - `gh pr list --repo Zer0pa/ZPE-Prosody --state open`
2. Verify no `.gpd/ROADMAP.md` or `.gpd/STATE.md` exists before claiming GPD orchestration.
3. Check README has the canonical ten-section spine and a valid Commercial Readiness enum.
4. Verify every README proof-anchor path resolves.
5. Parse `docs/market_surface.json`.
6. Record doc drift requiring later GitHub work without mutating GitHub unless authorized.

## Output Artifacts

- Repo truth memo.
- GitHub-required later list.
- Proof-anchor resolution list.
- GPD presence/absence statement.

## Acceptance Gate

- Current branch and working tree state are known.
- Local stashes are explicitly listed.
- Open PRs are classified as current, obsolete, or restack-required.
- No front-door claim exceeds current proof.

## Failure Mode

Execution is blocked if branch/doc/proof state cannot be determined or if proof anchors are missing. Do not proceed by assuming stale docs are true.

## Resource Requirement

Mac only. GitHub inspection is read-only until execution is explicitly authorized.
