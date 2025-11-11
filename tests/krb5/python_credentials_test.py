#!/usr/bin/env python

#
# Copyright (c) 2024 Kiwi TCMS project. All rights reserved.
# Author: Alexander Todorov <info@kiwitcms.org>
#

import unittest

from tcms_api import TCMS


class PythonCredentialsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rpc = TCMS(
            url="https://web.kiwitcms.org:8443/json-rpc/",
            username="kiwitcms-developer",
            password="hack-me",
        ).exec

    def test_passing_credentials_via_python_works(self):
        result = self.rpc.User.filter()[0]

        # this is from config file
        self.assertNotEqual(result["username"], "kiwitcms-bot")

        # this is specified in setUpClass() above
        self.assertEqual(result["username"], "kiwitcms-developer")


if __name__ == "__main__":
    unittest.main()
