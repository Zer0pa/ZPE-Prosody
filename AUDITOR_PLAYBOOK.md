<p>
  <img src=".github/assets/readme/zpe-masthead.gif" alt="ZPE Prosody Masthead" width="100%">
</p>

<p>
  <img src=".github/assets/readme/section-bars/what-this-is.svg" alt="WHAT THIS IS" width="100%">
</p>
Shortest honest verification path for the ZPE Prosody private staging repo. Prosody truth only. This playbook is for auditors validating the repo boundary, not a public release claim.

<p>
  <img src=".github/assets/readme/section-bars/verification.svg" alt="VERIFICATION" width="100%">
</p>
What you can verify here today:
<table width="100%" border="1" bordercolor="#b8c0ca" cellpadding="0" cellspacing="0">
  <thead>
    <tr>
      <th align="left">Check</th>
      <th align="left">Current truth</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Repo boundary</td>
      <td>Clean and private-first</td>
    </tr>
    <tr>
      <td>Package surface</td>
      <td>Imports and minimal test surface are live</td>
    </tr>
    <tr>
      <td>Proof bundle</td>
      <td>Accepted historical bundle is present</td>
    </tr>
    <tr>
      <td>Lane verdict</td>
      <td>Still <code>FAIL</code></td>
    </tr>
  </tbody>
</table>

<p>
  <img src=".github/assets/readme/section-bars/setup-and-verification.svg" alt="SETUP AND VERIFICATION" width="100%">
</p>
```bash
git clone https://github.com/Zer0pa/ZPE-Prosody.git zpe-prosody
cd zpe-prosody
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
make package-sanity
make test
```

<p>
  <img src=".github/assets/readme/section-bars/evidence-and-claims.svg" alt="EVIDENCE AND CLAIMS" width="100%">
</p>
Expected current truth for the accepted bundle:
<table width="100%" border="1" bordercolor="#b8c0ca" cellpadding="0" cellspacing="0">
  <thead>
    <tr>
      <th align="left">Signal</th>
      <th align="left">Accepted truth</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Package name</td>
      <td><code>zpe-prosody</code></td>
    </tr>
    <tr>
      <td>Packet format</td>
      <td><code>ZPRS/v1</code></td>
    </tr>
    <tr>
      <td>Minimal unit suite</td>
      <td>Passes</td>
    </tr>
    <tr>
      <td>Accepted lane verdict</td>
      <td><code>FAIL</code></td>
    </tr>
    <tr>
      <td>Accepted claim snapshot</td>
      <td><code>PRO-C001 PASS</code>, <code>PRO-C002 PASS</code>, <code>PRO-C003 PASS</code>, <code>PRO-C004 PASS</code>, <code>PRO-C005 PAUSED_EXTERNAL</code>, <code>PRO-C006 FAIL</code></td>
    </tr>
  </tbody>
</table>

<p>
  <img src=".github/assets/readme/section-bars/proof-corpus.svg" alt="PROOF CORPUS" width="100%">
</p>
<table width="100%" border="1" bordercolor="#b8c0ca" cellpadding="0" cellspacing="0">
  <thead>
    <tr>
      <th align="left">Anchor</th>
      <th align="left">Role</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>proofs/PROOF_INDEX.md</code></td>
      <td>Accepted bundle index</td>
    </tr>
    <tr>
      <td><code>proofs/FINAL_STATUS.md</code></td>
      <td>Accepted status snapshot</td>
    </tr>
    <tr>
      <td><code>proofs/artifacts/2026-02-20_zpe_prosody_wave1/quality_gate_scorecard.json</code></td>
      <td>Accepted scorecard</td>
    </tr>
    <tr>
      <td><code>proofs/artifacts/2026-02-20_zpe_prosody_wave1/claim_status_delta.md</code></td>
      <td>Accepted claim deltas</td>
    </tr>
    <tr>
      <td><code>proofs/artifacts/2026-02-20_zpe_prosody_wave1/handoff_manifest.json</code></td>
      <td>Accepted handoff manifest</td>
    </tr>
  </tbody>
</table>

<p>
  <img src=".github/assets/readme/section-bars/out-of-scope.svg" alt="OUT OF SCOPE" width="100%">
</p>
What this playbook does not establish:
<table width="100%" border="1" bordercolor="#b8c0ca" cellpadding="0" cellspacing="0">
  <thead>
    <tr>
      <th align="left">Not established here</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Phase 4.5 performance augmentation</td>
    </tr>
    <tr>
      <td>Phase 5 blind-clone verification</td>
    </tr>
    <tr>
      <td>Public release readiness</td>
    </tr>
    <tr>
      <td>Commercial-safe closure for <code>PRO-C005</code></td>
    </tr>
    <tr>
      <td>Retrieval closure for <code>PRO-C006</code></td>
    </tr>
  </tbody>
</table>
