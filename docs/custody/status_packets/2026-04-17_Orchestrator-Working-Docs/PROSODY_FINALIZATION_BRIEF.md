# Prosody Dedicated Finalization Brief

**Date:** 2026-04-17
**For:** The Codex agent on ZPE-Prosody. This replaces the shared finalization brief for Prosody.
**Repo:** `/Users/Zer0pa/ZPE/ZPE Prosody/ZPE-Prosody/`

---

## What happened

The reorientation pass was **not executed** on ZPE-Prosody. There is no `docs/_reorientation/2026-04-17/` directory, no `NOVELTY_CARD.md`, no `FIX_LOG.md`, no `OPEN_QUESTIONS.md`, no `reorientation/2026-04-17` branch.

The existing README is structurally sound: 10 canonical headings in order, 4-row Key Metrics, wedge framing (deterministic prosody encoding) correct per `COMMERCIAL_WEDGE_GROUND_TRUTH.md`, no Compass-8 or Hypothesis B language. You are NOT rewriting the README — you are executing the standard pass that was skipped, **plus closing two specific residual issues** that the Sonnet audit flagged.

---

## What to do

### Step 1 — Read the source docs

Required reads in this order:
1. `/Users/Zer0pa/Status_Packets/2026-04-17_Orchestrator-Working-Docs/Zer0pa Live Project Ethos.md`
2. `/Users/Zer0pa/Status_Packets/2026-04-17_Orchestrator-Working-Docs/UNIVERSAL_BRIEF.md`
3. `/Users/Zer0pa/Status_Packets/2026-04-17_Orchestrator-Working-Docs/REPO_PLAYBOOK.md`
4. `/Users/Zer0pa/Status_Packets/2026-04-17_Orchestrator-Working-Docs/assessments/ZPE-Prosody_ASSESSMENT.md` — the audit for your repo

### Step 2 — Execute the standard UNIVERSAL_BRIEF pass

All 7 criteria apply: drift, clarity, consistency, framing, beta posture, primitive scope, honest limits. Light touch. Cover all in-scope docs, not just README.

### Step 3 — Close these specific issues flagged by the audit

#### Always-in-beta posture violations (Check 7 FAIL)

- [ ] **`README.md:57`** — "not a final official release" → rewrite to always-in-beta positive frame. Example: "Useful now, improving continuously; retrieval closure is the active engineering focus."
- [ ] **`docs/ARCHITECTURE.md:8`** — remove "This is not a public release surface"; reframe as current usage surface.
- [ ] **`docs/ARCHITECTURE.md:140`** — remove "Private staging, inspection, and future verification only"; reframe.
- [ ] **`CHANGELOG.md:8, 21, 31`** — remove "not a public release log" negative hedges. State positively what it tracks.
- [ ] **`docs/family/RELEASE_IMPACT.md:6, 14`** — remove "this repo is private staging only"; reframe around the retrieval blocker without negative posture.
- [ ] **`docs/LEGAL_BOUNDARIES.md:13`** — remove "private staging boundary" language from scope description.

#### Proof Anchor resolution (Check 4 FAIL)

- [ ] **`README.md:75-83`** — every Proof Anchor path must resolve via `ls`. The Sonnet audit's Glob did not find `.json` files under the claimed paths. Options:
  - **Option A:** Restore the `proofs/` tree from local-only artifacts if they exist at the workspace path.
  - **Option B:** Remove rows whose paths do not resolve; keep only rows whose files actually exist in the repo tree.
  - **Option C:** If the artifacts live in a sparse checkout / LFS pointer state, annotate the Proof Anchors table State column accordingly (`PENDING` or explicit file-fetch note).
  - Pick the option that matches reality. Do not fabricate files.

### Step 4 — Produce the three deliverables

Write these to `docs/_reorientation/2026-04-17/` in your repo:

#### `NOVELTY_CARD.md`

Per UNIVERSAL_BRIEF §Deliverable. Key Prosody specifics:
- **Compass-8: NO** — Prosody uses delta + zigzag + varint + RLE + zlib. No directional primitives. Cite `src/zpe_prosody/codec.py` with line ranges.
- **Novel contributions** should name:
  - The `.zpros` packet format (magic `ZPRS`, per-channel TLV, CRC32) with deterministic replay. Cite.
  - The 12-D hand-crafted retrieval embedding at `src/zpe_prosody/retrieval.py:31-51`. Cite.
  - Any lane-specific quantization choices over F0 / energy / duration contours.
- **Standard techniques** should call out zlib, zigzag-varint, RLE, CRC32 as standard.
- **Honest limits for the license agent:** the retrieval claim (`PRO-C006`) is explicitly blocked (p@5 = 0.307 vs 0.80 gate). Flag this clearly in the card so the license agent does not list retrieval as a proven capability in the novelty schedule. Compression (16.60×) and fidelity (F0 RMSE 0.89%) are verified — those are fair to list.

#### `FIX_LOG.md`

Per UNIVERSAL_BRIEF §Deliverable. Must cover all 7 criteria. Explicitly record every always-in-beta posture rewrite and every proof-anchor fix.

#### `OPEN_QUESTIONS.md`

Include anything unresolved. Likely candidates: whether the 12-D retrieval embedding counts as novelty even though the retrieval claim is blocked; how to treat the lane's FAIL verdict in the license schedule.

---

## Commit and PR

- Branch: `reorientation/2026-04-17` (create it).
- Remember Prosody requires **PR with squash merge** — use `gh pr create` then `gh pr merge --squash --admin` **only if you are merging** (you are not — do not self-merge).
- Commit message: `reorientation: execute Prosody doc pass + beta-posture + proof-anchor fixes`.
- Open PR. Do not self-merge.

---

## Don't

- Don't touch `src/zpe_prosody/codec.py` or any codec source.
- Don't rewrite the existing README structure — it's already aligned.
- Don't promote the blocked retrieval claim.
- Don't push directly to main (Prosody has PR-required branch protection).
- Don't publish externally.

---

## Done condition

- All three deliverables at `docs/_reorientation/2026-04-17/`.
- Every always-in-beta posture violation rewritten.
- Every Proof Anchor path either resolves, is removed, or is honestly annotated.
- Branch pushed, PR open.
- Return with: one-sentence completion summary naming (a) the count of posture rewrites, (b) how Proof Anchors were handled (restore/remove/annotate), (c) the PR URL.

---

*Prosody's wedge is deterministic prosodic feature encoding with a lane-FAIL retrieval claim. The NOVELTY_CARD must be honest about both sides: real novelty on the codec + format + retrieval embedding; explicit blocker on retrieval p@5. The license agent will use this card to scope what Prosody contributes to the novelty schedule.*
