PYTHON ?= python3
PIP ?= $(PYTHON) -m pip

.PHONY: bootstrap repo-sanity test package-sanity portability-lint

bootstrap:
	$(PIP) install --upgrade pip
	$(PIP) install -e ".[dev]"

repo-sanity:
	$(PYTHON) -m compileall src scripts tests

test:
	$(PYTHON) -m unittest discover -s tests -p 'test_*.py'

package-sanity:
	$(PYTHON) scripts/verify_release_surface.py

portability-lint:
	@if rg -n --no-heading -S '/Users/[A-Za-z0-9._ -]+|[A-Za-z]:\\\\' \
		README.md AUDITOR_PLAYBOOK.md PUBLIC_AUDIT_LIMITS.md \
		CONTRIBUTING.md SECURITY.md RELEASING.md docs/SUPPORT.md \
		docs proofs/runbooks \
		-g '*.md' -g '*.json'; then \
		echo 'portability-lint: FAIL (machine-absolute path residue found in live docs)'; \
		exit 1; \
	else \
		echo 'portability-lint: PASS'; \
	fi
