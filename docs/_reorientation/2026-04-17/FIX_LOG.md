# Reorientation Fix Log — 2026-04-17

## Drift

- `README.md:74-83` — verified all six Proof Anchor paths with `ls`; no restore, removal, or annotation was needed because the artifact files exist in the repo tree.
- `docs/ARCHITECTURE.md:104-109` — replaced the stale `proofs/runbooks/` row with the existing `proofs/artifacts/librispeech_benchmark/` path.
- `docs/FALSIFICATION_REPORT.md:21-22` — replaced missing `proofs/FINAL_STATUS.md` and `proofs/PROOF_INDEX.md` references with the current `quality_gate_scorecard.json` and `c006_retrieval_failure_analysis.md` artifacts.
- `docs/FALSIFICATION_REPORT.md:35` — removed references to missing `docs/README.md` and `docs/FAQ.md`.
- `docs/FALSIFICATION_REPORT.md:44-47` — removed references to missing `CANONICAL_DOC_REGISTRY.md` and `SUPPORT.md`; pointed readers at the existing legal-boundary doc and proof artifacts.
- `docs/market_surface.json:8` — corrected deployment-model drift to match the current package surface (`pip install zpe-prosody` plus editable install path).

## Clarity

- `README.md:57` — rewrote the release-posture cell to the positive always-in-beta frame while keeping the retrieval blocker explicit.
- `docs/ARCHITECTURE.md:8` — rewrote the opening summary so it describes the current repo surface directly instead of defining it by what it is not.
- `CHANGELOG.md:8-10` — rewrote the changelog scope description as a positive statement of what it tracks.
- `docs/family/RELEASE_IMPACT.md:5-8` — reframed the classification reason around the bounded proof packet and the explicit FAIL blocker.
- `docs/market_surface.json:5-7` — tightened buyer-facing summary and wedge language so it states verified value plus the active blocker directly.

## Consistency

- `docs/ARCHITECTURE.md:61-79`, `README.md:99-120`, `docs/market_surface.json:8` — aligned the install/deployment story across docs: published package, editable repo install, and `.[api]` / `.[benchmarks]` extras.
- `docs/ARCHITECTURE.md:104-109`, `README.md:74-83`, `docs/FALSIFICATION_REPORT.md:21-22` — aligned proof-surface references to artifacts that actually exist in this checkout.

## Framing

- Repo-wide check only — no portfolio-level "single technology", "unified 8-primitive platform", or Hypothesis B framing was present in the active Prosody docs, so no framing rewrite was needed beyond the novelty-card clarification that Compass-8 does not apply here.

## Beta posture

- `README.md:57` — removed "not a final official release."
- `docs/ARCHITECTURE.md:8` — removed "private staging repo" / "not a public release surface" framing.
- `docs/ARCHITECTURE.md:140` — replaced "Private staging, inspection, and future verification only."
- `CHANGELOG.md:8-10`, `CHANGELOG.md:21`, `CHANGELOG.md:31` — removed "not a public release log", "Private staging import", and the `private staging` unreleased marker.
- `docs/family/RELEASE_IMPACT.md:6`, `docs/family/RELEASE_IMPACT.md:14` — removed "private staging only" language.
- `docs/LEGAL_BOUNDARIES.md:13` — removed "private staging boundary" language.
- `docs/market_surface.json:5`, `docs/market_surface.json:8`, `docs/market_surface.json:20` — removed `private-stage` and public-package-negative phrasing from the machine-readable market summary.

## Primitive scope

- `docs/_reorientation/2026-04-17/NOVELTY_CARD.md` — documented explicitly that Compass-8 does not apply to Prosody and cited the actual contour codec implementation in `src/zpe_prosody/codec.py` and `src/zpe_prosody/constants.py`.

## Honest limits

- `docs/_reorientation/2026-04-17/NOVELTY_CARD.md` — flagged `PRO-C006` retrieval as blocked (`p@5 = 0.307` vs `0.80` gate) so the license agent does not promote it as a proven capability.
- `docs/market_surface.json:5-7`, `README.md:62` — kept the retrieval blocker explicit instead of converting the lane into a pass narrative.
