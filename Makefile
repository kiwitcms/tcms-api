.PHONY: flake8
flake8:
	python -m flake8 --exclude=.git *.py tcms_api tests

.PHONY: pylint
pylint:
	PYTHONPATH=. python -m pylint --extension-pkg-whitelist=kerberos \
	                    -d missing-docstring -d duplicate-code \
	                    tcms_api/ tests/

.PHONY: test
test:
	python -m coverage run --source tcms_api setup.py test

.PHONY: build
build:
	./tests/check-build
