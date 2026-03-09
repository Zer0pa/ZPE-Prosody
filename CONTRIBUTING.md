# Contributing

This repo is evidence-first and private-first.

## Ground Rules

- Claims require artifacts.
- Negative findings are first-class and must not be suppressed.
- Scope discipline is hard: do not inflate a passing local unit test into a lane-level success claim.
- Keep changes narrow. One technical concern per PR is the default.

## Before Opening A PR

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
make package-sanity
make test
```

## Evidence Expectations

- If you change codec behavior, retrieval logic, transfer logic, or gate logic, attach before/after evidence or an explicit falsification note.
- If you correct a path, make it repo-relative or explicitly historical. Do not replace one machine-local absolute path with another.
- If a change worsens an accepted metric or weakens an existing proof path, it is a regression unless clearly documented and approved.

## Out Of Scope For This Repo

- public release work
- visibility changes
- blind-clone verification
- broad external-corpus regeneration inside the repo

## Licensing

`LICENSE` is the legal source of truth for contribution terms and repo use.
