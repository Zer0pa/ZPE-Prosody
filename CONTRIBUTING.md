<p>
  <img src=".github/assets/readme/zpe-masthead.gif" alt="ZPE Prosody Masthead" width="100%">
</p>

ZPE Prosody is a private staging repository for the Prosody Wave-1 lane.
Contributions are evidence-first and scoped to Prosody truth only.
Read this before opening a PR.

---

<p>
  <img src=".github/assets/readme/section-bars/before-you-start.svg" alt="BEFORE YOU START" width="100%">
</p>
ZPE Prosody operates under a falsification-first culture. This means:

- Negative results are first-class artifacts. Do not suppress them.
- Claims require evidence. A PR that asserts improvement without a
  comparator artifact will not be merged.
- Scope discipline is hard: do not inflate a passing local test into a
  lane-level success claim.
- Keep changes narrow. One technical concern per PR is the default.
- Authority anchors live in `README.md`, `proofs/PROOF_INDEX.md`, and
  `proofs/FINAL_STATUS.md`. Do not contradict those without new evidence.

---

<p>
  <img src=".github/assets/readme/section-bars/licensing-of-contributions.svg" alt="LICENSING OF CONTRIBUTIONS" width="100%">
</p>
By submitting a contribution you agree that:

- Your contribution is licensed to Zer0pa under the terms of the
  Zer0pa Source-Available License v6.0 (SAL v6.0).
- You retain copyright in your contribution.
- You grant Zer0pa a perpetual, worldwide, royalty-free, irrevocable
  license to use, modify, reproduce, distribute, sublicense, and
  commercially exploit your contribution as part of the Software.
- You represent that you have the legal right to make the
  contribution and that it does not violate any third-party rights.
- `LICENSE` is the legal source of truth. This section is a plain
  summary and is not legal advice.

---

<p>
  <img src=".github/assets/readme/section-bars/environment-setup.svg" alt="ENVIRONMENT SETUP" width="100%">
</p>
This is a private staging repo. If you do not have access, do not try
to mirror or publish it. For approved contributors:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
make repo-sanity
make package-sanity
```

---

<p>
  <img src=".github/assets/readme/section-bars/running-the-test-suite.svg" alt="RUNNING THE TEST SUITE" width="100%">
</p>
```bash
make test
```

All tests must pass before a PR is opened. If your change touches codec
behaviour, retrieval logic, transfer logic, or gate logic, attach
before/after evidence or an explicit falsification note. If a change
worsens an accepted metric or weakens a proof path, it is a regression
unless clearly documented and approved.

---

<p>
  <img src=".github/assets/readme/section-bars/what-we-accept.svg" alt="WHAT WE ACCEPT" width="100%">
</p>
**Bug fixes** — with a reproduction case and evidence that the fix
resolves it without regressing anything else.

**Adversarial or negative findings** — well-documented failures are
valid contributions.

**Path portability fixes** — normalising machine-absolute paths to
repo-relative paths.

**Documentation corrections** — factual errors, broken links, or
outdated evidence paths, backed by proof.

---

<p>
  <img src=".github/assets/readme/section-bars/what-we-do-not-accept.svg" alt="WHAT WE DO NOT ACCEPT" width="100%">
</p>
- Public release work or visibility changes
- Claims that exceed the Prosody lane scope or contradict the current
  authority snapshot without evidence
- Evidence suppression or removal of failing or INCONCLUSIVE artifacts
- IMC runtime coupling or contract changes without explicit
  cross-lane approval
- Replacing one machine-local absolute path with another
- Broad external-corpus regeneration inside the repo

---

<p>
  <img src=".github/assets/readme/section-bars/pr-process.svg" alt="PR PROCESS" width="100%">
</p>
1. **Branch from `main`** — use a descriptive branch name.
2. **Make the change** — keep scope tight; one concern per PR.
3. **Run tests** — `make test` must pass.
4. **Add evidence** — if behaviour changes, place artifacts under
   `proofs/artifacts/` and reference them in the PR.
5. **Open the PR** — fill every evidence field and explain any
   regressions.

---

<p>
  <img src=".github/assets/readme/section-bars/commit-style.svg" alt="COMMIT STYLE" width="100%">
</p>
- Present tense, imperative mood: `Fix prosody packet header`
- Keep commits atomic — one logical change per commit
- Reference the relevant risk or claim ID if addressing a known issue

---

<p>
  <img src=".github/assets/readme/section-bars/issues.svg" alt="ISSUES" width="100%">
</p>
Use the repo issue tracker if you have access. Include repro steps and
evidence paths; issues without evidence will be triaged as incomplete.

---

<p>
  <img src=".github/assets/readme/section-bars/questions.svg" alt="QUESTIONS" width="100%">
</p>
This is a private staging repo. Direct questions to
`architects@zer0pa.ai` or your internal maintainer contact.
