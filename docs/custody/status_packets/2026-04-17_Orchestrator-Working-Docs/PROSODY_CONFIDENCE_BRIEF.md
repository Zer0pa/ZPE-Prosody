# Prosody — Confidence Row Closeout

**For:** The ZPE-Prosody Codex agent.
**Scope:** One-row README fix to close the last residual. Do not touch anything else.

## What

The Commercial Readiness table in `README.md` currently has Verdict, Commit SHA, and Source but is **missing the required `Confidence` row**. Per `REPO_PLAYBOOK.md`, the table must contain exactly four fields in this order:

```
| Field | Value |
|-------|-------|
| Verdict | {your current value} |
| Commit SHA | {your current value} |
| Confidence | {percentage from your governing preflight / quality-gate artifact} |
| Source | {your current value} |
```

The `Confidence` value should come from an existing artifact in the repo (preflight report, quality gate scorecard, or equivalent). Do not invent a number. If no governing artifact exists, cite the gate pass rate (e.g. `4/6 gates = 66.7%`) and note the source.

## How

1. On branch `reorientation/2026-04-17`, add the `Confidence` row to the Commercial Readiness table in `README.md`, between the existing `Commit SHA` and `Source` rows.
2. Stage only `README.md`.
3. Add a follow-up commit: `chore: add Confidence field to Commercial Readiness per playbook`.
4. Push to `origin/reorientation/2026-04-17`. PR will auto-update.

Prosody requires PR-with-squash on merge — do **not** self-merge.

## Done condition

Return with the new commit SHA, the value you used for Confidence, and the path of the artifact it came from.
