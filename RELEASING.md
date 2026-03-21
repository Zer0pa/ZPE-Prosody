<p>
  <img src=".github/assets/readme/zpe-masthead.gif" alt="ZPE Prosody Masthead" width="100%">
</p>

<p>
  <img src=".github/assets/readme/section-bars/unreleased.svg" alt="UNRELEASED" width="100%">
</p>
This repo is not at public-release stage.

<p>
  <img src=".github/assets/readme/section-bars/release-notes.svg" alt="CURRENT RELEASE POSTURE" width="100%">
</p>
Current release posture (Prosody truth only):
<table width="100%" border="1" bordercolor="#b8c0ca" cellpadding="0" cellspacing="0">
  <thead>
    <tr>
      <th align="left">Signal</th>
      <th align="left">Current truth</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Stage</td>
      <td>Private staging only</td>
    </tr>
    <tr>
      <td>Package surface</td>
      <td>Standalone <code>zpe-prosody</code> wheel built from <code>src/zpe_prosody</code></td>
    </tr>
    <tr>
      <td>Optional extra</td>
      <td>FastAPI/Uvicorn is optional and not part of base install</td>
    </tr>
    <tr>
      <td>Repo-local tooling</td>
      <td>Gate scripts and external-corpus tooling are not part of the wheel contract</td>
    </tr>
    <tr>
      <td>Public visibility action</td>
      <td>No</td>
    </tr>
    <tr>
      <td>Phase 5 blind-clone verification</td>
      <td>Not completed from this repo boundary</td>
    </tr>
    <tr>
      <td>Publish greenlight</td>
      <td>No</td>
    </tr>
  </tbody>
</table>

<p>
  <img src=".github/assets/readme/section-bars/setup-and-verification.svg" alt="TECHNICAL VERIFICATION SURFACE" width="100%">
</p>
Run these before treating the repo as release-aligned:

```bash
python -m pip install -e ".[dev]"
make repo-sanity
make test
make package-sanity
```

<table width="100%" border="1" bordercolor="#b8c0ca" cellpadding="0" cellspacing="0">
  <thead>
    <tr>
      <th align="left">Package sanity check</th>
      <th align="left">Scope</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>make package-sanity</code></td>
      <td>Builds sdist and wheel, then verifies isolated installs for base package import and round-trip smoke</td>
    </tr>
    <tr>
      <td><code>make package-sanity</code></td>
      <td>Verifies <code>api</code> extra import and FastAPI app construction</td>
    </tr>
    <tr>
      <td><code>make package-sanity</code></td>
      <td>Verifies <code>benchmarks</code> extra import and NumPy-backed spectral descriptor extraction</td>
    </tr>
  </tbody>
</table>

<p>
  <img src=".github/assets/readme/section-bars/verification.svg" alt="MINIMUM RELEASE GATE" width="100%">
</p>
Minimum release gate before any visibility change:
<table width="100%" border="1" bordercolor="#b8c0ca" cellpadding="0" cellspacing="0">
  <thead>
    <tr>
      <th align="left">Step</th>
      <th align="left">Requirement</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td>Repo boundary is stable and inspector-ready</td>
    </tr>
    <tr>
      <td>2</td>
      <td>Legal and proof surfaces are coherent</td>
    </tr>
    <tr>
      <td>3</td>
      <td>Exact release commit is reviewed</td>
    </tr>
    <tr>
      <td>4</td>
      <td>Repo inspector and repo tester loops are complete</td>
    </tr>
    <tr>
      <td>5</td>
      <td>Operator gives explicit publish approval</td>
    </tr>
  </tbody>
</table>

Until then, stay private.
