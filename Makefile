.PHONY: flake8
flake8:
	@flake8 --exclude=.git *.py tcms_api tests

.PHONY: pylint
pylint:
	PYTHONPATH=. pylint --extension-pkg-whitelist=kerberos -d missing-docstring tcms_api/ tests/

test:
	python -m unittest -v tests/*.py

.PHONY: build
build:
	./tests/check-build
