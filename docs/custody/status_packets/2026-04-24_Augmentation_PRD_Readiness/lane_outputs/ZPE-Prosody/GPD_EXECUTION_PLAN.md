# ZPE-Prosody GPD-Ready Execution Plan

This repo currently has no active `.gpd/ROADMAP.md` or `.gpd/STATE.md`. This is therefore a GPD-ready phase plan that can be installed later, not a claim that formal GPD orchestration already exists.

## Proposed Phase

Phase P-Prosody-001: CPU Retrieval Feasibility And Wedge Decision

## Phase Goal

Determine whether `PRO-C006` retrieval can be materially rescued with CPU-first methods, or produce a proof-backed descope plan that narrows ZPE-Prosody to deterministic prosodic feature infrastructure.

## Dependency Chain

1. Repo truth and governance baseline.
2. HF custody verification.
3. Current authority metric reproduction.
4. CPU retrieval implementation.
5. CPU retrieval benchmark sweep.
6. Wedge decision.
7. Proof/docs readiness verification.

## Wave Plan

### Wave 0: Baseline And State

- verify branch, stashes, open PRs;
- run `make test`;
- verify HF dataset `Zer0pa/ZPE-Prosody-artifacts`;
- create authority map.

Checkpoint: no work starts until baseline is recorded.

### Wave 1: Retrieval Harness

- preserve existing 12-D cosine baseline;
- create comparable result schema;
- add deterministic scorer selection.

Checkpoint: current p@5 failure is reproducible.

### Wave 2: CPU Comparator Sweep

- normalized statistics;
- voiced-mask weighting;
- temporal contour shape scoring;
- binary/product-quantized codebook plus Hamming retrieval.

Checkpoint: compare every variant to `0.3067` in-domain and `0.1707` OOD.

### Wave 3: Decision Fork

If in-domain p@5 >= 0.55 and OOD p@5 >= 0.35:

- continue to CPU ANN/index research plan.

If either value misses:

- write descope artifact;
- narrow to deterministic prosody infrastructure;
- preserve failed retrieval proof.

Checkpoint: no mixed evidence pass narrative.

### Wave 4: Verification And Public Surface Plan

- verify tests, proof paths, custody, docs constraints;
- decide whether README/docs can change;
- prepare GitHub-required task list.

Checkpoint: public Commercial Readiness remains `FAIL` unless authority changes.

## Subagent Plan

- Repo/governance explorer: branch, PR, stashes, docs drift, proof anchors.
- Custody explorer: HF file counts, future HF requirements, RunPod path checks if needed.
- Implementation worker: retrieval scorer/harness patch.
- Experiment worker: CPU sweep execution and tables.
- Verification worker: re-run tests, compare metrics, inspect docs claims.
- Final adjudicator: main agent only; subagents do not decide readiness.

## Verification Loop

Every implementation wave must run:

- `make test`;
- current baseline retrieval comparison;
- result schema validation;
- proof-anchor path check for any promoted metric;
- HF custody check for large artifacts.

Failed checks return the phase to the previous wave. No phase can skip the retrieval comparison.

## Checkpoint Policy

- Checkpoint before any code changes.
- Checkpoint after baseline reproduction.
- Checkpoint after each comparator family.
- Checkpoint before any docs/front-door change.
- Checkpoint after HF upload of large artifacts.

Each checkpoint must record:

- git status;
- command log;
- metric table;
- artifact paths;
- pass/fail decision.

## Must Be True Before `gpd-execute-phase` Starts

- A formal `.gpd` structure is either installed or the executor accepts this as a manual GPD-ready plan.
- GitHub mutation is authorized if execution will create commits.
- The current local stashes are resolved or explicitly preserved.
- PR #27 is closed, restacked, or marked out of scope for the execution branch.
- HF auth returns `user=Architect-Prime orgs=Zer0pa`.
- `Zer0pa/ZPE-Prosody-artifacts` is live and contains current proof artifacts.
- The owner accepts the phase objective: retrieval rescue is tested only through CPU-first feasibility; no GPU-first work.

## Kill Conditions

- Current baseline cannot be reproduced.
- CPU variants do not exceed intermediate lift thresholds.
- New method cannot be evaluated on the same accepted protocol.
- Large artifacts cannot be put into HF custody.
- Docs need to hide failure to look coherent.

## Phase Completion Criteria

One of:

- retrieval pass: in-domain p@5 >= 0.80 and OOD p@5 >= 0.65 with reproducible artifacts;
- retrieval continuation: intermediate lift reached and next CPU ANN wave justified;
- descope: rescue failed, failure preserved, and a narrowed PRD/public posture plan is written.
