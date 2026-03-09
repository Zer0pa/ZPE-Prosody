PYTHON ?= python3
PIP ?= $(PYTHON) -m pip

.PHONY: bootstrap test package-sanity portability-lint

bootstrap:
	$(PIP) install --upgrade pip
	$(PIP) install -e ".[dev]"

test:
	PYTHONPATH=src $(PYTHON) -m unittest discover -s tests -p 'test_*.py'

package-sanity:
	$(PYTHON) -c "import tomllib, pathlib; data = tomllib.loads(pathlib.Path('pyproject.toml').read_text()); print(data['project']['name'])"
	PYTHONPATH=src $(PYTHON) -c "import zpe_prosody; print('exports=' + ','.join(sorted(zpe_prosody.__all__)))"
	$(PYTHON) -m compileall src scripts tests

portability-lint:
	@if rg -n --no-heading -S '/Users/[A-Za-z0-9._ -]+|[A-Za-z]:\\\\' \
		README.md AUDITOR_PLAYBOOK.md PUBLIC_AUDIT_LIMITS.md \
		CONTRIBUTING.md SECURITY.md RELEASING.md SUPPORT.md \
		docs proofs/runbooks \
		-g '*.md' -g '*.json'; then \
		echo 'portability-lint: FAIL (machine-absolute path residue found in live docs)'; \
		exit 1; \
	else \
		echo 'portability-lint: PASS'; \
	fi
