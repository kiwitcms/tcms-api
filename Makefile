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

.PHONY: build-services
build-services:
	docker build -t kiwitcms/kerberos -f tests/krb5/Dockerfile.kerberos tests/krb5/
	docker build -t kiwitcms/with-kerberos -f tests/krb5/Dockerfile.kiwitcms tests/krb5/

.PHONY: run-services
run-services:
	docker-compose -f tests/krb5/docker-compose.yml up -d
	docker exec -i web_kiwitcms_org /Kiwi/manage.py migrate
	docker exec -i web_kiwitcms_org /Kiwi/manage.py createsuperuser --noinput --username super-root --email root@example.com
	docker cp krb5_kiwitcms_org:/tmp/application.keytab .
	docker cp ./application.keytab web_kiwitcms_org:/Kiwi/application.keytab
	rm ./application.keytab
	docker exec -u 0 -i web_kiwitcms_org /bin/bash -c 'chown 1001:root /Kiwi/application.keytab'
