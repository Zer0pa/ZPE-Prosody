# ZPE-Prosody — Portfolio Hardening Audit

**Date:** 2026-04-24
**Auditor:** Codex lane agent for ZPE-Prosody
**Repo HEAD audited:** `3dd8a456b26831d2598cdb93bf332f345184ca5a`
**Overall verdict:** NEEDS_STRUCTURAL_WORK

---

## A. Seventeen-check results

| # | Check | Verdict | Cite |
|---|---|---|---|
| 1 | Cold-clone install | PASS_UV | `/tmp/zpe-audit-prosody/uv_install.log`: exit 0, `real 10.58` |
| 2 | Dependency pinning + lockfile | BOUNDED + no lockfile | `pyproject.toml:10,13,15-27`; no `uv.lock`/`pylock.toml` found |
| 3 | PyPI state | LIVE_CURRENT | PyPI JSON: `0.1.0`, 2026-04-14, matches `pyproject.toml:7` |
| 4 | Build prerequisites | DOCUMENTED | Pure Python setuptools build `pyproject.toml:1-3`; Quick Start `README.md:96-117` |
| 5 | Cross-file consistency | MAJOR_DRIFT | author drift `pyproject.toml:12`; no `CITATION.cff`; quick-start log exit 2 |
| 6 | PyPI publish pipeline | TOKEN_BASED | `.github/workflows/publish.yml:7-26`; PyPI simple API provenance `None` |
| 7 | SLSA level | NO_PROVENANCE | no `actions/attest-build-provenance`; no `Zer0pa/workflows` usage in `.github/workflows/` |
| 8 | Wheel matrix (Rust-backed) | N/A | Pure Python build backend `pyproject.toml:1-3`; no `Cargo.toml` |
| 9 | Zenodo DOI | ABSENT | no `.zenodo.json`; exact Zenodo query `"ZPE-Prosody"` returned 0 hits |
| 10 | HF Hub presence | ORG_ONLY | HF probes: model 401, dataset 401, space 401 |
| 11 | Scientific metadata | BARE | no `CITATION.cff`/`REPRODUCIBILITY.md`; PyPI classifiers `[]`; no keywords |
| 12 | Reusable workflows | HAND_ROLLED_TAG_FLOATING | 111 workflow LOC; `uses:` tags at `ci.yml:17-18`, `publish.yml:18-24` |
| 13 | Tooling stack | LEGACY | setuptools backend `pyproject.toml:1-3`; raw pip CI `ci.yml:21-24`; ruff only `.pre-commit-config.yaml:1-6` |
| 14 | CI health + security | RED | `ci.yml` 5/5 green; `prosody-ci.yml` 5/5 failing; zizmor 29 findings |
| 15 | Commit signing | GPG_SIGNED | `git log --show-signature -5 origin/main`: RSA key `B5690EEEBB952194`, no public key |
| 16 | SBOM + receipt chain | SBOM_ONLY | GitHub dependency graph SBOM API: SPDX-2.3, 22 packages; `handoff_manifest.json:3-12` hashes |
| 17 | Cross-runtime (Ink only) | N/A | Prosody is not Ink |

### A detail — per-check narrative

Check 1: Fresh clone at `/tmp/zpe-audit-prosody/ZPE-Prosody`; `uv pip install .` built and installed `zpe-prosody==0.1.0` with exit 0 in `/tmp/zpe-audit-prosody/uv_install.log`.

Checks 2/13: Runtime deps are empty, but optional extras are lower-bound only (`fastapi>=0.109`, `numpy>=1.24`, `pytest>=8`, `ruff>=0.6`) in `pyproject.toml:15-27`; no lockfile exists. Build backend is `setuptools.build_meta` (`pyproject.toml:1-3`), not 2026 frontier `uv` + `hatchling`.

Check 3: PyPI is live/current at `zpe-prosody==0.1.0`, but project URLs are `None`, classifiers are `[]`, license is `None`, and PEP 740 provenance is `None` for both wheel and sdist. PyPI page had no rendering-error banner.

Check 5: License metadata is v7.0 (`pyproject.toml:11`, `LICENSE:1-4`), but author is `Zer0pa`, not `Zer0pa (Pty) Ltd` (`pyproject.toml:12`); `CITATION.cff` is absent; README source Quick Start (`README.md:105-111`) failed at `make package-sanity` because `scripts/verify_release_surface.py:42-46` could not import `zpe_prosody`.

Checks 6/7/12/14: Publish workflow declares OIDC permission but still passes `secrets.PYPI_API_TOKEN` (`publish.yml:7-26`). No artifact attestation or reusable workflow is present. Actions use floating tags. `gh run list` shows `ci.yml` green, but `prosody-ci.yml` is red in all 5 latest runs. `zizmor` reported 8 high findings, mostly unpinned actions.

