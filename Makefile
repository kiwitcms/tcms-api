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
	docker cp krb5_kiwitcms_org:/tmp/application.keytab .
	docker cp ./application.keytab web_kiwitcms_org:/Kiwi/application.keytab
	rm ./application.keytab
	docker exec -u 0 -i web_kiwitcms_org /bin/bash -c 'chown 1001:root /Kiwi/application.keytab'
	docker exec -i web_kiwitcms_org /Kiwi/manage.py migrate
	docker exec -i web_kiwitcms_org /Kiwi/manage.py createsuperuser --noinput --username super-root --email root@example.com
	echo "from tcms.management.models import *; Classification.objects.create(name='test-products')" | docker exec -i web_kiwitcms_org /Kiwi/manage.py shell

.PHONY: verify-integration
verify-integration:
	PYTHONPATH=. python -m coverage run --source tcms_api ./tests/krb5/integration_test.py

.PHONY: verify-curl-with-kerberos
verify-curl-with-kerberos:
	# make sure curl supports Negotiate authentication
	curl -V | egrep -i "GSS-Negotiate|GSS-API|Kerberos"

.PHONY: verify-web-login
verify-web-login: verify-curl-with-kerberos
	# grab the page
	curl -k -L -o /tmp/curl.log --negotiate -u: \
	     -b /tmp/cookie.jar -c /tmp/cookie.jar \
	    https://web.kiwitcms.org:8443/login/kerberos/

	# verify user has been logged in
	cat /tmp/curl.log | grep 'Kiwi TCMS - Dashboard'
	cat /tmp/curl.log | grep 'Test executions'
	cat /tmp/curl.log | grep 'Your Test plans'

	# verify username is 'travis', e.g. taken from 'travis@KIWITCMS.ORG' principal
	cat /tmp/curl.log | grep '<a href="/accounts/travis/profile/" target="_parent">My profile</a>'
