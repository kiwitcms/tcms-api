.PHONY: flake8
flake8:
	python -m flake8 --exclude=.git *.py tcms_api tests

.PHONY: pylint
pylint:
	PYTHONPATH=. python -m pylint \
	                    --load-plugins=pylint.extensions.no_self_use \
	                    -d missing-docstring -d duplicate-code \
	                    tcms_api/ tests/

.PHONY: test
test:
	pytest -v --ignore=tests/krb5/ tests/

.PHONY: build
build:
	./tests/check-build

.PHONY: build-services
build-services:
	docker pull pub.kiwitcms.eu/kiwitcms/kiwi

.PHONY: run-services
run-services:
	docker compose -f tests/krb5/docker-compose.yml up -d
	docker exec -i web_kiwitcms_org /Kiwi/manage.py migrate
	docker exec -i web_kiwitcms_org /Kiwi/manage.py createsuperuser --noinput --username super-root --email root@example.com
	cat tests/krb5/db_init.py | docker exec -i web_kiwitcms_org /Kiwi/manage.py shell
	@echo "=== add the following to client's /etc/hosts ==="
	@echo "--- web.kiwitcms.org ---"
	@docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' web_kiwitcms_org

.PHONY: verify-integration
verify-integration:
	PYTHONPATH=. pytest -v ./tests/krb5/integration_test.py

.PHONY: verify-credentials-via-python
verify-credentials-via-python:
	PYTHONPATH=. pytest -v ./tests/krb5/python_credentials_test.py
