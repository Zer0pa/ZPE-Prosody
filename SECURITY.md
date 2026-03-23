<p>
  <img src=".github/assets/readme/zpe-masthead.gif" alt="ZPE Prosody Masthead" width="100%">
</p>

<p>
  <img src=".github/assets/readme/section-bars/scope.svg" alt="SCOPE" width="100%">
</p>
This document covers vulnerability reporting for the ZPE Prosody
private staging repo. It covers the `zpe_prosody` package, repo
workflows, and the proof corpus within this repo only. It does not
cover downstream lanes or any public release surface.
If you are uncertain whether a finding is security-relevant, report it
privately and we will triage.

Current repo stage: private staging only. Security fixes must preserve
that boundary. Security claims require evidence paths; if evidence is
missing, label the status as `UNKNOWN` or `INCONCLUSIVE`.

What counts as a security issue in this repo:

- Secrets, credentials, or tokens inadvertently committed to the repo
  or proof artifacts
- Dependency or workflow issues that enable code execution or
  supply-chain compromise
- Packaging or repo-boundary mistakes that expose material intended to
  stay outside the repo

What does not count as a security issue:

- Lane FAIL findings or falsification results
- Claims disputes without a security dimension

---

<p>
  <img src=".github/assets/readme/section-bars/reporting-a-vulnerability.svg" alt="REPORTING A VULNERABILITY" width="100%">
</p>
**Do not open a public issue for a security vulnerability.**

Report privately to:
- **`architects@zer0pa.ai`**

Include:
- A clear description of the issue
- The affected component (package, workflow, artifact, dependency)
- Steps to reproduce or a proof of concept
- Your assessment of severity and impact
- Whether secrets, credentials, or private data are involved

---

<p>
  <img src=".github/assets/readme/section-bars/response-commitment.svg" alt="RESPONSE COMMITMENT" width="100%">
</p>
Response targets are best-effort while the repo remains private staging
and may vary based on access and severity.

<table width="100%" border="1" bordercolor="#b8c0ca" cellpadding="0" cellspacing="0">
  <thead>
    <tr>
      <th align="left">Stage</th>
      <th align="left">Target expectation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Acknowledgement</td>
      <td>Best effort during private staging</td>
    </tr>
    <tr>
      <td>Initial assessment</td>
      <td>Best effort during private staging</td>
    </tr>
    <tr>
      <td>Remediation or mitigation plan</td>
      <td>Scheduled by owner based on severity</td>
    </tr>
  </tbody>
</table>

We follow coordinated disclosure. We will not take legal action against
researchers who report vulnerabilities in good faith and follow this
policy.

---

<p>
  <img src=".github/assets/readme/section-bars/supported-versions.svg" alt="SUPPORTED VERSIONS" width="100%">
</p>
<table width="100%" border="1" bordercolor="#b8c0ca" cellpadding="0" cellspacing="0">
  <thead>
    <tr>
      <th align="left">Version</th>
      <th align="left">Supported</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Private staging main</td>
      <td>✅ Supported (internal only)</td>
    </tr>
    <tr>
      <td>Public releases</td>
      <td>❌ None</td>
    </tr>
  </tbody>
</table>

Security fixes are documented in `CHANGELOG.md`. No public release tags
exist yet.

---

<p>
  <img src=".github/assets/readme/section-bars/out-of-scope.svg" alt="OUT OF SCOPE" width="100%">
</p>
The following are explicitly out of scope for this security policy:

- External publication channels for defensive disclosures
- General bug reports without a security dimension
- Licensing questions — direct those to `LICENSE` or
  `architects@zer0pa.ai`

`LICENSE` is the legal source of truth for licensing terms. This
security policy is an operational summary and is not legal advice.
