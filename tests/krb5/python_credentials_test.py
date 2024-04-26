#!/usr/bin/env python

#
# Copyright (c) 2024 Kiwi TCMS project. All rights reserved.
# Author: Alexander Todorov <info@kiwitcms.org>
#

import ssl
import unittest
from unittest.mock import patch

import requests
from tcms_api import TCMS


try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context


class DoNotVerifySSLSession(requests.sessions.Session):
    def __init__(self):
        super().__init__()
        self.verify = False

    def get(self, url, **kwargs):
        kwargs.setdefault("verify", False)
        return super().get(url, **kwargs)


class PythonCredentialsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rpc = TCMS(
            url="https://web.kiwitcms.org:8443/json-rpc/",
            username="kiwitcms-developer",
            password="hack-me",
        ).exec

    def test_passing_credentials_via_python_works(self):
        with patch("requests.sessions.Session") as session:
            session.return_value = DoNotVerifySSLSession()

            result = self.rpc.User.filter()[0]

            # this is from config file
            self.assertNotEqual(result["username"], "kiwitcms-bot")

            # this is specified in setUpClass() above
            self.assertEqual(result["username"], "kiwitcms-developer")


if __name__ == "__main__":
    unittest.main()
