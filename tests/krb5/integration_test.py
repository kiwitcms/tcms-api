#!/usr/bin/env python

#
# Copyright (c) 2020-2021 Kiwi TCMS project. All rights reserved.
# Author: Alexander Todorov <info@kiwitcms.org>
#

import ssl
import unittest
from unittest.mock import patch

from datetime import datetime

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


class IntegrationTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rpc = TCMS().exec

    def test_readonly_filtering_works(self):
        with patch("requests.sessions.Session") as session:
            session.return_value = DoNotVerifySSLSession()

            results = self.rpc.Product.filter({})
            self.assertGreater(len(results), 0)

    def test_create_objects_works(self):
        with patch("requests.sessions.Session") as session:
            session.return_value = DoNotVerifySSLSession()

            now = datetime.now().isoformat()

            result = self.rpc.Classification.filter(
                {
                    "name": "test-products",
                }
            )[0]
            self.assertEqual(result["name"], "test-products")
            classification_id = result["id"]

            product_name = "tcms-api-%s" % now
            result = self.rpc.Product.create(
                {"name": product_name, "classification": classification_id}
            )
            self.assertEqual(result["name"], product_name)


if __name__ == "__main__":
    unittest.main()
