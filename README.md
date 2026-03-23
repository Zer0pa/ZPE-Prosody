<p align="center">
  <img src=".github/assets/readme/zpe-masthead.gif" alt="ZPE Prosody Masthead" width="100%">
</p>

<table width="100%" cellpadding="0" cellspacing="0">
  <tr>
    <td align="center">
      <a href="#quickstart"><img src=".github/assets/readme/nav/quickstart-and-license.svg" alt="Quickstart" width="180"></a>
    </td>
    <td align="center">
      <a href="#what-this-is"><img src=".github/assets/readme/nav/what-this-is.svg" alt="What This Is" width="180"></a>
    </td>
    <td align="center">
      <a href="#canonical-authority"><img src=".github/assets/readme/nav/current-authority.svg" alt="Current Authority" width="180"></a>
    </td>
    <td align="center">
      <a href="#supporting-docs"><img src=".github/assets/readme/nav/go-next.svg" alt="Go Next" width="180"></a>
    </td>
  </tr>
</table>

<a id="quickstart"></a>
<p>
  <img src=".github/assets/readme/section-bars/quick-start.svg" alt="QUICK START" width="100%">
</p>
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
make repo-sanity
make package-sanity
make test
```
Optional install surfaces:
- `python -m pip install ".[api]"` for the FastAPI/Uvicorn wrapper
- `python -m pip install ".[benchmarks]"` for the NumPy-backed benchmark helpers

Technical release truth:
- The base wheel ships only the `src/zpe_prosody` package.
- `scripts/` remains a repo-local operational harness, not an installed CLI surface.
- `make package-sanity` builds sdist and wheel, then verifies isolated base, `api`, and `benchmarks` installs from the built wheel.

<p>
  <img src=".github/assets/readme/zpe-masthead-option-3.4.gif" alt="ZPE Prosody Upper Insert" width="100%">
</p>

<a id="what-this-is"></a>
<p>
  <img src=".github/assets/readme/section-bars/what-this-is.svg" alt="WHAT THIS IS" width="100%">
</p>
`ZPE Prosody` is the private staging repository for the ZPE Prosody Wave-1 lane. It is the authority surface for lane status and accepted claims, and it is not a public release surface.

<p>
  <img src=".github/assets/readme/zpe-masthead-option-3.5.gif" alt="ZPE Prosody Lower Insert" width="100%">
</p>

<a id="canonical-authority"></a>
<p>
  <img src=".github/assets/readme/section-bars/lane-status-snapshot.svg" alt="LANE STATUS SNAPSHOT" width="100%">
</p>
Canonical authority block (sole lane truth):
<table width="100%" border="1" bordercolor="#b8c0ca" cellpadding="0" cellspacing="0">
  <thead>
    <tr>
      <th align="left">Authority signal</th>
      <th align="left">Accepted truth</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Repo stage</td>
      <td>Private staging only</td>
    </tr>
    <tr>
      <td>Lane verdict</td>
      <td><code>FAIL</code></td>
    </tr>
    <tr>
      <td>Accepted claim snapshot</td>
      <td><code>PRO-C001 PASS</code>, <code>PRO-C002 PASS</code>, <code>PRO-C003 PASS</code>, <code>PRO-C004 PASS</code>, <code>PRO-C005 PAUSED_EXTERNAL</code>, <code>PRO-C006 FAIL</code></td>
    </tr>
    <tr>
      <td>Authority bundle path</td>
      <td><code>proofs/artifacts/2026-02-20_zpe_prosody_wave1/</code></td>
    </tr>
    <tr>
      <td>Public release readiness</td>
      <td>No</td>
    </tr>
    <tr>
      <td>Acquisition surface</td>
      <td>Private GitHub repo only (access by owner invitation)</td>
    </tr>
  </tbody>
</table>

<p>
  <img src=".github/assets/readme/zpe-masthead-option-3-2.gif" alt="ZPE Prosody Mid Masthead" width="100%">
</p>

<p>
  <img src=".github/assets/readme/section-bars/repo-shape.svg" alt="REPO SHAPE" width="100%">
</p>
- `src/zpe_prosody/`: lane package
- `scripts/`: gate and packaging scripts
- `tests/`: unit coverage
- `data/fixtures/`: deterministic fixtures
- `proofs/`: proof index, final status, runbooks, adjudicated bundle
- `docs/`: architecture, legal boundaries, release-contract notes

<p>
  <img src=".github/assets/readme/zpe-masthead-option-3-3.gif" alt="ZPE Prosody Lower Masthead" width="100%">
</p>

<a id="supporting-docs"></a>
<p>
  <img src=".github/assets/readme/section-bars/where-to-go.svg" alt="WHERE TO GO" width="100%">
</p>
Supporting docs and authority anchors (start here for verification):
- `docs/CANONICAL_DOC_REGISTRY.md`
- `proofs/PROOF_INDEX.md`
- `proofs/FINAL_STATUS.md`
- `AUDITOR_PLAYBOOK.md`
- `PUBLIC_AUDIT_LIMITS.md`
- `docs/README.md`
- `docs/ARCHITECTURE.md`
- `docs/LEGAL_BOUNDARIES.md`

<p>
  <img src=".github/assets/readme/section-bars/out-of-scope.svg" alt="OUT OF SCOPE" width="100%">
</p>
What is not claimed:
- No public release readiness.
- No commercial-safe transfer closure.
- Retrieval closure on the accepted path is below threshold.
- No Phase 4.5 performance augmentation or Phase 5 blind-clone verification yet.

<p>
  <img src=".github/assets/readme/zpe-masthead-option-3.6.gif" alt="ZPE Prosody Authority Insert" width="100%">
</p>
