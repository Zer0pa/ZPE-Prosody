# ZPE-Prosody — Reorientation Assessment

**Date:** 2026-04-17
**Assessor:** Sonnet sub-agent
**Verdict:** BLOCKED

## Summary

No Codex reorientation pass was performed on ZPE-Prosody. The directory `docs/_reorientation/2026-04-17/` does not exist, no deliverables (NOVELTY_CARD.md, FIX_LOG.md, OPEN_QUESTIONS.md) are present, and no `reorientation/2026-04-17` branch was detected in the repo's git object store. The current README is structurally sound for the playbook and has correct ethos posture overall — no portfolio-wide platform claims, no Compass-8 language, no Hypothesis B migration framing — but there are material residual issues: all six Proof Anchor paths are unresolvable (the `proofs/` tree is absent from the working directory as seen by the filesystem), and `README.md:57` contains a negative-frame beta posture violation ("not a final official release"). Several docs carry "private staging" language that conflicts with the always-in-beta positive frame. Assessment confidence is high that the pass was not executed; it is qualified on the proof-anchor finding because the Glob tool may not traverse git-LFS or sparse-checkout surfaces — but the absence of any `.json` or artifact files in the object tree supports the finding.

## Findings by check

| # | Check | Verdict | Notes |
|---|---|---|---|
| 1 | Completion | FAIL | No `docs/_reorientation/2026-04-17/` directory; no NOVELTY_CARD, FIX_LOG, or OPEN_QUESTIONS; no reorientation branch detected |
| 2 | Scope completeness | FAIL | Pass was not executed; no docs were touched under this pass |
| 3 | Logic triangle | PASS | README "What This Is" states deterministic prosody encoding, wedge ground truth says "Already correct (lane FAIL)"; Key Metrics 4 rows present; wedge framing matches COMMERCIAL_WEDGE_GROUND_TRUTH.md |
| 4 | Website pipeline | FAIL | All 10 headings present and in order; Key Metrics has exactly 4 rows. FAIL: all 6 Proof Anchor paths do not resolve — `proofs/` subtree absent from filesystem (`README.md:75-83`) |
| 5 | Deliverable coherence | FAIL | No deliverables to assess |
| 6 | Hypothesis B cross-ref | PASS | No Compass-8 or Hypothesis B language in any doc; Prosody is a non-Compass-8 lane and no directional-primitive framing was found |
| 7 | Ethos compliance | FAIL | `README.md:57` — "not a final official release" violates always-in-beta positive frame; `docs/ARCHITECTURE.md:8,140` and `CHANGELOG.md:8,21,31` and `docs/family/RELEASE_IMPACT.md:6,14` and `docs/LEGAL_BOUNDARIES.md:13` — repeated "private staging" framing conflicts with ethos always-in-beta posture |
| 8 | Open questions | FAIL | No OPEN_QUESTIONS.md exists; pass not executed |

## Finalization brief

- [ ] Execute the UNIVERSAL_BRIEF reorientation pass: create `docs/_reorientation/2026-04-17/NOVELTY_CARD.md`, `FIX_LOG.md`, and `OPEN_QUESTIONS.md` (if needed); branch `reorientation/2026-04-17`; open PR.
- [ ] `README.md:57` — change "not a final official release" to always-in-beta frame, e.g. "useful now, improving continuously; retrieval closure is the active blocker."
- [ ] `docs/ARCHITECTURE.md:8` — remove "This is not a public release surface"; reframe as always-in-beta.
- [ ] `docs/ARCHITECTURE.md:140` — remove "Private staging, inspection, and future verification only"; reframe as current usage surface.
- [ ] `CHANGELOG.md:8` — remove "not a public release log" negative hedge; state positively what it tracks.
- [ ] `docs/family/RELEASE_IMPACT.md:6` — remove "this repo is private staging only"; reframe around the FAIL blocker without negative posture.
- [ ] `docs/LEGAL_BOUNDARIES.md:13` — remove "private staging boundary" language from scope description.
- [ ] Verify all 6 Proof Anchor paths resolve in the repo tree; if `proofs/` artifacts are absent, remove or annotate the Proof Anchors table accordingly.
- [ ] NOVELTY_CARD must cite `src/zpe_prosody/codec.py` with line ranges for the delta+RLE+zigzag-varint+zlib pipeline; must state Compass-8: NO.
- [ ] FIX_LOG must cover all 7 UNIVERSAL_BRIEF criteria.

## Input to license agent

ZPE-Prosody's genuine novelty is a domain-specific prosodic contour codec (`src/zpe_prosody/codec.py`) using quantized delta coding, zigzag-varint serialization, RLE, and zlib with a structured `.zpros` packet format (magic `ZPRS`, version, per-channel TLV, CRC32) plus a 12-D hand-crafted retrieval embedding in `src/zpe_prosody/retrieval.py:31-51`. Compass-8 does not apply. The lane is in FAIL state (retrieval p@5 = 0.307 vs 0.80 gate); the license agent should note that the retrieval claim (`PRO-C006`) is explicitly blocked and must not be listed as a proven capability in the novelty schedule. The compression and fidelity claims (16.60×, F0 RMSE 0.89%) are verified. No NOVELTY_CARD was produced by the Codex pass — the license agent will need to backfill from source code directly.

## Confidence: 82%

Pass-not-executed finding is high-confidence. Proof-anchor absence is inferred from filesystem glob (no `.json` files found anywhere in repo) rather than direct `ls` verification; if artifacts live in a sparse checkout or LFS pointer state not traversed by Glob, the Check 4 finding could be wrong. Ethos compliance violations are exact string matches in read files.