Check 16: Built-in GitHub dependency-graph SBOM exists, but no `anchore/sbom-action`, CycloneDX release artifact, `cosign`, in-toto predicate, or Sigstore workflow is present. Proof hashes exist in `proofs/artifacts/2026-02-20_zpe_prosody_wave1/handoff_manifest.json:3-12`.

---

## B. Gaps identified

1. **Structural:** publishing is token-based and unattested (`publish.yml:24-26`; PyPI provenance `None`), so the repo misses the 2026 Trusted Publishing/PEP 740 baseline.
2. **Structural:** no reusable workflow or SHA-pinned action pattern (`ci.yml:17-18`, `prosody-ci.yml:27-28`, `publish.yml:18-24`), carrying duplicated insecure CI across 111 workflow lines.
3. **Local:** source Quick Start fails at package sanity (`README.md:105-111`; `/tmp/zpe-audit-prosody/quickstart_source.log` exit 2), weakening cold-reader trust despite successful install.
4. **Local:** scientific metadata is bare: no `CITATION.cff`, no `REPRODUCIBILITY.md`, no keywords/classifiers/project URLs (`pyproject.toml:5-27`; PyPI JSON).
5. **Structural:** no public HF/Zenodo surface; HF probes return 401 and exact Zenodo query returns zero records.
6. **Local:** docs still contain retired/private phrasing (`docs/ARCHITECTURE.md:8`, `docs/market_surface.json:5-9`), inconsistent with the public repo posture.

---

## C. Recommended fixes (for Orchestrator rollup — NOT executed here)

1. ⚑ **HIGHEST LEVERAGE**: Move CI/publish to `Zer0pa/workflows` reusable SHA-pinned workflows with Trusted Publishing, PEP 740, artifact attestations, and least-privilege permissions. Effort: M. Blast radius: affects `Zer0pa/workflows` + PyPI. Category: publishing pipeline.
2. Repair README source Quick Start/package-sanity import path so the documented verification sequence passes. Effort: S. Blast radius: self-contained. Category: core install.
3. Add `CITATION.cff`, `REPRODUCIBILITY.md`, pyproject keywords/classifiers/project URLs, and DOI/HF links once minted. Effort: S. Blast radius: affects PyPI/HF Hub. Category: scientific credibility.
4. Create per-lane HF dataset/model/Space surfaces or at minimum dataset card for fixtures/proofs. Effort: M. Blast radius: affects HF Hub. Category: scientific credibility.
5. Replace setuptools-only posture with `uv`-first dev flow and a lockfile; consider `hatchling` for pure Python. Effort: M. Blast radius: self-contained. Category: org-wide leverage.
6. Add release SBOM emission via `anchore/sbom-action` and a receipt-chain design hook for future Sigstore/in-toto predicates. Effort: M. Blast radius: portfolio-wide. Category: proof chain.

---

## D. Frontier-reader impression

A frontier reader sees an honest codec repo with unusually clear negative retrieval evidence: README says `FAIL`, metrics cite proof files, and `uv pip install .` works. That is materially better than a polished but false surface. The hardening layer, though, reads pre-frontier: no Trusted Publishing attestation, no Zenodo/HF scientific surfaces, no CITATION/reproducibility root files, hand-written tag-pinned workflows, red secondary CI, and legacy setuptools/raw-pip packaging. The repo signals useful engineering proof, not yet Astral/HF-level release infrastructure.

---

## E. Scope-discipline attestation

- [x] No edits made to any file in the repo.
- [x] `git status` clean. `git diff` empty.
- [x] `git diff --stat main...HEAD` returns zero lines in audited `/tmp` clone.
- [x] Used fresh venv at `/tmp/zpe-audit-prosody/ZPE-Prosody/.venv` and removed it after checks — did not install into system Python.
- [x] No cross-repo reads (verified ecosystem facts via `gh api` only).
- [x] Card is <=1,800 words.

---

## F. Before / after / delta (validation test)

**Before this audit:** We knew Prosody had honest failed retrieval evidence, but not its 2026 packaging/provenance/HF/Zenodo posture.

**After this audit:** We know `uv` install passes, PyPI is live/current but unattested, source Quick Start fails, CI is mixed/red, and HF/Zenodo/scientific metadata are absent or bare.

**Named delta:** The audit turns "Prosody is honest but blocked on retrieval" into a concrete hardening map: Trusted Publishing/provenance first, Quick Start repair second, scientific metadata/HF/Zenodo third.
