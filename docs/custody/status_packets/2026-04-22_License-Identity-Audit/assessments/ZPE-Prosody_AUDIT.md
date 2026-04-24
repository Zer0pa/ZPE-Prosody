# ZPE-Prosody — License & Identity Audit

**Date:** 2026-04-22
**Verdict:** NEEDS-WORK
**Auditor:** Sonnet sub-agent

---

## Summary

ZPE-Prosody ships with SAL v6.2 throughout — LICENSE file, pyproject.toml SPDX field, and docs/market_surface.json — while the canonical reference is SAL v7.0. No badge is present in README, so badge criterion is vacuously noted. A stale contact address (`hello@zer0pa.com`) appears in `docs/market_surface.json`. No Compass-8 fabrications found; the codec is correctly described as a delta + RLE + zigzag-varint + zlib pipeline with no directional primitives. No banned ethos strings detected. Commercial Readiness block is present with four required fields and uses a valid enum Verdict (`FAIL`).

---

## Findings by severity

### CRITICAL

None.

### MAJOR

1. **License version mismatch (§1 / Criterion 1 + 2):** The repo LICENSE is `Zer0pa Source-Available License v6.2` (SPDX: `LicenseRef-Zer0pa-SAL-6.2`). The canonical reference at `/Users/Zer0pa/ZPE_CANONICAL/zpe-diagram/LICENSE` is SAL v7.0 (SPDX: `LicenseRef-Zer0pa-SAL-7.0`, which supersedes v6.2). The mismatch propagates to `pyproject.toml` (`license = "LicenseRef-Zer0pa-SAL-6.2"`) and `docs/market_surface.json` (`"license": "LicenseRef-Zer0pa-SAL-6.2"`). CITATION.cff is absent from the repo, removing one mandatory SPDX surface.

2. **Stale contact in market_surface.json (Criterion 4):** `docs/market_surface.json` line 25 reads `"contact": "hello@zer0pa.com"`. The canonical contact is `architects@zer0pa.ai`. All other locations (LICENSE text, FALSIFICATION_REPORT.md, git commit metadata) use the correct address; the JSON file is the lone offender.

### MINOR

1. **No badge present (Criterion 3):** README.md contains no license badge (`img.shields.io` or equivalent). There is therefore no badge URL or alt-text to verify against v7.0. The criterion cannot pass in the absence of any badge; it is recorded as N-A with a gap flag.

2. **CITATION.cff absent (Criterion 2):** The canonical portfolio repos carry a `CITATION.cff` file with SPDX metadata. ZPE-Prosody has none, meaning one of the four expected SPDX surfaces (pyproject / CITATION / README / docs) is missing entirely.

---

## Criterion scorecard

| # | Criterion | Verdict | Note |
|---|---|---|---|
| 1 | License file correctness | FAIL | LICENSE is SAL v6.2; canonical is SAL v7.0. Full text diverges at header, SPDX identifier, and supersession clause. |
| 2 | SPDX and metadata consistency | FAIL | v6.2 identifier in LICENSE, pyproject.toml, and market_surface.json. CITATION.cff absent. No v7.0 token anywhere. |
| 3 | License badge URL integrity | N-A | No badge in README. Cannot verify v7.0 alignment. Flag as gap. |
| 4 | Contact consistency | PARTIAL | LICENSE body and FALSIFICATION_REPORT.md use `architects@zer0pa.ai` correctly; `docs/market_surface.json` uses stale `hello@zer0pa.com`. |
| 5 | Legal entity consistency | PASS | `Zer0pa (Pty) Ltd, Republic of South Africa` present in LICENSE header (line 2), definitions (line 26), and copyright footer (line 652). No conflicting entity found. |
| 6 | Commercial Readiness shape + Verdict enum | PASS | README Commercial Readiness table carries four fields (Verdict, Commit SHA, Confidence, Source). Verdict = `FAIL` — valid enum member. |
| 7 | Compass-8 claim accuracy | PASS | No Compass-8, P8, N-primitive, directional, or 8-primitive claims anywhere in README, pyproject, docs, or CHANGELOG. Codec described correctly as delta + zigzag + varint + RLE + zlib throughout. Expected: NO. |
| 8 | Ethos posture | PASS | Zero matches for all 11 banned strings across all scanned surfaces. |

---

## Confidence: 92%

Confidence deducted for: (a) proof artifact logs are large and were not exhaustively scanned for banned strings or entity/contact drift; (b) README badge gap is unambiguous but only because the badge is absent rather than wrong — intent unclear.
