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

.PHONY: kerberos-image
kerberos-image:
	docker build -t kiwitcms/kerberos -f tests/krb5/Dockerfile.kerberos tests/krb5/

.PHONY: run-kerberos
run-kerberos:
	docker run -d --name krb5_kiwitcms_org kiwitcms/kerberos

.PHONY: kiwitcms-image
kiwitcms-image:
	docker build -t kiwitcms/with-kerberos -f tests/krb5/Dockerfile.kiwitcms tests/krb5/

.PHONY: run-kiwitcms
run-kiwitcms:
	docker run -d --name web_kiwitcms_org kiwitcms/with-kerberos
	docker exec -it web_kiwitcms_org /Kiwi/manage.py migrate
#	docker exec -it web_kiwitcms_org /Kiwi/manage.py createsuperuser
	docker cp krb5_kiwitcms_org:/tmp/application.keytab .
	docker cp ./application.keytab web_kiwitcms_org:/Kiwi/application.keytab
	rm ./application.keytab
	docker exec -u 0 -it web_kiwitcms_org /bin/bash -c 'chown 1001:root /Kiwi/application.keytab'
