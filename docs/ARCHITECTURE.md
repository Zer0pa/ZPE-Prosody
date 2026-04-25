# Architecture

Prosody-only architecture overview for the current public repo surface. Use this to map the package layout and boundaries. This page describes the committed release surface only.

## Interface Contracts

Core package location: <code>src/zpe_prosody/</code>. The table below describes the in-repo responsibilities only.
<table width="100%" border="1" bordercolor="#b8c0ca" cellpadding="0" cellspacing="0">
  <thead>
    <tr>
      <th align="left">Module</th>
      <th align="left">Responsibility</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>codec.py</code></td>
      <td>Packet encode/decode for <code>ZPRS/v1</code></td>
    </tr>
    <tr>
      <td><code>extract.py</code></td>
      <td>Deterministic contour generation and fallback extraction</td>
    </tr>
    <tr>
      <td><code>eval.py</code></td>
      <td>Fidelity and benchmark helpers</td>
    </tr>
    <tr>
      <td><code>retrieval.py</code></td>
      <td>Contour embedding and retrieval scoring</td>
    </tr>
    <tr>
      <td><code>transfer.py</code></td>
      <td>Transfer shaping and MOS proxy logic</td>
    </tr>
    <tr>
      <td><code>api_service.py</code></td>
      <td>Optional FastAPI-shaped API surface with an in-process fallback contract</td>
    </tr>
  </tbody>
</table>

## Technical Release Surface

Only Prosody truth for the release surface:
<table width="100%" border="1" bordercolor="#b8c0ca" cellpadding="0" cellspacing="0">
  <thead>
    <tr>
      <th align="left">Surface</th>
      <th align="left">Current truth</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Base distribution</td>
      <td>Zero-dependency <code>zpe-prosody</code> Python package</td>
    </tr>
    <tr>
      <td>Optional extra</td>
      <td><code>api</code> for FastAPI/Uvicorn</td>
    </tr>
    <tr>
      <td>Optional extra</td>
      <td><code>benchmarks</code> for NumPy-backed benchmark helpers</td>
    </tr>
    <tr>
      <td>Repo-local only</td>
      <td><code>scripts/</code> gate harness, external-corpus tooling, operator scratch workflows</td>
    </tr>
    <tr>
      <td>CLI surface</td>
      <td>No installed CLI or gate scripts packaged as runtime entry points</td>
    </tr>
  </tbody>
</table>

## Proof Corpus

<table width="100%" border="1" bordercolor="#b8c0ca" cellpadding="0" cellspacing="0">
  <thead>
    <tr>
      <th align="left">Surface</th>
      <th align="left">Role</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>scripts/</code></td>
      <td>Lane gate scripts and packaging helpers</td>
    </tr>
    <tr>
      <td><code>tests/</code></td>
      <td>Lightweight unit suite</td>
    </tr>
    <tr>
      <td><code>proofs/artifacts/2026-02-20_zpe_prosody_wave1/</code></td>
      <td>Accepted adjudicated bundle</td>
    </tr>
    <tr>
      <td><code>data/fixtures/manifest.json</code></td>
      <td>Committed fixture manifest for repo-local inputs</td>
    </tr>
  </tbody>
</table>

## Scope Discipline

Repo boundary discipline for the current public surface:
<table width="100%" border="1" bordercolor="#b8c0ca" cellpadding="0" cellspacing="0">
  <thead>
    <tr>
      <th align="left">Boundary rule</th>
      <th align="left">Current truth</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>External corpora</td>
      <td>Excluded from the repo</td>
    </tr>
    <tr>
      <td>Quarantine assets</td>
      <td>Excluded from the repo</td>
    </tr>
    <tr>
      <td>Scratch runtimes and caches</td>
      <td>Excluded from the repo</td>
    </tr>
    <tr>
      <td>Repo contents</td>
      <td>Public codec repo with a narrow, evidence-backed proof surface</td>
    </tr>
  </tbody>
</table>
