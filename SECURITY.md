# Security Policy

This document covers vulnerability reporting for the `ZPE Prosody` private staging repo.

## Report Privately

Do not open a public issue for a security problem.

Report privately to:
- `architects@zer0pa.ai`

Include:
- affected file or component
- reproduction steps or proof of concept
- severity and impact
- whether secrets, credentials, or private data are involved

## What Counts As A Security Issue

- committed secrets or credentials
- dependency or workflow issues that enable code execution or supply-chain compromise
- packaging or repo-boundary mistakes that expose material intended to stay outside the repo

## What Does Not Count

- lane FAIL findings
- falsification results
- claim disputes without a security dimension

Current repo stage is private staging only. Security fixes should preserve that boundary.
